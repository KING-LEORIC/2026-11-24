# 실행 기록 (직접 작성)

- 선택 단계 / 실습: Day27 실습 05 · 05_cross_encoder_reranking (STAGE_RUNNERS[5], outputs\day27_05_live.json)
- 실행 날짜와 Python Interpreter: 2026-11-24 / 프로젝트 가상환경 Python
- 실행 모드: **live** (execution_mode: "live_e5_cuda_postgresql_crossencoder", day27_05_live.json 생성)
- 요청 질문과 Category: 요청 질문 "회의실 예약을 취소하는 방법은?" / Category 값 미기록 (FAC-* 청크 ID 기준 시설 관련 질의)
- Query Rewrite의 원 질문과 검색용 질문: 해당 없음 (05_cross_encoder_reranking 단계는 원 질문 "회의실 예약을 취소하는 방법은?"과 문서 본문 쌍(pairs)으로 재순위화를 수행하며 Query Rewrite 입·출력 필드는 미포함)
- Candidate ID → Rerank ID → Context included ID:
    - Candidate ID (before_ids, 5건): FAC-102-C1, FAC-107-C1, FAC-109-C1, FAC-103-C1, FAC-101-C1
    - Rerank ID (after_ids, 상위 3건, scores_finite: true, rank_sorted: true, same_candidate_pool: true, metadata_kept: true, pre_rank_recorded: true): FAC-102-C1 (0.9991612434387207), FAC-109-C1 (0.813144326210022), FAC-107-C1 (0.7214917540550232)
    - Context included ID: 해당 없음 (최종 컨텍스트 선별 ID 목록은 본 JSON에 미포함)
- 답변과 출처 문서의 실제 내용 대조: 최종 생성 답변은 미포함이나, pairs에 기록된 문서 본문 기준 첫 번째 쌍은 *"예약 시스템의 나의 예약 메뉴에서 취소를 선택합니다. 시작 2시간 전까지 취소할 수 있습니다."*로 취소 방법과 기한 조건을 직접 다루고, 두 번째 쌍은 열쇠 수령·반납 안내와 함께 *"예약 취소 규정은 별도 문서를 참조합니다."*로 별도 문서 참조를 안내함
- 실패 또는 예상과 다른 결과: after_ids에서 FAC-109-C1이 FAC-107-C1보다 높은 순위(0.8131 vs 0.7215)로 올라갔으나, note에 *"고정 점수는 실제 CrossEncoder 모델 점수가 아닙니다."*라고 명시되어 있어 실제 CrossEncoder 스코어러 실측 점수가 아님
- 고친 TODO와 이유: D27-05-A01~D27-05-A04 구현 — create_pairs로 (질문, 문서본문) 쌍 생성, rank_documents로 top_n=3 재정렬, check_rank_scores로 점수 유한성(math.isfinite) 및 내림차순 정렬 점검, audit_ranking으로 후보 풀 동일성·출처 메타데이터·이전 순위(pre_rank) 보존 감사를 수행하기 위함
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): 고정 점수 경로 대신 실제 CrossEncoder 모델을 연결해 rerank_scores를 산출하면 취소 절차 본문과 별도 문서 참조 청크 간 관련도 점수 격차가 달라져 상위 top_n 순위 결정이 실제 모델 판단 기준으로 정렬될 수 있을 것으로 기대되나, 실측 적용 전까지 효과를 단정할 수 없음
