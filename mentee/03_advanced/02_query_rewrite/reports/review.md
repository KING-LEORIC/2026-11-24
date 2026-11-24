# 실행 기록 (직접 작성)

- 선택 단계 / 실습: Day27 실습 02 · 02_query_rewrite (STAGE_RUNNERS[2], day27_02_live.json)
- 실행 날짜와 Python Interpreter: 2026-11-24 / 프로젝트 가상환경 Python
- 실행 모드: **live** (execution_mode: "live_llm_api", day27_02_live.json 생성)
- 요청 질문과 Category: Q02 ("그럼 취소는 어떻게 해?", history_turns: 2), Q04 ("예약 시간을 바꾸고 싶은데?", history_turns: 1), Q-ambiguous ("그거는 어떻게 해?", history_turns: 0) / Category 값 미기록 (회의실 예약 맥락 대상)
- Query Rewrite의 원 질문과 검색용 질문:
    - Q02: "그럼 취소는 어떻게 해?" → "회의실 예약은 어떻게 취소하나요?" (status: "ready", changed: true)
    - Q04: "예약 시간을 바꾸고 싶은데?" → "회의실 예약 시간을 변경하려면 어떻게 해야 하나요?" (status: "ready", changed: true)
    - Q-ambiguous: "그거는 어떻게 해?" → "" (status: "clarification_required", changed: true, 사유: 대화 기록 내 ‘그거’ 지시 대상 부재)
- Candidate ID → Rerank ID → Context included ID: 해당 없음 (질의 재작성 단계까지만 수행되며 검색·리랭킹·컨텍스트 청크 ID 미포함)
- 답변과 출처 문서의 실제 내용 대조: 해당 없음 (최종 RAG 답변 및 원문 청크 미생성; Q02·Q04는 대화 맥락 기반 재작성 문구와 reason의 타당성 수동 검토 필요, Q-ambiguous는 모호성으로 clarification_required 처리됨)
- 실패 또는 예상과 다른 결과: Q-ambiguous에서 search_query가 ""로 비어 있음에도 audit.changed가 true로 기록됨 (original_question "그거는 어떻게 해?"와 "" 단순 문자열 비교 결과); 또한 status != "ready"일 때 check_semantics가 검사를 생략하므로 semantic_guard가 기본 true로 기록됨
- 고친 TODO와 이유: D27-02-A01~D27-02-A04 구현 — apply_rewrite로 모드별 재작성 호출, record_rewrite로 original_question과 search_query 분리 보존, check_semantics로 ready 상태의 부정·숫자 조건 탈락 시 ValueError 차단, audit_rewrite로 턴 수·변경 여부·수동 검토 필요(human_review_needed: true)를 남기기 위함
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): clarification_required로 search_query가 빈 문자열("")인 케이스에서 changed 플래그를 단순 비동일(!=) 대신 실제 검색 질의 생성 여부 또는 status == "ready" 조건과 구분해 기록하도록 개선하면 감사 로그 해석 혼동을 줄일 수 있을 것으로 기대되나, 실제 적용 후 실측 확인이 필요함
