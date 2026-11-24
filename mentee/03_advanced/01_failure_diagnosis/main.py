"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""

# 파일 경로 처리 기능 사용
# - Path : 파일 및 디렉터리 경로 관리
# 파이썬 실행 환경 제어 기능 사용
# - sys : 모듈 검색 경로 등록
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

# - save_report : 실행 결과 리포트 JSON 저장
from coursekit.io import save_report

# 워크숍 단계 실행기 및 리포트 저장 유틸리티 사용
# - STAGE_RUNNERS : 실습 번호별 실행기 매핑
from coursekit.workshops import STAGE_RUNNERS

# 진단 정책 및 검사 서비스 함수 임포트
# - diagnose_stage : 파이프라인 장애 단계 진단
# - recommend_action : 진단 단계별 개선 조치 추천
from policies.diagnosis import diagnose_stage, recommend_action

# - reason_for_stage : 진단 단계 판정 근거 기록
# - audit_case : 케이스별 정책 및 단계 감사 로그 생성
from services.inspector import audit_case, reason_for_stage

"""Day27 실습 01(01_failure_diagnosis)의 진단 정책·감사 서비스 함수 연결, 실행 모드 처리 및 결과 리포트 저장을 담당하는 진입 모듈"""


# 프로그램 진입 함수
# - --offline 옵션 파싱 및 STAGE_RUNNERS[1] 실행
# - 모드별 리포트 파일 저장 및 검토 안내 메시지 출력
def main():
    # CLI 인자 파서 구성 및 --offline 플래그 파싱
    parser = argparse.ArgumentParser(description="Day27 실습 01 · 01_failure_diagnosis")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.",
    )
    args = parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    # - 진단 함수 4종을 주입하여 1단계 러너 실행
    report = STAGE_RUNNERS[1](
        args.offline, [diagnose_stage, recommend_action, reason_for_stage, audit_case]
    )
    # 실행 모드(--offline 여부)에 따른 파일명 구성 및 리포트 저장
    path = save_report(
        HERE, "day27_01_" + ("fixture" if args.offline else "live") + ".json", report
    )
    # 생성된 리포트 경로 및 후속 검토 안내 출력
    print("실습 01 결과:", path)
    print("보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.")


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
파이프라인 실패 진단 정책(diagnose_stage, recommend_action)과 감사 서비스(reason_for_stage, audit_case)를 
Day27 1단계 러너에 통합하여 실행 모드별 리포트를 생성하도록 구성하였다.
이를 통해 진단 로직과 실행 진입점의 책임을 분리하고, 실행 결과의 재현성과 후속 검토 추적성을 확보하였다.
"""
