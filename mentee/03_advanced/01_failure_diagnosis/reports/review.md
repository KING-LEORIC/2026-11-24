# 실행 기록 (직접 작성)

- 선택 단계 / 실습: Day27 실습 01 · 01_failure_diagnosis (STAGE_RUNNERS[1], day27_01_live.json)
- 실행 날짜와 Python Interpreter: 2026-11-24 / 프로젝트 가상환경 Python
- 실행 모드: **live** (--offline 미지정으로 day27_01_live.json 생성되었으나, JSON 내부 execution_mode는 "fixed_diagnostic_cases"이며 "note"에 *"일반 검색 알고리즘 또는 실제 LLM 모델을 호출하지 않은 진단 예시"*로 기록됨)
- 요청 질문과 Category: 해당 없음 (F01~F07 고정 진단 케이스 집합 대상 실행으로 단일 사용자 질의·카테고리 파라미터 미사용)
- Query Rewrite의 원 질문과 검색용 질문: 해당 없음 (F01에서 ambiguous: true로 "rewrite" 단계 진단은 수행되었으나 실제 질의 재작성 입·출력 문자열은 미포함)
- Candidate ID → Rerank ID → Context included ID: 해당 없음 (실제 검색·리랭킹·컨텍스트 조립 결과 대신 gold_in_candidates, gold_in_context 불리언 플래그만 reason.evidence에 기록됨)
- 답변과 출처 문서의 실제 내용 대조: 해당 없음 (실제 LLM 답변 및 원문 문서 본문 미생성; F04는 validation 단계, F05는 healthy 단계로 분류되고 각 단계별 improvement 문구만 매핑됨)
- 실패 또는 예상과 다른 결과: 파일명은 day27_01_live.json이지만 실제 검색·LLM 호출 없이 고정 진단 케이스(fixed_diagnostic_cases)만 평가한 결과임; F06은 authorization_filter(authorized: false), F07은 version_filter(current: false)로 선행 정책 필터 단계에서 조기 진단됨
- 고친 TODO와 이유: D27-01-A01~D27-01-A04 구현 — 권한·버전·인덱스 준비·모호성·후보/컨텍스트 포함 여부·출처 유효성 순으로 최우선 실패 단계를 판정(diagnose_stage)하고, 단계별 조치(recommend_action), 핵심 근거 3종(reason_for_stage), 정책·단계 감사 로그(audit_case)를 구조화하기 위함
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): 고정 진단 케이스(F01~F07)가 아닌 실제 질의·검색·재순위·생성 로그와 연결할 경우, ambiguous 및 gold_in_candidates/gold_in_context 플래그를 실제 파이프라인 산출물에서 자동 산출하도록 연동하면 수동 플래그 누락이나 불일치를 줄일 수 있을 것으로 기대되나, 실제 연동 후 실측 검증이 필요함
