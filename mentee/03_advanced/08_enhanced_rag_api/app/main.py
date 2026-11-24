"""Uvicorn app factory. import만으로 GPU/DB/LLM을 호출하지 않습니다."""

# 파이썬 실행 환경 제어 및 경로 처리 기능 사용
# - sys : 모듈 검색 경로 등록
# - Path : 파일 및 디렉터리 경로 관리
import sys
from pathlib import Path

# 프로젝트 루트 디렉터리 계산 및 모듈 검색 경로 등록
# - ROOT : 현재 파일 기준 3단계 상위 디렉터리
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

"""모듈 임포트 시 자원 초기화를 유보하고 ASGI factory 호출 시점에 RAG FastAPI 앱을 조립하는 팩토리 모듈"""


# ASGI 앱 팩토리 함수
# - 호출 시점에 서비스 체인 생성 및 FastAPI 앱 와이어링 수행
def create_app_factory():
    """실제 GPU/DB/LLM 준비는 ASGI factory 호출 시에만 실행됩니다."""
    # 서비스 체인 생성기 및 FastAPI 와이어링 함수 임포트
    from app.retrieval.stages import make_service_chain
    from app.services.rag_service import wire_fastapi

    # 라이브 모드 체인을 연결한 FastAPI 앱 생성 및 반환
    return wire_fastapi(make_service_chain(offline=False))


"""
모듈 임포트 단계에서는 GPU·DB·LLM 초기화 코드를 실행하지 않고 create_app_factory 호출 시점에 
파이프라인과 FastAPI 앱을 조립하도록 구성하여 서버 기동 제어성과 부작용 차단을 확보하였다.
"""
