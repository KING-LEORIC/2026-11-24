"""단계별 역할 분리: policies/diagnosis.py / 독립 실행은 main.py."""

"""RAG 파이프라인 단계별 이상 징후 진단 및 단계별 개선 조치 추천을 수행하는 정책 모듈"""


# 파이프라인 장애 단계 진단 함수
# - 권한, 버전, 인덱스 준비 상태, 질의 모호성, 검색·재순위 포함 여부, 출처 유효성을 순차 검사
# - 가장 먼저 감지된 문제 단계 식별자 반환, 이상 없으면 'healthy' 반환
def diagnose_stage(case):
    """어떤 문제가 먼저 발생했는지 위에서부터 조건을 검사합니다."""
    # BEGIN D27-01-A01
    # TODO D27-01-A01: 어떤 문제가 먼저 발생했는지 위에서부터 조건을 검사합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 접근 권한 미충족 여부 확인
    if not case["authorized"]:
        return "authorization_filter"
    # 현재 유효 문서 버전 여부 확인
    if not case["current"]:
        return "version_filter"
    # 인덱스 공개·준비 완료 여부 확인
    if not case["ready"]:
        return "index_not_ready"
    # 질의 모호성 존재 여부 확인
    if case["ambiguous"]:
        return "rewrite"
    # 검색 후보군 내 정답(gold) 포함 여부 확인
    if not case["gold_in_candidates"]:
        return "retrieval"
    # 최종 Context 내 정답(gold) 포함 여부 확인
    if not case["gold_in_context"]:
        return "reranking"
    # 생성 응답 출처 유효성 명시적 실패 여부 확인
    if case["valid_source"] is False:
        return "validation"
    # 모든 단계 조건 통과 시 정상 상태 반환
    return "healthy"
    # raise NotImplementedError("D27-01-A01 미완성")
    # END D27-01-A01


# 진단 단계별 개선 조치 반환 함수
# - 각 파이프라인 단계에 대응하는 조치 가이드 문자열 조회
def recommend_action(stage):
    """문제 단계에 맞는 개선 방법을 반환합니다. Reranker는 누락된 후보를 새로 찾지 않습니다."""
    # BEGIN D27-01-A02
    # TODO D27-01-A02: 문제 단계에 맞는 개선 방법을 반환합니다. Reranker는 누락된 후보를 새로 찾지 않습니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 단계별 권고 조치 매핑 조회 및 반환
    return {
        "authorization_filter": "서버에서 접근 권한을 검사합니다.",
        "version_filter": "현재 유효한 문서만 검색합니다.",
        "index_not_ready": "Indexing 공개 상태를 확인합니다.",
        "rewrite": "History에서 명확한 대상만 복원합니다.",
        "retrieval": "검색 대상·필터·Top-k를 점검합니다.",
        "reranking": "후보 문서의 관련성 순위를 다시 평가합니다.",
        "validation": "답변과 실제 근거를 대조합니다.",
        "healthy": "정상 흐름을 유지합니다.",
    }[stage]
    # raise NotImplementedError("D27-01-A02 미완성")
    # END D27-01-A02


"""
파이프라인 선행 조건(권한·버전·인덱스)부터 질의 재작성, 검색, 재순위화, 검증까지 우선순위 기반의 단계 진단을 구현하였다.
각 실패 지점에 적합한 개선 조치를 매핑하여 문제 원인의 조기 격리와 후속 디버깅 방향 설정의 명확성을 확보하였다.
"""
