"""단계별 역할 분리: services/inspector.py / 독립 실행은 main.py."""

"""진단 단계별 핵심 근거 기록 및 케이스별 정책·단계 감사 로그 생성을 수행하는 서비스 모듈"""


# 단계 진단 근거 기록 함수
# - 진단 결과 단계명(stage)과 주요 판정 근거(ambiguous, gold_in_candidates, gold_in_context) 묶음 반환
def reason_for_stage(case, stage):
    """진단할 때 사용한 근거 3개를 기록합니다."""
    # BEGIN D27-01-A03
    # TODO D27-01-A03: 진단할 때 사용한 근거 3개를 기록합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 진단 단계 및 핵심 판정 근거 3종 딕셔너리 반환
    return {
        "reason": stage,
        "evidence": {
            "ambiguous": case["ambiguous"],
            "gold_in_candidates": case["gold_in_candidates"],
            "gold_in_context": case["gold_in_context"],
        },
    }
    # raise NotImplementedError("D27-01-A03 미완성")
    # END D27-01-A03


# 케이스 감사 로그 생성 함수
# - 케이스 ID, 정책 상태(authorized, current, ready), 진단 단계 정보를 통합 구성
def audit_case(case, row):
    """권한·버전·준비 상태를 실패 진단 로그에 포함합니다."""
    # BEGIN D27-01-A04
    # TODO D27-01-A04: 권한·버전·준비 상태를 실패 진단 로그에 포함합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 케이스 식별자, 정책 플래그 및 진단 단계 감사 레코드 반환
    return {
        "case_id": case["id"],
        "policy": {
            "authorized": case["authorized"],
            "current": case["current"],
            "ready": case["ready"],
        },
        "stage": row["stage"],
    }
    # raise NotImplementedError("D27-01-A04 미완성")
    # END D27-01-A04


"""
진단 단계별 판정 근거와 케이스의 권한·버전·인덱스 준비 상태를 구조화된 로그로 묶어 반환하도록 구현하였다.
이를 통해 파이프라인 실패 원인을 추적할 때 정책 제약 조건과 검색·컨텍스트 근거를 함께 확인할 수 있는 감사 체계를 마련하였다.
"""
