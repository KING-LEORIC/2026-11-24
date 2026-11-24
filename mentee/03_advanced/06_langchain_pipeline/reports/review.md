# 실행 기록 (직접 작성)

- 선택 단계 / 실습: Day27 실습 06 · 06_langchain_pipeline (STAGE_RUNNERS[6], outputs/day27_06_live.json)
- 실행 날짜와 Python Interpreter: 2026-11-24 / 프로젝트 가상환경 Python
- 실행 모드: **live** (execution_mode: "live_e5_cuda_postgresql_llm", source_mode: "live", day27_06_live.json 생성)
- 요청 질문과 Category: 요청 질문 "그럼 취소는 어떻게 해?" / Category: "시설" (candidate_k: 5, context_k: 2, use_rewrite: true, use_multiquery: false, use_rerank: true)
- Query Rewrite의 원 질문과 검색용 질문: 원 질문 "그럼 취소는 어떻게 해?" → 검색용 질문 "회의실 예약을 어떻게 취소하나요?" (queries: ["회의실 예약을 어떻게 취소하나요?"], query_count: 1, questions_separate: true)
- Candidate ID → Rerank ID → Context included ID:
    - Candidate ID (5건): FAC-102-C1, FAC-107-C1, FAC-103-C1, FAC-109-C1, FAC-108-C1
    - Rerank ID (5건): FAC-102-C1, FAC-109-C1, FAC-107-C1, FAC-103-C1, FAC-108-C1
    - Context included ID (2건, included_from_candidates: true): FAC-102-C1, FAC-109-C1 (최종 인용 출처 source_ids: [2] → citation_id: 2, FAC-102-C1, guides/fac-102.md#section-1, 2026-11-v2)
- 답변과 출처 문서의 실제 내용 대조: 답변 *"예약 시스템의 ‘나의 예약’ 메뉴에서 취소를 선택하면 됩니다. 예약 시작 2시간 전까지 취소할 수 있습니다."*는 인용 출처 guides/fac-102.md#section-1 (FAC-102-C1) 및 앞선 실습(05)에서 확인된 예약 취소 절차·2시간 전 기한 내용과 부합하며, manual_grounding_review: true로 원문 대조 대상임
- 실패 또는 예상과 다른 결과: 특이 오류 없이 status: "answered"로 완료되었으나, 전체 단계 소요 시간(timing_ms 합계 약 9,645.258ms) 중 rerank가 5161.703ms(약 53.5%), rewrite가 2269.49ms(약 23.5%), generation이 1594.871ms(약 16.5%)로 대부분을 차지함; 또한 included_ids에 FAC-109-C1이 함께 포함되었으나 실제 인용은 citation_id: 2 (FAC-102-C1) 단일 출처만 사용됨
- 고친 TODO와 이유: D27-06-A01~D27-06-A04 구현 — prepare_pipeline_request로 원 질문·이력·플래그 구성, wire_langchain_pipeline으로 create_rag_pipeline 조립, validate_trace로 질의·ID 기록 및 후보 내 포함 여부 확인, audit_pipeline으로 모드·단계·출력 출처 및 수동 대조 필요성을 남기기 위함
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): rerank 단계(약 5.16초)의 후보 대상 수나 배치/모델 호출 방식을 조정하면 전체 파이프라인 응답 지연을 줄일 수 있을 것으로 기대되나, 순위 정확도 변동 여부와 실제 단축 폭은 실측 전까지 단정할 수 없음
