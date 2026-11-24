"""단계별 역할 분리: app/services/audit.py / 독립 실행은 main.py."""

"""HTTP 응답 상태 코드, 요청 질의, 실행 모드, 트레이스 단계 목록 및 서버 정책 역할을 기록하는 감사 모듈"""


# HTTP 응답 감사 로그 생성 함수
# - 응답 JSON 및 trace에서 상태 코드, 질의, 실행 모드, 단계 목록 추출
# - 오류를 정보 부족 응답으로 감추지 않으며 policy_role을 "server_learner"로 기록
def audit_http_response(payload, response):
    """HTTP 오류를 정보 부족 응답으로 숨기지 않고 Stage·모드·상태를 기록합니다."""
    # BEGIN D27-08-A04
    # TODO D27-08-A04: HTTP 오류를 정보 부족 응답으로 숨기지 않고 Stage·모드·상태를 기록합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 응답 JSON 본문 및 trace 객체 추출
    body = response.json()
    trace = body.get("trace", {})
    # 상태 코드, 질의, 실행 모드, 실행 단계 및 서버 지정 정책 역할 반환
    return {
        "status_code": response.status_code,
        "query": payload["query"],
        "execution_mode": trace.get("source_mode", "error"),
        "stages": list(trace.get("timing_ms", {})),
        "policy_role": "server_learner",
    }
    # raise NotImplementedError("D27-08-A04 미완성")
    # END D27-08-A04


"""
HTTP 상태 코드와 트레이스 단계·모드 정보를 그대로 남겨 오류를 일반 정보 부족 응답으로 은폐하지 않고, 
서버가 부여한 정책 역할("server_learner")과 함께 감사 기록으로 남기도록 구현하였다.
"""
