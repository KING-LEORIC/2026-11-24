"""Day27 2-step RAG: Rewrite → Retrieve → Rerank → Context → Generation. Stage별 계약."""

# 고정밀 경과 시간 측정 기능 사용
# - perf_counter : 단계별 실행 소요 시간(ms) 계측
from time import perf_counter

# 문서 컨텍스트 변환, ID 추출 및 출처 인덱스 구성 유틸리티 사용
# - context_from_documents : 순위 문서로부터 Context 문자열 및 포함 문서 목록 생성
# - docs_to_ids : Document 목록에서 ID 리스트 추출
# - source_index : citation_id 기준 출처 매핑 인덱스 생성
from coursekit.documents import context_from_documents, docs_to_ids, source_index

# 표준 미답변 상수, 오프라인 답변 생성 및 생성 결과 검증 함수 사용
# - NO_ANSWER : 근거 부족 시 표준 미답변 문구 상수
# - offline_answer : 오프라인 모드 고정 답변 생성
# - validate_generation : 생성 답변 스키마 및 허용 출처 ID 유효성 검증
from coursekit.llm import NO_ANSWER, offline_answer, validate_generation

# 다중 질의 검색 및 고유 질의 목록 구성 유틸리티 사용
# - search_multiple : 복수 질의 기반 검색 실행 및 후보 병합
# - unique_queries : 중복 제거 및 최대 개수 제한 적용 질의 목록 생성
from coursekit.multi_query import search_multiple, unique_queries

"""Rewrite → Retrieve → Rerank → Context → Generation 단계별 계약, 예외 래핑, 계측 및 LCEL 파이프라인 조립을 담당하는 모듈"""


# 단계별 실행 오류 표현 예외 클래스
# - stage : 오류가 발생한 파이프라인 단계명
# - code : 예외 유형명 또는 검증 실패 코드
class StageError(RuntimeError):
    # 단계명과 오류 코드를 저장하고 표준 예외 메시지 초기화
    def __init__(self, stage, code):
        self.stage = stage
        self.code = code
        super().__init__(f"{stage}:{code}")


