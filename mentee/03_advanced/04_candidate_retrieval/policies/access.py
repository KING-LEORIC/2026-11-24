"""단계별 역할 분리: policies/access.py / 독립 실행은 main.py."""

"""검색 결과 후보 문서들의 인덱스 준비 여부, 유효 버전 여부 및 공개 접근 권한을 방어적으로 점검하는 정책 모듈"""


# 후보 문서 접근·상태 정책 점검 함수
# - 모든 후보 Document의 ready, is_current, access_level('public') 조건 충족 여부를 항목별 불리언으로 반환
def policy_check(docs, payload):
    """실제 권한 필터는 검색 SQL에서 적용합니다. 이 검사는 반환된 후보의 방어적 확인입니다."""
    # BEGIN D27-04-A04
    # TODO D27-04-A04: 실제 권한 필터는 검색 SQL에서 적용합니다. 이 검사는 반환된 후보의 방어적 확인입니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # ready, current, public 정책 준수 여부 딕셔너리 반환
    return {
        "ready": all(d.metadata.get("ready", True) is True for d in docs),
        "current": all(d.metadata.get("is_current", True) is True for d in docs),
        "public": all(
            d.metadata.get("access_level", "public") == "public" for d in docs
        ),
    }
    # raise NotImplementedError("D27-04-A04 미완성")
    # END D27-04-A04


"""
SQL 조회 단계에서 적용된 접근·버전 필터가 실제 반환 후보 문서들에서도 유지되었는지 
준비 상태(ready), 최신 유효 상태(is_current), 공개 등급(public) 기준으로 방어적 검증을 수행하도록 구현하였다.
"""
