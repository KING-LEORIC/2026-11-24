"""단계별 역할 분리: retrieval/planner.py / 독립 실행은 main.py."""

"""원 질문과 확장 질의 후보를 조합해 중복 없는 검색 질의 목록을 생성하는 플래너 모듈"""


# 검색 질의 계획 생성 함수
# - 원 질문(base)과 추가 질의 앞 2개(extras[:2])를 대상으로 최대 3개 고유 질의 구성
def plan_queries(base, extras):
    """원 질문을 포함한 서로 다른 질문 2개로 시작합니다."""
    # BEGIN D27-03-A01
    # TODO D27-03-A01: 원 질문을 포함한 서로 다른 질문 2개로 시작합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 고유 질의 목록 생성 유틸리티(unique_queries) 호출 및 반환
    from coursekit.multi_query import unique_queries

    return unique_queries(base, extras[:2], max_queries=3)
    # raise NotImplementedError("D27-03-A01 미완성")
    # END D27-03-A01


"""
원 질문과 확장 후보 질의를 중복 없이 결합하고 최대 질의 상한(max_queries=3)을 적용하여 
다중 질의 검색의 쿼리 생성 범위를 통제하도록 구현하였다.
"""
