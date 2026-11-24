"""단계별 역할 분리: services/trace.py / 독립 실행은 main.py."""

"""트레이스 상의 원·검색 질의 존재 여부, ID 목록 타입 및 포함 ID의 후보 ID 부분집합 여부를 검증하는 모듈"""


# 파이프라인 트레이스 정합성 검증 함수
# - original_question 및 search_query 존재 여부 확인
# - candidate_ids, included_ids 리스트 타입 여부 및 included_ids ⊆ candidate_ids 여부 반환
def validate_trace(result):
    """원 질문·검색용 질문·후보·Context ID를 각각 확인합니다."""
    # BEGIN D27-06-A03
    # TODO D27-06-A03: 원 질문·검색용 질문·후보·Context ID를 각각 확인합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 실행 결과 내 trace 객체 참조
    t = result["trace"]
    # 질의 분리 기록, ID 리스트 형식 및 후보 집합 내 포함 여부 검증 결과 반환
    return {
        "questions_separate": bool(t["original_question"] and t["search_query"]),
        "ids_recorded": isinstance(t["candidate_ids"], list)
        and isinstance(t["included_ids"], list),
        "included_from_candidates": set(t["included_ids"]).issubset(t["candidate_ids"]),
    }
    # raise NotImplementedError("D27-06-A03 미완성")
    # END D27-06-A03


"""
원 질문과 검색용 질의의 기록 여부, 후보·포함 문서 ID 리스트의 자료형 정합성, 
그리고 최종 Context 포함 ID가 검색 후보 ID 집합 내에 속하는지 여부를 점검하도록 구현하였다.
"""
