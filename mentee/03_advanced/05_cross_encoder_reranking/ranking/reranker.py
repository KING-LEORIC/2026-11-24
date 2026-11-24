"""단계별 역할 분리: ranking/reranker.py / 독립 실행은 main.py."""

"""기존 후보 문서 집합을 스코어러 기준으로 재정렬해 상위 top_n 문서를 반환하는 모듈"""


# 후보 문서 재순위화 함수
# - 신규 후보 생성 없이 기존 docs를 scorer로 평가해 상위 top_n=3 문서 반환
def rank_documents(question, docs, scorer):
    """Reranker는 후보를 새로 찾지 않고 동일 후보를 순위 변경합니다."""
    # BEGIN D27-05-A02
    # TODO D27-05-A02: Reranker는 후보를 새로 찾지 않고 동일 후보를 순위 변경합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # coursekit 재순위화 유틸리티(rerank_documents) 호출 및 상위 3건 반환
    from coursekit.reranking import rerank_documents

    return rerank_documents(question, docs, scorer, top_n=3)
    # raise NotImplementedError("D27-05-A02 미완성")
    # END D27-05-A02


"""
검색 단계에서 확보된 후보 문서 풀을 유지한 채 CrossEncoder 스코어러 기반으로 순위만 재배치하고 
상위 3개 문서를 선별하도록 구현하였다.
이를 통해 재순위화 단계의 책임을 순위 조정으로 명확히 한정하였다.
"""
