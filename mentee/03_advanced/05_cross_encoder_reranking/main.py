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

# 리포트 저장, 단계 러너, 점수 검증, 쌍 생성, 재순위화 및 감사 함수 임포트
# - save_report : 실행 결과 리포트 JSON 저장
from coursekit.io import save_report

# - STAGE_RUNNERS : 실습 번호별 실행기 매핑
from coursekit.workshops import STAGE_RUNNERS

# - check_rank_scores : 재순위화 점수 유한성 및 정렬 검사
from ranking.guards import check_rank_scores

# - create_pairs : (질문, 문서본문) 입력 쌍 생성
from ranking.pairs import create_pairs

# - rank_documents : 후보 문서 재정렬 및 상위 선별
from ranking.reranker import rank_documents

# - audit_ranking : 후보 풀 유지·출처 보존·이전 순위 기록 감사
from services.audit import audit_ranking

"""Day27 실습 05(05_cross_encoder_reranking)의 입력 쌍 생성·재순위화·점수 검증·결과 감사 연결 및 리포트 저장을 담당하는 진입 모듈"""


# 프로그램 진입 함수
# - --offline 옵션 파싱 및 STAGE_RUNNERS[5] 실행
# - 실행 모드별 리포트 JSON 저장 및 원문 대조 안내 메시지 출력
def main():
    # CLI 인자 파서 구성 및 --offline 플래그 파싱
    parser = argparse.ArgumentParser(
        description="Day27 실습 05 · 05_cross_encoder_reranking"
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.",
    )
    args = parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    # 쌍 생성·재순위화·점수 검증·결과 감사 함수 4종을 주입하여 5단계 러너 실행
    report = STAGE_RUNNERS[5](
        args.offline, [create_pairs, rank_documents, check_rank_scores, audit_ranking]
    )
    # 실행 모드(--offline 여부)에 따른 파일명 구성 및 리포트 저장
    path = save_report(
        HERE, "day27_05_" + ("fixture" if args.offline else "live") + ".json", report
    )
    # 결과 리포트 경로 및 후속 원문 대조 안내 출력
    print("실습 05 결과:", path)
    print("보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.")


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
CrossEncoder 입력 쌍 생성(create_pairs), 후보 재순위화(rank_documents), 점수 유한성·정렬 검증(check_rank_scores), 
후보 풀·출처·이전 순위 감사(audit_ranking)를 Day27 5단계 러너에 통합하여 모드별 리포트를 생성하도록 구성하였다.
이를 통해 재순위화 단계의 입·출력 규약과 수치·메타데이터 무결성 검증 체계를 일관되게 연결하였다.
"""
