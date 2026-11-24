"""단계별 역할 분리: metrics/topk.py / 독립 실행은 main.py."""

"""재순위화 전·후 문서 목록의 Top-2 골드(gold) 문서 포함 여부를 비교하는 평가 지표 모듈"""


# 재순위화 전·후 Top-2 골드 문서 포함 비교 함수
# - 고정 관련 문서(gold) 집합 기준 before/after 목록의 Top-2 포함 지표 산출을 compare_lists에 위임
def compare_rankings(before, after, gold):
    """고정한 관련 문서 ID를 Top-2에 포함했는지 확인합니다."""
    # BEGIN D27-07-A01
    # TODO D27-07-A01: 고정한 관련 문서 ID를 Top-2에 포함했는지 확인합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 평가 지표 비교 유틸리티(compare_lists) 호출 및 Top-2 비교 결과 반환
    from coursekit.evaluation import compare_lists

    return compare_lists(before, after, gold, k=2)
    # raise NotImplementedError("D27-07-A01 미완성")
    # END D27-07-A01


"""
재순위화 이전 목록과 이후 목록에서 사전에 고정된 골드 문서가 Top-2 내에 포함되는지 비교하도록 구현하였다.
이를 통해 순위 변동이 실제 상위 핵심 문서 도달 여부에 미치는 영향을 정량 지표로 산출할 수 있게 하였다.
"""
