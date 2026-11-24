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

# 재작성 체인, 리포트 저장, 단계 러너, 스키마, 감사 및 의미 검증 함수 임포트
# - apply_rewrite : 질의 재작성 실행
from chains.rewrite import apply_rewrite

# - save_report : 실행 결과 리포트 JSON 저장
from coursekit.io import save_report

# - STAGE_RUNNERS : 실습 번호별 실행기 매핑
from coursekit.workshops import STAGE_RUNNERS

# - record_rewrite : 원 질문·재작성 질의 결과 기록
from schemas.result import record_rewrite

# - audit_rewrite : 재작성 케이스 감사 로그 생성
from services.audit import audit_rewrite

# - check_semantics : 부정·숫자 조건 보존 검증
from validation.constraints import check_semantics

"""Day27 실습 02(02_query_rewrite)의 재작성 체인·기록 스키마·의미 검증·감사 서비스 연결 및 리포트 저장을 담당하는 진입 모듈"""


# 프로그램 진입 함수
# - --offline 옵션 파싱 및 STAGE_RUNNERS[2] 실행
# - 모드별 리포트 JSON 저장 및 원문 대조 안내 출력
def main():
    # CLI 인자 파서 구성 및 --offline 플래그 파싱
    parser = argparse.ArgumentParser(description="Day27 실습 02 · 02_query_rewrite")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.",
    )
    args = parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    # - 재작성·기록·검증·감사 함수 4종을 주입하여 2단계 러너 실행
    report = STAGE_RUNNERS[2](
        args.offline, [apply_rewrite, record_rewrite, check_semantics, audit_rewrite]
    )
    # 실행 모드(--offline 여부)에 따른 파일명 구성 및 리포트 저장
    path = save_report(
        HERE, "day27_02_" + ("fixture" if args.offline else "live") + ".json", report
    )
    # 결과 경로 및 수동 검토 안내 메시지 출력
    print("실습 02 결과:", path)
    print("보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.")


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
질의 재작성 실행, 원 질문 보존 기록, 부정·숫자 의미 검증 및 감사 로깅을 Day27 2단계 러너에 통합하여 
모드별 실행 결과를 일관되게 산출하도록 구성하였다.
이를 통해 각 모듈의 역할을 명확히 분리하고, 재작성 품질의 자동 검증과 수동 원문 대조 연계를 확보하였다.
"""
