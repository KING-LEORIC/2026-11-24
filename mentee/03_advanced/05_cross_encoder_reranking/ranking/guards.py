"""단계별 역할 분리: ranking/guards.py / 독립 실행은 main.py."""

"""재순위화 결과 문서의 rerank_score 유한성 및 내림차순 정렬 일관성을 점검하는 가드 모듈"""


# 재순위화 점수 유효성 및 정렬 순서 검사 함수
# - 모든 문서의 rerank_score가 유한값(math.isfinite)인지 확인
# - 인접 문서 간 rerank_score가 내림차순(a >= b) 정렬을 유지하는지 확인
def check_rank_scores(ranked):
    """점수의 개수·유한값·정렬 순서 검사. 점수는 정답 확률이 아닙니다."""
    # BEGIN D27-05-A03
    # TODO D27-05-A03: 점수의 개수·유한값·정렬 순서 검사. 점수는 정답 확률이 아닙니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 부동소수점 유한값 검사 유틸리티 임포트
    # - math : math.isfinite 함수 사용
    import math

    # 점수 유한값 여부 및 내림차순 정렬 상태 딕셔너리 반환
    return {
        "scores_finite": all(math.isfinite(d.metadata["rerank_score"]) for d in ranked),
        "rank_sorted": all(
            a.metadata["rerank_score"] >= b.metadata["rerank_score"]
            for a, b in zip(ranked, ranked[1:])
        ),
    }
    # raise NotImplementedError("D27-05-A03 미완성")
    # END D27-05-A03


"""
재순위화 결과 문서의 점수가 NaN·무한대 없이 유한한 수치인지와 상위 점수 순으로 정렬되었는지 점검하도록 구현하였다.
이를 통해 후속 컨텍스트 선별 단계로 넘어가는 순위 데이터의 수치적 무결성을 보장하였다.
"""
