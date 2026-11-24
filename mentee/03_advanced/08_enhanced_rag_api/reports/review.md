# 실행 기록 (직접 작성)

- 선택 단계 / 실습: Day27 실습 08 · 08_enhanced_rag_api (STAGE_RUNNERS[8], outputs/day27_08_live.json 및 POST /api/v1/rag/answer 라이브 호출)
- 실행 날짜와 Python Interpreter: 2026-11-24 / /c/Users/pc_12/AppData/Local/Programs/Python/Python313/python
- 실행 모드: **live** (execution_mode: "live_e5_cuda_postgresql_llm", source_mode: "live", day27_08_live.json 생성 및 uvicorn app.main:create_app_factory --factory --reload 기동 확인)
- 요청 질문과 Category:
    - 러너 (day27_08_live.json): Q01 "회의실 예약을 취소하는 방법은?" / Category: "시설" (candidate_k: 5, context_k: 2), Q06 "정확한 과제 마감 날짜는?" (status: "insufficient_context"), INVALID_K (candidate_k: 0 → HTTP 422)
    - 직접 API 호출 (POST /api/v1/rag/answer): "회의실 예약을 취소하는 방법은?" / Category: "시설" (candidate_k: 5, context_k: 2)
- Query Rewrite의 원 질문과 검색용 질문: 원 질문 "회의실 예약을 취소하는 방법은?" → 검색용 질문 "회의실 예약을 취소하는 방법은?" (queries: ["회의실 예약을 취소하는 방법은?"], query_count: 1)
- Candidate ID → Rerank ID → Context included ID:
    - Candidate ID (5건): FAC-102-C1, FAC-107-C1, FAC-109-C1, FAC-103-C1, FAC-101-C1
    - Rerank ID (5건): FAC-102-C1, FAC-109-C1, FAC-107-C1, FAC-103-C1, FAC-101-C1
    - Context included ID (2건): FAC-102-C1, FAC-109-C1 (최종 인용 출처 source_ids: [2] → citation_id: 2, FAC-102-C1, guides/fac-102.md#section-1, 2026-11-v2, citation_consistent: true)
- 답변과 출처 문서의 실제 내용 대조: 답변 *"예약 시스템의 ‘나의 예약’ 메뉴에서 해당 예약을 선택해 취소하세요. 시작 2시간 전까지만 취소할 수 있습니다."*는 인용 출처 FAC-102-C1 (doc_id: "FAC-102", source_locator: "guides/fac-102.md#section-1", source_version: "2026-11-v2", category: "시설")의 예약 취소 경로 및 시작 2시간 전 취소 가능 기한 안내와 부합함(2026-11-24 워크스페이스 내 별도 guides/fac-102.md 파일은 미존재하여 응답 출처 메타데이터 기준으로 대조); Q06은 근거 부족 시 표준 미답변 문구와 누락 정보(missing_information)를 반환함
- 실패 또는 예상과 다른 결과: Q01·Q06 200 응답 및 INVALID_K 422 검증 오류 모두 의도대로 동작했으나, 초기 curl 호출 시 /ask 경로 404 및 셸 인자 UTF-8 파싱 오류(There was an error parsing the body)가 발생했고 /api/v1/rag/answer 경로로 --data-binary @- UTF-8 입력을 전달해 해결함; 또한 Q01 직접 API 호출 기준 총 소요 시간(timing_ms 합계 약 10,342.319ms) 중 rerank(4959.79ms), rewrite(2947.734ms), generation(1847.183ms) 비중이 큼
- 고친 TODO와 이유: D27-08-A01~D27-08-A04 구현 — make_service_chain으로 서비스 체인 연결, wire_fastapi로 클라이언트 역할 입력을 배제하고 서버에서 trusted_role="learner" 지정, check_http_response로 비-200 상태 기록 및 성공 응답의 source_ids와 sources ID 일치 검증, audit_http_response로 HTTP 상태·질의·실행 모드·단계·서버 정책 역할을 기록해 오류 은폐를 막기 위함
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): Q01 직접 호출 기준 rerank(약 4.96s)와 rewrite(약 2.95s) 단계의 병목 지점을 점검해 배치 크기나 호출 경로를 조정하면 응답 지연을 줄일 수 있을 것으로 기대되나, 실제 지연 단축 효과와 답변 품질 유지 여부는 실측 전까지 단정할 수 없음
