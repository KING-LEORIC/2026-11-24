"""단계별 역할 분리: services/audit.py / 독립 실행은 main.py."""

"""재순위화 전·후 후보 집합 동일성, 출처 메타데이터 유지 및 이전 순위 기록 여부를 감사하는 서비스 모듈"""


# 재순위화 결과 감사 함수
# - 재순위화 후 문서가 기존 후보 풀(before) 내에 속하는지 확인
# - source_locator, citation_id 메타데이터 및 pre_rank 기록 유지 여부 반환
def audit_ranking(before, ranked):
    """Reranking으로 새 문서를 창작하지 않으며 출처와 이전 순위를 유지합니다."""
    # BEGIN D27-05-A04
    # TODO D27-05-A04: Reranking으로 새 문서를 창작하지 않으며 출처와 이전 순위를 유지합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 재순위화 이전 후보 문서들의 chunk_id 집합 생성
    before_ids = {d.metadata["chunk_id"] for d in before}
    # 후보 풀 일치 여부, 출처 메타데이터 보존 여부 및 이전 순위 기록 여부 반환
    return {
        "same_candidate_pool": all(
            d.metadata["chunk_id"] in before_ids for d in ranked
        ),
        "metadata_kept": all(
            "source_locator" in d.metadata and "citation_id" in d.metadata
            for d in ranked
        ),
        "pre_rank_recorded": all("pre_rank" in d.metadata for d in ranked),
    }
    # raise NotImplementedError("D27-05-A04 미완성")
    # END D27-05-A04


"""
재순위화 결과가 기존 검색 후보 집합에서 벗어나지 않는지 검증하고, 출처 정보(source_locator, citation_id)와 
이전 순위(pre_rank) 메타데이터가 누락 없이 남았는지 감사하도록 구현하였다.
이를 통해 순위 변경 과정에서 발생할 수 있는 문서 변조나 출처 소실을 사전에 차단하였다.
"""
