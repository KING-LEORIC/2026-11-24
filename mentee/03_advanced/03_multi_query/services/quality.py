"""단계별 역할 분리: services/quality.py / 독립 실행은 main.py."""

"""다중 질의 목록의 개수·중복·상한 검증 및 병합 후 후보 청크의 중복·출처 보존 감사를 수행하는 서비스 모듈"""


# 검색 질의 목록 품질 점검 함수
# - 질의 총 개수(count), 고유성(unique), 상한(3개 이하) 준수 여부(within_limit) 반환
def check_query_list(queries):
    """검색 요청 수와 중복 여부를 기록합니다."""
    # BEGIN D27-03-A03
    # TODO D27-03-A03: 검색 요청 수와 중복 여부를 기록합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 질의 개수, 고유 여부 및 3개 이하 상한 충족 여부 딕셔너리 반환
    return {
        "count": len(queries),
        "unique": len(queries) == len(set(queries)),
        "within_limit": len(queries) <= 3,
    }
    # raise NotImplementedError("D27-03-A03 미완성")
    # END D27-03-A03


# 병합 후보 감사 로그 생성 함수
# - 병합 문서의 chunk_id 고유성, citation_id 및 source_locator 존재 여부, 질의 실행 횟수 기록
def audit_candidate_merge(pairs, merged):
    """중복 제거 후에도 출처가 보존되고 호출 횟수 상한을 지키는지 검사합니다."""
    # BEGIN D27-03-A04
    # TODO D27-03-A04: 중복 제거 후에도 출처가 보존되고 호출 횟수 상한을 지키는지 검사합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 병합 문서 목록에서 chunk_id 리스트 추출
    ids = [d.metadata["chunk_id"] for d in merged]
    # 고유 ID 여부, 출처 메타데이터 보존 여부 및 질의 실행 횟수 반환
    return {
        "unique_ids": len(ids) == len(set(ids)),
        "source_preserved": all(
            d.metadata.get("citation_id") and d.metadata.get("source_locator")
            for d in merged
        ),
        "query_runs": len(pairs),
    }
    # raise NotImplementedError("D27-03-A04 미완성")
    # END D27-03-A04


"""
생성된 다중 질의 목록의 수량 상한·중복 여부를 검증하고, 후보 병합 이후 chunk_id 고유성과 출처 메타데이터(citation_id, source_locator) 보존 상태를 점검하도록 구현하였다.
이를 통해 다중 검색 과정에서의 중복 호출 과다와 출처 누락을 사전에 감지할 수 있는 품질 관리 체계를 갖추었다.
"""
