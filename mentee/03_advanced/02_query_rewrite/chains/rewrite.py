"""단계별 역할 분리: chains/rewrite.py / 독립 실행은 main.py."""

"""대화 이력(history)과 원 질문을 반영해 검색용 질의를 재작성하는 체인 모듈"""


# 질의 재작성 실행 함수
# - offline 모드에 따라 고정 예시 또는 실제 프롬프트·Chat Model 경로로 rewrite_query 호출
def apply_rewrite(question, history, offline):
    """offline이면 고정 예시, 기본 실행이면 실제 ChatPromptTemplate → Chat Model을 호출합니다."""
    # BEGIN D27-02-A01
    # TODO D27-02-A01: offline이면 고정 예시, 기본 실행이면 실제 ChatPromptTemplate → Chat Model을 호출합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # coursekit 질의 재작성 함수 호출 및 결과 반환
    from coursekit.rewrite import rewrite_query

    return rewrite_query(question, history, offline=offline)
    # raise NotImplementedError("D27-02-A01 미완성")
    # END D27-02-A01


"""
오프라인 고정 예시와 실제 프롬프트-Chat Model 호출을 추상화된 rewrite_query 계층으로 위임하여 
질의 재작성 체인의 실행 모드를 일관되게 제어하도록 구성하였다.
"""
