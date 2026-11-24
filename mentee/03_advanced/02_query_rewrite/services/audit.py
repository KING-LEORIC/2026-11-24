"""단계별 역할 분리: services/audit.py / 독립 실행은 main.py."""

"""질의 재작성 케이스의 이력 규모, 변환 여부 및 수동 검토 필요성을 기록하는 감사 서비스 모듈"""


# 재작성 감사 로그 생성 함수
# - 질문 ID, 대화 턴 수, 재작성 상태, 질의 변경 여부 및 사람 검토 필요 플래그 구성
def audit_rewrite(case, row):
    """원 질문·History 규모와 의미 대조 필요성을 남깁니다."""
    # BEGIN D27-02-A04
    # TODO D27-02-A04: 원 질문·History 규모와 의미 대조 필요성을 남깁니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 감사 지표(턴 수, 상태, 변경 여부, 수동 검토 플래그) 딕셔너리 반환
    return {
        "question_id": case["id"],
        "history_turns": len(case["history"]),
        "status": row["status"],
        "changed": row["original_question"] != row["search_query"],
        "human_review_needed": True,
    }
    # raise NotImplementedError("D27-02-A04 미완성")
    # END D27-02-A04


"""
질의 재작성 결과에 대해 대화 이력 길이와 원문 대비 변경 여부를 집계하고, 
의미 보존 여부에 대한 수동 검토 플래그를 남겨 후속 품질 감사의 기준을 마련하였다.
"""
