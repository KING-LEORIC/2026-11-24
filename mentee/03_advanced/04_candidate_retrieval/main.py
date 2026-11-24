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

# 리포트 저장, 단계 러너, 접근·메타데이터 정책 및 검색 어댑터 함수 임포트
# - save_report : 실행 결과 리포트 JSON 저장
from coursekit.io import save_report

# - STAGE_RUNNERS : 실습 번호별 실행기 매핑
from coursekit.workshops import STAGE_RUNNERS

# - policy_check : 후보 문서 준비·버전·공개 정책 점검
from policies.access import policy_check

# - metadata_check : 후보 문서 메타데이터 및 카테고리 검증
from policies.metadata import metadata_check

# - fetch_documents, make_candidate_request : 검색 요청 생성 및 후보 문서 조회
from retrieval.adapter import fetch_documents, make_candidate_request

"""Day27 실습 04(04_candidate_retrieval)의 검색 요청 구성·후보 조회·메타데이터/정책 검증 연결 및 리포트 저장을 담당하는 진입 모듈"""


# 프로그램 진입 함수
# - --offline 옵션 파싱 및 STAGE_RUNNERS[4] 실행
# - 모드별 리포트 JSON 저장 및 원문 대조 안내 메시지 출력
def main():
    # CLI 인자 파서 구성 및 --offline 플래그 파싱
    parser = argparse.ArgumentParser(
        description="Day27 실습 04 · 04_candidate_retrieval"
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.",
    )
    args = parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    # 요청 구성·문서 조회·메타데이터 검증·정책 점검 함수 4종을 주입하여 4단계 러너 실행
    report = STAGE_RUNNERS[4](
        args.offline,
        [make_candidate_request, fetch_documents, metadata_check, policy_check],
    )
    # 실행 모드(--offline 여부)에 따른 파일명 구성 및 리포트 저장
    path = save_report(
        HERE, "day27_04_" + ("fixture" if args.offline else "live") + ".json", report
    )
    # 결과 리포트 경로 및 후속 원문 대조 안내 출력
    print("실습 04 결과:", path)
    print("보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.")


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
후보 검색 요청 생성(make_candidate_request), 후보 문서 조회 및 상한 검증(fetch_documents), 
메타데이터 검증(metadata_check), 정책 점검(policy_check)을 Day27 4단계 러너에 통합하여 실행 리포트를 생성하도록 구성하였다.
이를 통해 후보 검색 단계의 입·출력 규약과 방어적 검증 절차를 체계적으로 연결하였다.
"""
