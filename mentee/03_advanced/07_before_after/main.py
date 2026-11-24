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

# 리포트 저장, 단계 러너, Top-k 비교, 통제 정책, 변화 해석 및 비교 감사 함수 임포트
# - save_report : 실행 결과 리포트 JSON 저장
from coursekit.io import save_report

# - STAGE_RUNNERS : 실습 번호별 실행기 매핑
from coursekit.workshops import STAGE_RUNNERS

# - compare_rankings : 재순위화 전·후 Top-2 골드 포함 비교
from metrics.topk import compare_rankings

# - check_conditions : 골드 분리 및 후보 집합 유지 통제 점검
from policies.control import check_conditions

# - interpret_change : Top-k 포함 변화 해석 요약
from reports.summary import interpret_change

# - audit_comparison : 비교 조건·시간·인과 단정 제한 감사
from services.audit import audit_comparison

"""Day27 실습 07(07_before_after)의 순위 비교·변화 해석·통제 정책 점검·비교 감사 연결 및 리포트 저장을 담당하는 진입 모듈"""


# 프로그램 진입 함수
# - --offline 옵션 파싱 및 STAGE_RUNNERS[7] 실행
# - 실행 모드별 리포트 JSON 저장 및 원문 대조 안내 메시지 출력
def main():
    # CLI 인자 파서 구성 및 --offline 플래그 파싱
    parser = argparse.ArgumentParser(description="Day27 실습 07 · 07_before_after")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.",
    )
    args = parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    # 비교·해석·통제·감사 함수 4종을 주입하여 7단계 러너 실행
    report = STAGE_RUNNERS[7](
        args.offline,
        [compare_rankings, interpret_change, check_conditions, audit_comparison],
    )
    # 실행 모드(--offline 여부)에 따른 파일명 구성 및 리포트 저장
    path = save_report(
        HERE, "day27_07_" + ("fixture" if args.offline else "live") + ".json", report
    )
    # 결과 리포트 경로 및 후속 원문 대조 안내 출력
    print("실습 07 결과:", path)
    print("보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.")


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
재순위화 전·후 Top-2 골드 비교(compare_rankings), 변화 해석(interpret_change), 평가 통제 점검(check_conditions), 
비교 감사(audit_comparison)를 Day27 7단계 러너에 통합하여 모드별 리포트를 생성하도록 구성하였다.
이를 통해 전·후 비교 실험의 지표 산출과 해석·통제 절차를 일관되게 연결하였다.
"""
