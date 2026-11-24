"""단계별 역할 분리: schemas/result.py / 독립 실행은 main.py."""

"""원 질문과 질의 재작성 결과를 분리 보존하는 레코드 스키마 모듈"""


# 재작성 결과 기록 함수
# - original_question을 덮어쓰지 않고 search_query, status, reason과 함께 별도 필드로 기록
def record_rewrite(original, result):
    """원래 질문을 검색 질문으로 덮어쓰지 않습니다."""
    # BEGIN D27-02-A02
    # TODO D27-02-A02: 원래 질문을 검색 질문으로 덮어쓰지 않습니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 원 질문, 재작성 검색 질의, 상태 및 사유를 담은 딕셔너리 반환
    return {
        "original_question": original,
        "search_query": result.search_query,
        "status": result.status,
        "reason": result.reason,
    }
    # raise NotImplementedError("D27-02-A02 미완성")
    # END D27-02-A02


"""
원래 질문(original_question)과 재작성된 검색 질의(search_query)를 분리 저장하여 
질의 변환 이력과 상태를 훼손 없이 추적할 수 있도록 구현하였다.
"""
