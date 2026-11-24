"""단계별 역할 분리: services/audit.py / 독립 실행은 main.py."""

"""파이프라인 실행 모드, 계측 단계 목록, 출력 출처 ID 및 수동 원문 대조 필요성을 기록하는 감사 모듈"""


# 파이프라인 실행 감사 로그 생성 함수
# - source_mode, timing_ms 키 정렬 목록, 응답 sources의 citation_id 목록 및 수동 검토 플래그 반환
def audit_pipeline(result):
    """Stage 시간과 출처 연결을 기록하되 진위 판단은 별도로 수행합니다."""
    # BEGIN D27-06-A04
    # TODO D27-06-A04: Stage 시간과 출처 연결을 기록하되 진위 판단은 별도로 수행합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 실행 결과 내 trace 객체 참조
    t = result["trace"]
    # 실행 모드, 기록된 단계명 목록, 출력 출처 ID 및 수동 검토 필요 여부 반환
    return {
        "mode": t["source_mode"],
        "stage_times": sorted(t["timing_ms"]),
        "output_source_ids": [r["citation_id"] for r in result["sources"]],
        "manual_grounding_review": True,
    }
    # raise NotImplementedError("D27-06-A04 미완성")
    # END D27-06-A04


"""
파이프라인 실행 트레이스의 모드·계측 단계와 최종 출력 출처 ID를 수집하고, 
근거 진위 판정은 별도 수동 대조(manual_grounding_review=True)로 분리하여 감사 일관성을 유지하도록 구현하였다.
"""
