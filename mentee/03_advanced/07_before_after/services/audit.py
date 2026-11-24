"""단계별 역할 분리: services/audit.py / 독립 실행은 main.py."""

"""전·후 비교 실행 모드, 검색·재순위화 소요 시간 비음수 여부 및 반복 검증·인과 단정 제한 플래그를 기록하는 감사 모듈"""


# 전·후 비교 감사 로그 생성 함수
# - 실행 모드, search_ms 및 rerank_ms의 0 이상 여부 확인
# - 반복 측정 필요(repeat_needed=True) 및 단일 사례 인과 개선 주장 불가(causal_improvement_claim=False) 기록
def audit_comparison(row, offline):
    """시간·실행모드·비교 조건을 기록하고 단일 사례로 성능 개선을 단정하지 않습니다."""
    # BEGIN D27-07-A04
    # TODO D27-07-A04: 시간·실행모드·비교 조건을 기록하고 단일 사례로 성능 개선을 단정하지 않습니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 실행 모드, 소요 시간 비음수 여부 및 반복 측정·인과 단정 제한 플래그 반환
    return {
        "mode": "offline_fixture" if offline else "live",
        "timing_nonnegative": row["search_ms"] >= 0 and row["rerank_ms"] >= 0,
        "repeat_needed": True,
        "causal_improvement_claim": False,
    }
    # raise NotImplementedError("D27-07-A04 미완성")
    # END D27-07-A04


"""
전·후 비교 결과의 실행 모드와 검색·재순위화 소요 시간의 유효성을 기록하고, 
단일 사례 기반의 인과적 성능 개선 단정을 배제하며 반복 측정 필요성을 명시하도록 구현하였다.
이를 통해 실험 결과 해석의 과잉 일반화를 방지하고 검증 신뢰도를 높였다.
"""
