"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""

# 파이썬 실행 환경 제어 및 경로 처리 기능 사용
# - sys : 모듈 검색 경로 등록
# - Path : 파일 및 디렉터리 경로 관리
import sys
from pathlib import Path

# 현재 스크립트 경로 및 coursekit 포함 역할 루트 경로 탐색
# - ROLE_ROOT : 상위 경로 중 coursekit 디렉터리가 존재하는 루트 탐색
# - sys.path에 추가하여 실행 위치와 무관하게 역할 모듈 임포트 지원
HERE = Path(__file__).resolve().parent
ROLE_ROOT = next(p for p in HERE.parents if (p / "coursekit").is_dir())
sys.path.insert(0, str(ROLE_ROOT))

# 명령행 인자 파싱 기능 사용
# - argparse : --offline 플래그 등 CLI 옵션 처리
import argparse

# 라우트 검증, 체인 생성, HTTP 감사, FastAPI 연결, 리포트 저장 및 단계 러너 임포트
# - check_http_response : HTTP 상태 및 출처 ID 일관성 검사
from app.api.routes import check_http_response

# - make_service_chain : RAG 서비스 체인 생성
from app.retrieval.stages import make_service_chain

# - audit_http_response : HTTP 응답·트레이스·정책 역할 감사
from app.services.audit import audit_http_response

# - wire_fastapi : 신뢰 역할 고정 FastAPI 앱 구성
from app.services.rag_service import wire_fastapi

# - save_report : 실행 결과 리포트 JSON 저장
from coursekit.io import save_report

# - STAGE_RUNNERS : 실습 번호별 실행기 매핑
from coursekit.workshops import STAGE_RUNNERS

"""Day27 실습 08(08_enhanced_rag_api)의 체인 구성·FastAPI 연결·응답 검증·감사 수행 및 리포트 저장을 담당하는 진입 모듈"""


# 프로그램 진입 함수
# - --offline 옵션 파싱 및 STAGE_RUNNERS[8] 실행
# - 실행 모드별 리포트 JSON 저장 및 원문 대조 안내 메시지 출력
def main():
    # CLI 인자 파서 구성 및 --offline 플래그 파싱
    parser = argparse.ArgumentParser(description="Day27 실습 08 · 08_enhanced_rag_api")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.",
    )
    args = parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    # 체인 생성·FastAPI 연결·HTTP 응답 검사·감사 함수 4종을 주입하여 8단계 러너 실행
    report = STAGE_RUNNERS[8](
        args.offline,
        [make_service_chain, wire_fastapi, check_http_response, audit_http_response],
    )
    # 실행 모드(--offline 여부)에 따른 파일명 구성 및 리포트 저장
    path = save_report(
        HERE, "day27_08_" + ("fixture" if args.offline else "live") + ".json", report
    )
    # 결과 리포트 경로 및 후속 원문 대조 안내 출력
    print("실습 08 결과:", path)
    print("보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.")


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
서비스 체인 생성(make_service_chain), FastAPI 와이어링(wire_fastapi), HTTP 응답 검증(check_http_response), 
HTTP 감사(audit_http_response)를 Day27 8단계 러너에 통합하여 모드별 리포트를 생성하도록 구성하였다.
이를 통해 RAG 파이프라인의 API 계층 노출과 권한·응답 정합성 검증을 일관되게 연결하였다.
"""
