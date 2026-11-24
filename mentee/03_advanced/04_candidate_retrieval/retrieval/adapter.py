"""단계별 역할 분리: retrieval/adapter.py / 독립 실행은 main.py."""

"""후보 검색 요청 페이로드 구성 및 Retriever 호출·candidate_k 상한 검증을 담당하는 어댑터 모듈"""


# 후보 검색 요청 페이로드 생성 함수
# - 질의(query), 카테고리(category), 후보 검색 상한(candidate_k=5), 컨텍스트 상한(context_k=2) 구성
def make_candidate_request(case):
    """candidate_k와 context_k는 다른 제한값입니다."""
    # BEGIN D27-04-A01
    # TODO D27-04-A01: candidate_k와 context_k는 다른 제한값입니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 검색 쿼리·카테고리 및 분리된 k 제한값(candidate_k, context_k) 딕셔너리 반환
    return {
        "query": case["question"],
        "category": case["category"],
        "candidate_k": 5,
        "context_k": 2,
    }
    # raise NotImplementedError("D27-04-A01 미완성")
    # END D27-04-A01


# Retriever 후보 문서 조회 및 상한 검증 함수
# - retriever.invoke(payload)로 후보 Document 목록 조회
# - 반환 문서 개수가 candidate_k 초과 시 ValueError 발생, 아니면 목록 반환
def fetch_documents(retriever, payload):
    """Day26에서 배운 Runnable.invoke로 후보 Document를 받아옵니다."""
    # BEGIN D27-04-A02
    # TODO D27-04-A02: Day26에서 배운 Runnable.invoke로 후보 Document를 받아옵니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # Retriever invoke 실행으로 후보 문서 목록 수신
    docs = retriever.invoke(payload)
    # 반환 문서 수의 candidate_k 상한 초과 여부 검사
    if len(docs) > payload["candidate_k"]:
        raise ValueError("candidate_k 초과")
    # 검증을 통과한 후보 문서 목록 반환
    return docs
    # raise NotImplementedError("D27-04-A02 미완성")
    # END D27-04-A02


"""
후보 탐색 상한(candidate_k)과 컨텍스트 투입 상한(context_k)을 분리 정의하고, 
Retriever 호출 결과의 건수가 candidate_k를 초과할 경우 즉시 예외를 발생시키도록 구현하였다.
이를 통해 검색 단계의 반환 규모를 통제하고 하위 처리 단계로의 과다 입력 유입을 차단하였다.
"""
