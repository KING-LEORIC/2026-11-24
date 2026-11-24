"""단계별 역할 분리: validation/constraints.py / 독립 실행은 main.py."""

"""재작성된 검색 질의에서 원 질문의 부정 표현과 숫자 조건 보존 여부를 점검하는 검증 모듈"""


# 부정 및 숫자 조건 보존 검증 함수
# - status가 'ready'일 때 부정 키워드 및 숫자 토큰 누락 여부 확인
# - 조건 훼손 감지 시 ValueError 발생, 통과 시 점검 결과 딕셔너리 반환
def check_semantics(original, result):
    """원 질문의 부정·숫자 조건을 임의로 변경하지 않았는지 점검합니다. 자동 검사만으로 의미 동일성을 보장하지 않습니다."""
    # BEGIN D27-02-A03
    # TODO D27-02-A03: 원 질문의 부정·숫자 조건을 임의로 변경하지 않았는지 점검합니다. 자동 검사만으로 의미 동일성을 보장하지 않습니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 부정 및 숫자 조건 보존 점검 상태 딕셔너리 초기화
    checks = {"negation_preserved": True, "number_preserved": True}
    # 상태가 'ready'가 아닌 경우 의미 조건 검사 생략 후 반환
    if result.status != "ready":
        return checks
    # 원 질문의 주요 부정 표현 검색 질의 내 유지 여부 확인
    for key in ("안 ", "않", "아니", "취소하지"):
        if key in original and key not in result.search_query:
            checks["negation_preserved"] = False
    # 정규표현식으로 원 질문 숫자 추출 및 검색 질의 포함 여부 확인
    # - re : 숫자 토큰 패턴 매칭
    import re

    numbers = re.findall(r"\d+", original)
    checks["number_preserved"] = all(value in result.search_query for value in numbers)
    # 부정 또는 숫자 조건 누락 시 ValueError 발생
    if not all(checks.values()):
        raise ValueError("Rewrite가 원 질문의 부정/숫자 조건을 변경했습니다.")
    # 점검 통과 결과 반환
    return checks
    # raise NotImplementedError("D27-02-A03 미완성")
    # END D27-02-A03


"""
질의 재작성 과정에서 핵심 제약 조건인 부정 표현과 숫자 토큰이 탈락·변형되는지 자동 점검하는 가드레일을 구현하였다.
자동 규칙 검사의 한계를 인지한 상태에서 조건 변경 시 즉시 예외를 발생시켜 잘못된 검색 질의 전파를 차단하도록 구성하였다.
"""
