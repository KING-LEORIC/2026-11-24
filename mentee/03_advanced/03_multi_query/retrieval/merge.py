"""단계별 역할 분리: retrieval/merge.py / 독립 실행은 main.py."""

"""다중 질의 검색 후보(pairs)를 chunk_id 기준으로 병합하고 출처 추적 메타데이터를 기록하는 모듈"""


# 검색 후보 병합 함수
# - chunk_id 기준 중복 제거 및 found_by_query 메타데이터 기록을 merge_found에 위임
def merge_candidates(pairs):
    """chunk_id를 중복 제거 키로 사용하고 found_by_query를 Metadata에 기록합니다."""
    # BEGIN D27-03-A02
    # TODO D27-03-A02: chunk_id를 중복 제거 키로 사용하고 found_by_query를 Metadata에 기록합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # coursekit 다중 질의 후보 병합 유틸리티 호출 및 결과 반환
    from coursekit.multi_query import merge_found

    return merge_found(pairs)
    # raise NotImplementedError("D27-03-A02 미완성")
    # END D27-03-A02


"""
다중 질의 검색에서 수집된 후보 문서 쌍을 chunk_id 단위로 중복 제거하고, 
어떤 질의에서 해당 청크가 탐색되었는지(found_by_query) 메타데이터로 보존하도록 구성하였다.
"""
