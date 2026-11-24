"""단계별 역할 분리: schemas/request.py / 독립 실행은 main.py."""

"""원 질문과 대화 이력을 유지한 채 검색 상한 및 단계 활성화 플래그를 포함한 파이프라인 요청 스키마 모듈"""


# 파이프라인 실행 요청 페이로드 생성 함수
# - query, history, category 보존 및 candidate_k=5, context_k=2, rewrite/rerank 활성 옵션 설정
def prepare_pipeline_request(case):
    """원 질문과 History를 함께 보존하고 검색용 질문은 Chain 내부에서 만듭니다."""
    # BEGIN D27-06-A01
    # TODO D27-06-A01: 원 질문과 History를 함께 보존하고 검색용 질문은 Chain 내부에서 만듭니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 입력 케이스 정보와 단계 제어 파라미터를 담은 요청 딕셔너리 반환
    return {
        "query": case["question"],
        "history": case["history"],
        "category": case["category"],
        "candidate_k": 5,
        "context_k": 2,
        "use_rewrite": True,
        "use_multiquery": False,
        "use_rerank": True,
    }
    # raise NotImplementedError("D27-06-A01 미완성")
    # END D27-06-A01


"""
사용자 원 질문(query)과 대화 이력(history), 카테고리를 그대로 보존하면서 
후보 수(candidate_k), 컨텍스트 수(context_k), 재작성·다중질의·재순위화 사용 여부를 표준 요청 구조로 구성하도록 구현하였다.
"""