# RAG 파이프라인 LCEL 체인 생성 함수
# - rewrite_fn, search_fn, rank_fn, generation_fn 및 선택적 multiquery_fn 주입
# - 단계별 시간 측정, 내부 예외 은폐(StageError 변환) 및 트레이스 기록을 포함한 체인 반환
def create_rag_pipeline(
    rewrite_fn, search_fn, rank_fn, generation_fn, *, multiquery_fn=None, offline=False
):
    """Dependency Injection: mock / real 모델의 실행 경로를 명시적으로 선택합니다."""

    # LCEL Runnable 래퍼 생성기 임포트
    # - RunnableLambda : 파이썬 함수를 LCEL 체인 노드로 변환
    from langchain_core.runnables import RunnableLambda

    # 개별 파이프라인 단계 실행 래퍼 생성 함수
    # - 단계 수행 시간(timing_ms) 기록 및 일반 예외를 StageError(단계명, 예외클래스명)로 변환
    def run(name, fn):
        # 상태(state)를 받아 단계 함수를 실행하는 내부 래퍼
        def wrapped(state):
            start = perf_counter()
            try:
                result = fn(state)
            # 이미 규격화된 StageError는 그대로 전파
            except StageError:
                raise
            # 그 외 예외는 민감 세부정보 노출을 막고 StageError로 변환
            except Exception as exc:
                # Error 원문(DB 접속정보/API 응답 등)은 외부로 노출하지 않습니다.
                raise StageError(name, type(exc).__name__) from exc
            # 성공/실패와 무관하게 단계 소요 시간(ms) 기록
            finally:
                state.setdefault("timing_ms", {})[name] = round(
                    (perf_counter() - start) * 1000, 3
                )
            # 마지막 Generation도 trace에 기록합니다. 부품 내부의 처리 시간 측정입니다.
            # 최종 생성 결과 딕셔너리에 누적 timing_ms 복사 반영
            if isinstance(result, dict) and "trace" in result:
                result["trace"]["timing_ms"] = dict(state["timing_ms"])
            return result

        return RunnableLambda(wrapped)

    # 요청 스키마 검증 및 초기 파이프라인 상태 생성 함수
    # - RagRequest로 입력 검증 후 신뢰 역할(trusted_role)과 초기 상태 필드 구성
    def start(req):
        # 요청 검증 모델 임포트
        # - RagRequest : 입력 파라미터 스키마 검증
        from coursekit.api import RagRequest

        # 인증 서버 기준 신뢰 역할 추출 및 사용자 입력 내 trusted_role 제외 검증
        trusted_role = req.get("trusted_role", "learner")
        req = RagRequest.model_validate(
            {k: v for k, v in req.items() if k != "trusted_role"}
        ).model_dump()
        # principal role은 사용자 JSON에 넣지 않습니다. 인증된 서버 코드가 지정합니다.
        # 파이프라인 실행 초기 상태 딕셔너리 구성 및 반환
        return dict(
            req,
            trusted_role=trusted_role,
            search_query=req["query"],
            queries=[],
            candidates=[],
            ranked=[],
            included=[],
            context="",
            status="running",
            timing_ms={},
            source_mode="offline_fixture" if offline else "live",
        )

    # 질의 재작성 단계 처리 함수
    # - use_rewrite 활성 시 rewrite_fn 호출 후 clarification_required 상태 또는 search_query 갱신
    def rewrite(s):
        # 재작성 비활성화 시 현재 상태 그대로 반환
        if not s["use_rewrite"]:
            return s
        plan = rewrite_fn(s["query"], s["history"])
        # 명확화 필요 상태면 상태 및 사유 기록, 아니면 검색 질의 반영
        if plan.status == "clarification_required":
            s["status"] = "clarification_required"
            s["reason"] = plan.reason
        else:
            s["search_query"] = plan.search_query
        return s

    # 다중 검색 질의 목록 구성 단계 처리 함수
    # - 실행 중(running) 상태이고 use_multiquery 활성 시 추가 질의 생성 후 최대 3개 고유 질의 확정
    def queries(s):
        # 진행 중 상태가 아니면 건너뜀
        if s["status"] != "running":
            return s
        # 다중 질의 확장 함수 호출 여부 분기
        additional = multiquery_fn(s["search_query"]) if s["use_multiquery"] else []
        s["queries"] = unique_queries(s["search_query"], additional, max_queries=3)
        return s

    # 후보 문서 검색 단계 처리 함수
    # - 확정된 queries로 search_multiple 실행 후 후보 문서, ID 목록 및 질의 실행 수 저장
    def retrieve(s):
        # 진행 중 상태가 아니면 건너뜀
        if s["status"] != "running":
            return s
        data = search_multiple(
            s["queries"],
            search_fn,
            category=s["category"],
            role=s["trusted_role"],
            candidate_k=s["candidate_k"],
            max_queries=3,
        )
        # 검색 후보 문서 및 ID/실행 횟수 상태 반영
        s["candidates"] = data["documents"]
        s["candidate_ids"] = docs_to_ids(data["documents"])
        s["query_count"] = data["query_count"]
        return s

    # 후보 문서 재순위화 단계 처리 함수
    # - use_rerank 활성 및 후보 존재 시 rank_fn(최대 20건) 호출, 아니면 후보 목록 복사 유지
    def rerank(s):
        # 진행 중 상태가 아니면 건너뜀
        if s["status"] != "running":
            return s
        # 재순위화 활성화 및 후보 존재 여부에 따른 순위 산출
        if s["use_rerank"] and s["candidates"]:
            s["ranked"] = rank_fn(
                s["search_query"], s["candidates"], min(len(s["candidates"]), 20)
            )
        else:
            s["ranked"] = s["candidates"][:]
        s["ranked_ids"] = docs_to_ids(s["ranked"])
        return s

    # 컨텍스트 조립 단계 처리 함수
    # - context_k 및 max_chars=650 기준으로 최종 Context 문자열과 포함 문서·ID 목록 생성
    def context(s):
        # 진행 중 상태가 아니면 건너뜀
        if s["status"] != "running":
            return s
        s["context"], s["included"] = context_from_documents(
            s["ranked"], context_k=s["context_k"], max_chars=650
        )
        s["included_ids"] = docs_to_ids(s["included"])
        return s

    # 최종 답변 생성 및 출처 검증 단계 처리 함수
    # - clarification_required 또는 빈 context는 미답변(insufficient_context) 처리
    # - 오프라인/라이브 모드별 답변 생성 및 인용 ID의 포함 Context 소속 여부 검증 후 결과 반환
    def generate(s):
        # 명확화 필요 상태일 경우 미답변 결과 및 트레이스 반환
        if s["status"] == "clarification_required":
            return {
                "status": "clarification_required",
                "result": {
                    "status": "insufficient_context",
                    "answer": NO_ANSWER,
                    "source_ids": [],
                    "missing_information": s["reason"],
                },
                "sources": [],
                "trace": make_trace(s),
            }
        # Context 부재 시 근거 부족 미답변 결과 구성
        if not s["context"]:
            result = {
                "status": "insufficient_context",
                "answer": NO_ANSWER,
                "source_ids": [],
                "missing_information": "현재 검색 범위에 답할 Context가 부족합니다.",
            }
        # 오프라인 모드에서는 고정 답변 생성기 사용
        elif offline:
            result = offline_answer(s["query"], s["context"], s["included"])
        # 라이브 모드에서는 원 질문과 독립 검색 질의를 결합해 생성 후 출처 ID 검증
        else:
            query = s["query"] + "\n[검색용 독립 질문] " + s["search_query"]
            result = validate_generation(
                generation_fn(query, s["context"]),
                {d.metadata["citation_id"] for d in s["included"]},
            )
        # 생성된 source_ids가 실제 포함된 Context 출처 집합 내에 있는지 교차 검증
        index = source_index(s["included"])
        if not set(result["source_ids"]).issubset(index):
            raise StageError("generation", "source_not_in_context")
        sources = [index[cid] for cid in result["source_ids"]]
        # 최종 상태, 답변 결과, 인용 출처 목록 및 실행 트레이스 반환
        return {
            "status": result["status"],
            "result": result,
            "sources": sources,
            "trace": make_trace(s),
        }

    # 파이프라인 실행 추적(trace) 딕셔너리 생성 함수
    # - 질의 이력, 각 단계별 문서 ID 흐름, 질의 횟수, 단계별 소요 시간 및 실행 모드 기록
    def make_trace(s):
        # 생성에 쓰인 원본/검색 질문, 실제 Context IDs를 보존합니다. Key/전체 본문은 기록하지 않습니다.
        return {
            "original_question": s["query"],
            "search_query": s["search_query"],
            "queries": s["queries"],
            "candidate_ids": s.get("candidate_ids", []),
            "ranked_ids": s.get("ranked_ids", []),
            "included_ids": s.get("included_ids", []),
            "query_count": s.get("query_count", 0),
            "timing_ms": s.get("timing_ms", {}),
            "source_mode": s["source_mode"],
        }

    # LCEL의 | 연결은 실행 순서만 준비합니다. invoke 호출에서 실제 Stage를 실행합니다.
    # 파이프라인 단계 순차 연결 및 LCEL Runnable 체인 반환
    chain = (
        RunnableLambda(start)
        | run("rewrite", rewrite)
        | run("multiquery", queries)
        | run("retrieval", retrieve)
        | run("rerank", rerank)
        | run("context", context)
        | run("generation", generate)
    )
    return chain


"""
Rewrite → Retrieve → Rerank → Context → Generation의 전 과정을 LCEL 체인으로 연결하고, 
단계별 소요 시간 계측, 내부 예외 은폐(StageError), 명확화/빈 컨텍스트 조기 분기 및 인용 출처 교차 검증을 통합 구현하였다.
이를 통해 의존성 주입 기반의 유연한 실행 경로 전환과 단계별 디버깅·감사 추적성을 확보하였다.
"""
