# 실행 기록 (직접 작성)

- 선택 단계 / 실습: Day27 실습 04 · 04_candidate_retrieval (STAGE_RUNNERS[4], day27_04_live.json)
- 실행 날짜와 Python Interpreter: 2026-11-24 / 프로젝트 가상환경 Python
- 실행 모드: **live** (execution_mode: "live_e5_cuda_postgresql", day27_04_live.json 생성)
- 요청 질문과 Category: 요청 질문 문자열 미기록 / Category: "시설" (candidate_k: 5, context_k: 2)
- Query Rewrite의 원 질문과 검색용 질문: 해당 없음 (04_candidate_retrieval 단계는 후보 문서 조회 및 메타데이터·정책 점검을 수행하며 Query Rewrite 입·출력 필드는 미포함)
- Candidate ID → Rerank ID → Context included ID:
    - Candidate ID (5건, metadata_ok: true, policy_check: ready: true, current: true, public: true): FAC-102-C1, FAC-107-C1, FAC-109-C1, FAC-103-C1, FAC-101-C1
    - Rerank ID: 해당 없음 (리랭킹 단계 미포함)
    - Context included ID: 해당 없음 (context_k: 2 상한값이 기록되어 있으나 최종 선택된 컨텍스트 ID 목록은 본 JSON에 미포함)
- 답변과 출처 문서의 실제 내용 대조: 해당 없음 (최종 생성 답변 및 청크 원문 본문 미포함; 반환된 5개 후보 모두 metadata_ok: true 및 ready/current/public 정책 조건 충족)
- 실패 또는 예상과 다른 결과: 특이 오류 없음 (candidate_k: 5에 맞춰 5건의 후보 청크가 정상 반환되고 metadata_ok: true, policy_check 전 항목 true로 통과함; 단, context_k: 2로 축소될 대상 ID는 본 출력에 미표시)
- 고친 TODO와 이유: D27-04-A01~D27-04-A04 구현 — make_candidate_request로 candidate_k(5)와 context_k(2) 분리 설정, fetch_documents로 retriever.invoke 호출 및 candidate_k 초과 차단, metadata_check로 문서 유효성 및 카테고리 일치 검사, policy_check로 ready/current/public 정책 방어 확인을 수행하기 위함
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): context_k(2) 적용 후 실제 컨텍스트 포함 청크 ID와 원문 본문을 리포트에 함께 남기도록 확장하면 후보 검색 단계와 컨텍스트 구성 단계 간 선별 일관성을 더 쉽게 점검할 수 있을 것으로 기대되나, 구현 및 실측 검증 전까지 효과를 단정할 수 없음
