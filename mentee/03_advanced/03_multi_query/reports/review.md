# 실행 기록 (직접 작성)

- 선택 단계 / 실습: Day27 실습 03 · 03_multi_query (STAGE_RUNNERS[3], day27_03_live.json)
- 실행 날짜와 Python Interpreter: 2026-11-24 / 프로젝트 가상환경 Python
- 실행 모드: **live** (execution_mode: "live_e5_cuda_postgresql", day27_03_live.json 생성)
- 요청 질문과 Category: 기준 질의 "회의실 예약을 취소하는 방법은?" 및 확장 질의 "회의실 예약 취소 방법", "예약한 회의실을 취소하려면 어떻게 하나요?" (count: 3, unique: true, within_limit: true) / Category 값 미기록 (FAC-* 청크 ID 기준 시설 관련 질의)
- Query Rewrite의 원 질문과 검색용 질문:해당 없음 (03_multi_query 단계는 plan_queries로 다중 검색 질의 3개를 생성하며 별도 Query Rewrite 스키마·상태 필드는 미포함; 첫 번째 질의 "회의실 예약을 취소하는 방법은?"은 UndefinedTable 오류로 실패했고 나머지 2개 질의가 검색에 실행됨)
- Candidate ID → Rerank ID → Context included ID:
    - 질의 1 ("회의실 예약을 취소하는 방법은?"): UndefinedTable 오류로 후보 미수집
    - 질의 2 ("회의실 예약 취소 방법"): FAC-102-C1, FAC-109-C1, FAC-103-C1, FAC-107-C1, FAC-101-C1
    - 질의 3 ("예약한 회의실을 취소하려면 어떻게 하나요?"): FAC-102-C1, FAC-107-C1, FAC-103-C1, FAC-109-C1, FAC-101-C1
    - 병합 후 (merged_ids, unique_ids: true, source_preserved: true, query_runs: 2): FAC-102-C1, FAC-109-C1, FAC-103-C1, FAC-107-C1, FAC-101-C1 (Rerank ID 및 Context included ID는 본 단계 출력에 미포함)
- 답변과 출처 문서의 실제 내용 대조: 해당 없음 (최종 생성 답변 및 청크 원문 본문 미포함; 병합된 5개 청크 모두 두 정상 실행 질의에서 found_by_query로 수집됨)
- 실패 또는 예상과 다른 결과: 첫 번째 질의 "회의실 예약을 취소하는 방법은?" 실행 시 UndefinedTable 오류가 발생해 정상 검색 질의가 2건(query_runs: 2)만 수행됨; 두 질의에서 FAC-102-C1과 FAC-101-C1의 순위는 동일했으나 FAC-109-C1과 FAC-107-C1의 세부 순위가 서로 다름
- 고친 TODO와 이유: D27-03-A01~D27-03-A04 구현 — plan_queries로 최대 3개 고유 질의 구성, merge_candidates로 chunk_id 중복 제거 및 found_by_query 기록, check_query_list로 개수·고유성·상한 점검, audit_candidate_merge로 병합 후 ID 고유성·출처 보존·실행 횟수 감사를 수행하기 위함
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): PostgreSQL 측 UndefinedTable 오류 원인을 해소하고 첫 번째 질의까지 정상 수행되도록 복구하면 전체 3개 질의가 검색에 참여해 누락 후보나 순위 편차를 더 안정적으로 포착할 수 있을 것으로 기대되나, DB 스키마·테이블 상태 점검 및 실측 재실행 전까지 개선 효과를 단정할 수 없음
