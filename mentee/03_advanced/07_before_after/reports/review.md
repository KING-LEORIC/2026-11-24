# 실행 기록 (직접 작성)

- 선택 단계 / 실습: Day27 실습 07 · 07_before_after (STAGE_RUNNERS[7], outputs/day27_07_live.json)
- 실행 날짜와 Python Interpreter: 2026-11-24 / 프로젝트 가상환경 Python
- 실행 모드: **live** (execution_mode: "live_e5_cuda_postgresql_crossencoder", audit.mode: "live", day27_07_live.json 생성)
- 요청 질문과 Category: Question ID "Q01" (질문 문자열 미기록) / Category: "시설" (gold: ["FAC-102-C1"], k: 2, gold_separate: true, same_candidates: true)
- Query Rewrite의 원 질문과 검색용 질문: 해당 없음 (07_before_after 단계는 재순위화 전·후 Top-k 비교 및 통제 점검을 수행하며 Query Rewrite 입·출력 필드는 미포함)
- Candidate ID → Rerank ID → Context included ID:
    - Candidate ID (before, search_ms: 640.213): FAC-102-C1, FAC-107-C1, FAC-109-C1, FAC-103-C1, FAC-101-C1 (before_contains_gold: true)
    - Rerank ID (after, rerank_ms: 4432.401, same_candidates: true): FAC-102-C1, FAC-109-C1, FAC-107-C1, FAC-103-C1, FAC-101-C1 (after_contains_gold: true, Top-2: FAC-102-C1, FAC-109-C1)
    - Context included ID: 해당 없음 (컨텍스트 선별·생성 단계 미포함)
- 답변과 출처 문서의 실제 내용 대조: 해당 없음 (최종 생성 답변 및 문서 원문 본문 미포함; 골드 문서 FAC-102-C1은 전·후 모두 Top-2에 유지됨)
- 실패 또는 예상과 다른 결과: 특이 오류 없이 before_contains_gold: true, after_contains_gold: true로 유지되었고 "Top-k 관련 문서 포함 여부는 변하지 않음"으로 해석됨; FAC-109-C1과 FAC-107-C1의 세부 순서가 역전되었으나 Top-2 골드 포함 여부는 동일하며 rerank_ms(4432.401ms)가 search_ms(640.213ms)보다 약 6.9배 길게 소요됨(repeat_needed: true, causal_improvement_claim: false)
- 고친 TODO와 이유: D27-07-A01~D27-07-A04 구현 — compare_rankings로 k=2 골드 포함 비교, interpret_change로 순위·포함 변동 시 섣부른 개선 단정 방지, check_conditions로 골드 분리(gold_separate) 및 후보 풀 유지(same_candidates) 검증, audit_comparison으로 모드·시간 비음수·반복 측정 필요 및 단일 사례 인과 개선 주장 불가 기록을 수행하기 위함
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): 여러 질문(Q01 외 추가 케이스)과 반복 측정을 확보해 전·후 순위 변동 및 지연 시간 분포를 함께 비교하면 단일 사례(Q01) 기반 해석의 한계를 줄일 수 있을 것으로 기대되나, 다중 케이스 실측 전까지 일반화나 개선 효과를 단정할 수 없음
