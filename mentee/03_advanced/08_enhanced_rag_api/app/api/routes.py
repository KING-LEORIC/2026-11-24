"""단계별 역할 분리: app/api/routes.py / 독립 실행은 main.py."""

"""HTTP 응답 상태 코드, 오류 상세 및 본문 source_ids와 sources citation_id 정합성을 점검하는 라우트 검증 모듈"""


# HTTP 응답 상태 및 출처 ID 일관성 검사 함수
# - status_code가 200이 아니면 http_ok=False 및 error_detail 반환
# - status_code가 200이면 sources의 citation_id 목록과 result.source_ids 일치 여부(citation_consistent) 반환
def check_http_response(response):
    """성공 응답의 source_ids와 실제 연결된 sources의 ID가 같은지 검사합니다."""
    # BEGIN D27-08-A03
    # TODO D27-08-A03: 성공 응답의 source_ids와 실제 연결된 sources의 ID가 같은지 검사합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 응답 JSON 본문 파싱
    body = response.json()
    # 비-200 HTTP 상태 코드 시 오류 정보 반환
    if response.status_code != 200:
        return {"http_ok": False, "error_detail": body.get("detail")}
    # 연결된 출처 객체들의 citation_id 목록 추출
    ids = [src["citation_id"] for src in body["sources"]]
    # 정상 응답 여부 및 출처 ID 목록 일치 여부 반환
    return {"http_ok": True, "citation_consistent": ids == body["result"]["source_ids"]}
    # raise NotImplementedError("D27-08-A03 미완성")
    # END D27-08-A03


"""
HTTP 응답 상태와 본문 출처 ID의 일관성을 검증하여 비정상 상태 코드 은폐를 방지하고, 
답변에 명시된 source_ids와 실제 첨부된 sources 객체 간 불일치를 감지하도록 구현하였다.
"""
