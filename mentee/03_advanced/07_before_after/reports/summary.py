"""단계별 역할 분리: reports/summary.py / 독립 실행은 main.py."""

"""재순위화 전·후 Top-k 골드 포함 여부의 변화 양상을 해석 문구로 요약하는 리포트 모듈"""


# 전·후 골드 포함 변화 해석 함수
# - before_contains_gold가 None이면 수동 검토 안내 반환
# - before와 after 포함 여부가 같으면 변화 없음 문구, 다르면 추가 검증 필요 문구 반환
def interpret_change(report):
    """순위가 바뀌어도 반드시 개선됐다는 결론을 내리지 않습니다."""
    # BEGIN D27-07-A02
    # TODO D27-07-A02: 순위가 바뀌어도 반드시 개선됐다는 결론을 내리지 않습니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 재순위화 전·후 골드 포함 여부 값 추출
    before = report["before_contains_gold"]
    after = report["after_contains_gold"]
    # 골드 라벨 부재 시 수동 검토 필요 문구 반환
    if before is None:
        return "gold 없음: 인간 검토 필요"
    # 전·후 포함 상태 동일 시 변화 없음 문구 반환
    if before == after:
        return "Top-k 관련 문서 포함 여부는 변하지 않음"
    # 전·후 포함 상태 변동 시 추가 검증 필요 문구 반환
    return "관련 문서 Top-k 포함 여부가 달라짐 (추가 검증 필요)"
    # raise NotImplementedError("D27-07-A02 미완성")
    # END D27-07-A02


"""
재순위화 전·후의 Top-k 골드 문서 포함 여부에 따라 골드 부재, 상태 유지, 상태 변동의 세 가지 해석을 구분하도록 구현하였다.
단순 순위 이동이나 포함 여부 변화만으로 성능 개선을 섣불리 단정하지 않고 추가 검증·인간 검토를 유도하도록 구성하였다.
"""
