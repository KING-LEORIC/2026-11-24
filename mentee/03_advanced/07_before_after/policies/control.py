"""단계별 역할 분리: policies/control.py / 독립 실행은 main.py."""

"""평가 시점 골드 라벨 분리 여부 및 재순위화 후 문서의 기존 후보 집합 소속 여부를 점검하는 통제 정책 모듈"""


# 평가 조건 통제 점검 함수
# - 질문 ID와 카테고리 기록
# - before 후보 문서 메타데이터에 gold 누출이 없는지(gold_separate) 및 ranked가 before 부분집합인지(same_candidates) 확인
def check_conditions(case, before, ranked):
    """Gold Label은 검색과 Reranker의 입력이 아니라 평가할 때만 사용합니다."""
    # BEGIN D27-07-A03
    # TODO D27-07-A03: Gold Label은 검색과 Reranker의 입력이 아니라 평가할 때만 사용합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 질문 식별자, 카테고리, 골드 분리 여부 및 후보 집합 유지 여부 반환
    return {
        "question_id": case["id"],
        "category": case["category"],
        "gold_separate": all("gold" not in d.metadata for d in before),
        "same_candidates": set(d.metadata["chunk_id"] for d in ranked).issubset(
            set(d.metadata["chunk_id"] for d in before)
        ),
    }
    # raise NotImplementedError("D27-07-A03 미완성")
    # END D27-07-A03


"""
검색·재순위화 단계에서 골드 라벨이 문서 메타데이터에 섞이지 않았는지(gold_separate)와 
재순위화 결과가 기존 후보 집합 내에 머물렀는지(same_candidates)를 점검하도록 구현하였다.
이를 통해 평가 데이터 유출을 방지하고 전·후 비교 실험의 공정성을 확보하였다.
"""
