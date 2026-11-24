"""단계별 역할 분리: app/services/rag_service.py / 독립 실행은 main.py."""

"""RAG 체인을 FastAPI 애플리케이션에 연결하면서 신뢰 역할을 서버에서 'learner'로 고정 지정하는 서비스 모듈"""


# FastAPI 앱 와이어링 함수
# - 클라이언트 요청의 role 값을 신뢰하지 않고 trusted_role="learner"로 create_app 호출
def wire_fastapi(chain):
    """API 요청의 role 문자열을 신뢰하지 않고 서버에서 learner 역할을 지정합니다."""
    # BEGIN D27-08-A02
    # TODO D27-08-A02: API 요청의 role 문자열을 신뢰하지 않고 서버에서 learner 역할을 지정합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # FastAPI 앱 팩토리(create_app) 임포트
    from coursekit.api import create_app

    # 서버 신뢰 역할('learner') 고정 적용 및 앱 인스턴스 반환
    return create_app(chain, trusted_role="learner")
    # raise NotImplementedError("D27-08-A02 미완성")
    # END D27-08-A02


"""
클라이언트 입력 role 문자열을 신뢰하지 않고 서버 측에서 trusted_role="learner"를 강제 지정하여 
FastAPI 앱을 생성하도록 구현함으로써 권한 위조 가능성을 차단하였다.
"""
