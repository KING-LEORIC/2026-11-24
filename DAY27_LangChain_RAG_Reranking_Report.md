# DAY 27 학습 보고서

## LangChain RAG & Reranking

**학습일:** 2026년 11월 24일  
**핵심 주제:** Query Rewrite · Multi-query · Cross-Encoder  
**학습 범위:** LangChain RAG Orientation부터 FastAPI · Citation · Agent Tool까지

---

## 1. 학습 목표

이번 수업의 목표는 기존 RAG 구조를 유지하면서 검색 품질을 개선하는 방법을 이해하고, 이를 LangChain으로 연결하는 것이다.

기존 RAG는 사용자의 질문으로 관련 문서를 검색하고, 검색한 문서를 LLM에 전달해 답변을 생성한다. 하지만 질문이 모호하거나 문서와 표현이 다르면 필요한 자료를 놓칠 수 있고, 검색된 문서의 순서가 적절하지 않을 수도 있다.

이를 개선하기 위해 다음 세 가지 기술을 학습했다.

| 기술 | 역할 |
|---|---|
| **Query Rewrite** | 대화 기록을 참고해 모호한 질문을 독립적인 검색 질문으로 변경 |
| **Multi-query** | 여러 표현의 검색 질문으로 후보 문서를 폭넓게 검색하고 결과를 통합 |
| **Cross-Encoder Reranking** | 검색된 후보 문서를 질문과 다시 비교해 관련성 순서로 재정렬 |

이 과정에서 LangChain은 E5, PostgreSQL, Cross-Encoder, LLM 등을 대체하는 모델이 아니라, 각각의 기능을 실행하고 연결하는 Python 라이브러리로 사용된다.

## 2. 전체 처리 흐름

```text
사용자 질문 + Conversation History
              │
              ▼
       Query Rewrite
       독립적인 검색 질문 생성
              │
              ▼
     Query Expansion / Multi-query
       여러 검색 표현 생성
              │
              ▼
    Candidate Retrieval (E5 + pgvector)
    Category · Version · 권한 조건 적용
              │
              ▼
       Deduplication
       chunk_id 기준 중복 제거
              │
              ▼
    Cross-Encoder Reranking
    질문과 후보 문서의 관련성 점수 계산
              │
              ▼
          Top-N 선택
       최종 Context 구성 및 출처 ID 보관
              │
              ▼
       Prompt + LLM Generation
              │
              ▼
       Validation + Citation
              │
              ▼
       FastAPI 응답 / Agent Tool 연계
```

**핵심 구조:** 검색 전에 질문을 정리하고 검색 단계에서 후보를 확보한 뒤, 검색 후 Cross-Encoder로 순위를 다시 정한다.

---

## 3. Chapter별 학습 내용

### 01. LangChain RAG Orientation — Query · Failure · Retrieval

LangChain은 Prompt, Model, Retriever 등 서로 다른 구성요소를 공통 실행 방식으로 연결해 LLM 애플리케이션을 구성하는 라이브러리다. LangChain 자체가 LLM이나 데이터베이스, Embedding 모델은 아니다.

| 구성요소 | 역할 |
|---|---|
| E5 | 문장을 벡터로 변환 |
| PostgreSQL + pgvector | 문서 벡터 저장 및 검색 |
| Retriever | 질문에 관련된 문서 후보 검색 |
| Cross-Encoder | 질문과 문서 쌍의 관련성 평가 |
| Chat Model | 실제 LLM 호출 및 답변 생성 |
| LangChain | 위 구성요소의 입력·출력과 실행 흐름 연결 |

LangChain에서 구분해야 할 객체는 다음과 같다.

- **Document:** `page_content`에 문서 본문을, `metadata`에 `chunk_id`, `citation_id`, `source_locator` 등의 출처 정보를 담는 자료 객체다. 생성만으로 검색이나 모델 호출이 실행되지는 않는다.
- **Runnable:** 입력을 받아 작업을 실행하고 출력을 반환하는 실행 단위다.
- **RunnableLambda:** 일반 Python 함수를 Runnable로 감싸 Pipeline에 연결한다.
- **ChatPromptTemplate:** 입력값을 채워 Chat Message 묶음인 `ChatPromptValue`를 만든다.
- **Chat Model:** 메시지를 전달받아 실제 모델 제공자 API를 호출하고 `AIMessage`를 반환한다.

간단한 Runnable 연결 예시는 다음과 같다.

```python
from langchain_core.runnables import RunnableLambda


def clean_question(state: dict) -> dict:
    # 원 질문은 보존하고 검색용 질문을 별도 필드로 만든다.
    return {
        **state,
        "search_query": state["question"].strip(),
    }


def explain_step(state: dict) -> str:
    return f'Retriever 입력: {state["search_query"]}'


chain = (
    RunnableLambda(clean_question)
    | RunnableLambda(explain_step)
)

# 이 시점에 실제 실행된다.
result = chain.invoke({"question": "  회의실 예약 취소 절차는?  "})
```

`|`는 앞 Runnable의 출력을 다음 Runnable의 입력으로 연결한다. 연결식을 작성하는 것과 실제 실행은 다르며, `invoke()`를 호출할 때 작업이 실행된다.

또한 `prompt.invoke()`는 메시지를 구성하고, `model.invoke()`는 모델을 호출한다. 이름은 같아도 실행 결과와 역할이 다르다.

### 02. Conversational Query Rewrite — History · Standalone Query · Rewrite

대화 중 후속 질문은 앞선 대화가 있어야 의미를 이해할 수 있는 경우가 많다.

**예시**

- 이전 질문: “회의실 예약 방법은?”
- 현재 질문: “그럼 취소는?”
- 검색용 독립 질문: “교육센터 회의실 예약을 취소하는 방법은 무엇인가?”

- **History:** 현재 질문을 해석하는 데 필요한 이전 사용자·Assistant 대화다.
- **Standalone Query:** 대화 기록이 없어도 의미를 이해할 수 있는 독립 검색 질문이다.
- **Coreference:** “그것”, “그거” 등의 지시 표현이 무엇을 가리키는지 연결하는 관계다.
- **Ellipsis:** 문장의 일부가 생략된 현상이다.

Rewrite는 질문을 명확하게 바꾸는 것이지, 원래 질문에 없던 사실을 추가하는 과정이 아니다. 날짜, 대상, 부정 표현, 조건을 임의로 바꾸면 안 된다. 대화만으로 대상을 확정할 수 없다면 추측하지 않고 추가 확인이 필요하다고 표시한다.

원래 질문과 검색용 질문은 별도로 보관한다.

```python
def build_rewrite_input(history: list[dict], question: str) -> dict:
    if not question.strip():
        raise ValueError("question is empty")

    recent = history[-6:]
    return {
        "history": recent,
        "question": question,
    }
```

실제 Rewrite 단계에서는 `ChatPromptTemplate`과 Chat Model을 연결하고, Pydantic 스키마 등을 이용해 `standalone_query`와 `needs_clarification`을 구조화해 받을 수 있다.

| 필드 | 의미 |
|---|---|
| `original` 또는 `question` | 사용자가 실제 입력한 원래 질문 |
| `search_query` | Retriever에 전달할 재작성 질문 |
| `needs_clarification` / `status` | 추가 확인이 필요한지 나타내는 상태 |

### 03. Expansion & Multi-query — Expansion · Multi-query · Dedup

Query Expansion은 질문의 목적을 유지하면서 검색에 도움이 되는 관련 표현이나 용어를 보강하는 방법이다. 예를 들어 “예약 취소”와 “예약 철회”처럼 문서마다 다르게 쓰인 표현을 고려한다.

Multi-query는 하나의 검색 질문에서 여러 검색 질문을 만들어 각각 검색하는 전략이다.

| 질의 | 검색 표현 예시 | 검색 결과 예시 |
|---|---|---|
| Q1 | 예약 취소 방법 | C1, C2 |
| Q2 | 예약 철회 절차 | C2, C3 |
| Q3 | 취소 요청 방법 | C1, C4 |

검색 결과를 그대로 합치면 `C1, C2, C2, C3, C1, C4`처럼 같은 청크가 반복될 수 있다. 이를 `chunk_id` 기준으로 중복 제거하여 `C1, C2, C3, C4`로 통합한다.

교안의 통합 단계는 기존 검색 함수 `search_hits()`를 질의별로 실행하고, 동일한 `chunk_id`가 이미 있으면 다시 추가하지 않는 방식이다. 이때 모든 검색에 같은 Category·Version·권한 조건을 적용해야 한다. 어떤 질의에서 해당 문서를 찾았는지 `found_by_query`로 기록할 수도 있다.

검색 질문을 늘리면 검색 범위를 넓힐 수 있지만 검색 횟수, 중복, Reranking 처리량, 지연 시간도 증가한다. 따라서 질의 수와 각 질의의 검색 개수를 제한해야 한다. Multi-query의 단순 결과 병합은 검색 점수를 통합하는 모든 Ranking Fusion 기법과 같은 뜻은 아니다.

### 04. Candidate Retrieval — Candidate-k · Version · Filter

Candidate Retrieval은 Cross-Encoder가 정밀하게 평가할 후보 문서를 먼저 확보하는 단계다. 전체 문서를 처음부터 Cross-Encoder로 비교하지 않고, 기존 E5·pgvector Retriever로 후보를 줄인다.

| 용어 | 의미 |
|---|---|
| `Candidate-k` | 1차 검색에서 확보할 후보 문서 수 |
| `Top-N` / `Context-k` | 재정렬 후 최종 Context에 사용할 문서 수 |
| `Version` | 문서의 원본 버전 또는 처리 파이프라인 버전 |
| `Filter` | Category, 현재 버전, 준비 상태, 접근 권한 등 검색 조건 |

예를 들어 `candidate_k=10`으로 후보 10개를 확보한 뒤 Cross-Encoder로 순위를 정하고 `Top-N=3`으로 최종 문서 3개를 선택할 수 있다.

교안의 Metadata에는 다음과 같은 정보가 등장한다.

- `category`: 문서 분류
- `source_version`: 원본 문서 버전
- `pipeline_version`: 문서 처리 파이프라인 버전
- `ready`: 검색에 사용할 준비가 되었는지 여부

기존 E5 모델과 저장된 벡터는 유지한다. 교안에서는 `intfloat/multilingual-e5-small` 및 384차원 벡터 구성을 사용하고, 기존 `query:` / `passage:` 입력 규칙을 유지한다. Query Rewrite나 Multi-query를 추가한다고 기존 문서를 다시 Embedding하거나 재색인하는 것은 아니다.

Filter와 접근 권한은 LangChain이 자동으로 보장하는 것이 아니다. 애플리케이션과 검색 계층에서 올바르게 적용해야 하며, Multi-query의 모든 검색에도 동일한 조건을 적용해야 한다.

### 05. Cross-Encoder Reranking — Cross-Encoder · Reranker · Top-N

**Bi-Encoder와 Cross-Encoder의 차이**가 핵심이다.

| 구분 | Bi-Encoder | Cross-Encoder |
|---|---|---|
| 입력 방식 | 질문과 문서를 각각 인코딩 | 질문과 문서를 한 쌍으로 함께 입력 |
| 출력 | 문장 Embedding 벡터 | 입력 쌍의 관련성 점수 |
| 용도 | 대량 문서의 빠른 검색 | 검색 후보의 정밀한 재평가 |
| 특징 | 문서 벡터를 미리 계산해 저장 가능 | 후보별로 질문-문서 쌍을 계산하므로 상대적으로 비용이 큼 |

Cross-Encoder는 문장 Embedding을 생성하는 모델이 아니다. `(질문, 문서)` 쌍을 입력해 그 쌍의 관련성을 점수화한다. 따라서 전체 문서 검색보다는 Bi-Encoder가 먼저 찾은 Top-k 후보를 재정렬하는 용도에 적합하다.

교안에서는 `BAAI/bge-reranker-v2-m3` 모델을 예로 사용한다.

```python
from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder(
    "BAAI/bge-reranker-v2-m3",
    device="cuda:0",
)

question = "회의실 예약을 취소하는 방법은?"
passages = [
    "회의실 예약은 담당자 승인 후 확정됩니다.",
    "회의실 예약을 취소하려면 운영실에 철회를 요청합니다.",
]

pairs = [(question, passage) for passage in passages]
scores = cross_encoder.predict(pairs, batch_size=2)
```

후보 문서가 2개이므로 `(질문, 문서)` 입력 쌍도 2개 만들어진다. `predict()`가 각 쌍의 점수를 계산한다. `batch_size`는 한 번에 처리할 입력 쌍의 개수다.

점수는 정답 확률이 아니다. 점수 범위와 해석은 모델에 따라 다르며, 일부 모델은 0~1이 아닌 Logit을 반환한다. 같은 모델과 같은 질문에서 후보들의 상대적인 순위를 비교하는 용도로 이해해야 한다.

교안에서는 점수와 원본 Document를 묶어 내림차순으로 정렬하고, 상위 3개를 `ranked_docs`로 보관한다. 원본 Document 객체를 재배치하므로 `chunk_id`, `citation_id`, `source_locator` 등의 Metadata도 유지할 수 있다.

**중요한 한계:** 정답 문서가 최초 Candidate Set에 없다면 Reranker는 그 문서를 새로 검색하거나 생성할 수 없다. 따라서 최초 검색의 후보 포함 여부(Candidate Recall)가 Reranking 성능의 상한을 결정한다.

### 06. LangChain Integration — Runnable · Pipeline · invoke

각 단계의 중간 데이터를 `state`라는 Dictionary로 관리한다. 단계마다 정보를 덮어쓰지 않고 별도 필드로 보관하면 어느 단계에서 결과가 달라졌는지 추적하기 쉽다.

| State 필드 | 내용 |
|---|---|
| `question` | 원래 사용자 질문 |
| `history` / `history_text` | 대화 기록 |
| `search_query` / `search_queries` | Rewrite 및 Multi-query 결과 |
| `candidate_hits` / `candidate_docs` | Retriever가 반환한 후보 |
| `ranked_hits` / `ranked_docs` | Reranking 후 순위 |
| `context` | LLM에 전달할 최종 근거 내용 |
| `included_ids` | 실제 Context에 포함한 출처 ID |
| `answer` / `sources` | 검증 후 반환할 답변 및 출처 |

기본적인 연결 원리는 다음과 같다.

```python
from langchain_core.runnables import RunnableLambda

rewrite_stage = RunnableLambda(rewrite_step)
retrieval_stage = RunnableLambda(retrieve_step)
rerank_stage = RunnableLambda(rerank_step)
context_stage = RunnableLambda(context_step)

search_pipeline = (
    rewrite_stage
    | retrieval_stage
    | rerank_stage
    | context_stage
)

result = search_pipeline.invoke(request_state)
```

위 코드는 각 단계 함수가 서로 호환되는 State Dictionary를 반환한다는 전제의 구조 예시다. 실제 강의 프로젝트에서는 질문 확인, Multi-query, 오류 처리, Prompt·Model 생성 단계 등을 함께 연결한다.

파일은 역할에 따라 나눠 관리할 수 있다.

| 파일 예시 | 책임 |
|---|---|
| `query.py` | Query Rewrite |
| `retrieval.py` | 기존 E5 검색 및 후보 반환 |
| `rerank.py` | Cross-Encoder 점수 계산 및 재정렬 |
| `pipeline.py` | State와 Runnable 단계 연결, Context·생성 처리 |
| `api.py` | FastAPI 요청 및 응답 처리 |

Prompt와 Model도 구분한다. Prompt의 `invoke()`는 메시지를 구성하고, Chat Model의 `invoke()`는 실제 모델 호출을 수행한다. Runnable을 연결한 시점과 `invoke()`로 실행하는 시점도 다르다.

오류는 단계별로 구분한다. Rewrite, Retrieval, Reranker, Generator 오류를 정상 검색 결과로 조용히 대체하면 안 된다. Fallback을 사용한다면 실제로 어떤 경로가 실행되었는지 기록해야 한다.

### 07. Compare & Diagnose — Before/After · Coverage · Latency

개선한 RAG가 실제로 좋아졌는지는 동일한 질문과 평가 조건으로 비교해야 한다.

비교 구성 예시는 다음과 같다.

1. Baseline: 기존 RAG
2. Rewrite only: Query Rewrite만 적용
3. Rerank only: 동일한 후보 집합에 Cross-Encoder만 적용
4. Rewrite + Rerank: 두 기능을 함께 적용

Reranker의 효과를 따로 확인할 때는 같은 Candidate Set을 사용해야 한다. 후보 자체가 바뀌면 검색 범위 변화와 재정렬 효과를 구분하기 어렵다.

- **Coverage:** 필요한 정보나 정답 문서를 얼마나 빠짐없이 확보했는지 살펴본다.
- **Hit@k:** 정답 문서가 상위 k개 안에 하나라도 포함되는지 확인한다.
- **Recall@k:** 전체 관련 문서 중 상위 k개에서 찾아낸 비율을 평가한다.
- **MRR / nDCG:** 정답 문서의 순위와 관련성 정도를 고려하는 평가 지표다. 교안에서는 상세 계산을 다음 평가 수업으로 연결한다.
- **Latency:** Query Rewrite, Retrieval, Reranking, Generation 등 각 단계와 전체 처리에 걸린 시간이다.

GPU 연산 시간은 비동기로 처리될 수 있으므로 정확한 CUDA 단계 시간 측정에는 필요 시 `torch.cuda.synchronize()`로 연산 완료를 기다려야 한다. 이 동기화는 GPU 연산 측정에 관한 것이며 원격 API나 데이터베이스 호출 자체를 동기화하는 것은 아니다.

교안 HTML에 포함된 순위, 점수, 비교 결과는 사전 준비된 교육용 예시다. 실제 E5·PostgreSQL·Cross-Encoder·LLM을 실행해 측정한 성능 결과가 아니다. 실제 개선 여부는 고정된 평가 질문과 정답 문서로 별도 검증해야 한다.

### 08. End-to-End & Agent Bridge — FastAPI · Citation · Agent Tool

개선한 RAG Pipeline을 FastAPI 서비스로 연결한다.

- **FastAPI:** HTTP 요청을 받아 RAG Service를 실행하고 결과를 반환한다.
- **Pydantic:** 질문, Category, History, `candidate_k`, `context_k`, Rewrite/Rerank 사용 여부 등 요청 데이터의 형태와 범위를 검증한다.
- **Citation:** 답변에 사용한 근거 문서의 출처를 연결한다.
- **Grounding:** 생성된 답변의 주장과 실제 근거 원문이 일치하는지 확인한다.
- **Agent Tool:** 완성한 RAG 검색 기능을 이후 Agent가 필요할 때 호출할 수 있도록 도구로 제공한다.

Citation을 표시할 때는 LLM이 임의로 만든 문서 경로나 ID를 신뢰하지 않는다. 서버가 실제 Context에 포함한 `included_ids`와 Document Metadata를 이용해 출처를 연결한다. 출처 ID가 존재해도 답변의 내용이 원문과 일치한다는 보장은 없으므로 Grounding 검증이 별도로 필요하다.

실행 상태도 구분해야 한다.

| 상태 예시 | 의미 |
|---|---|
| `needs_clarification` | History만으로 질문 대상을 확정할 수 없어 사용자 확인 필요 |
| `insufficient_context` | 검색을 수행했지만 현재 근거만으로 답변할 수 없음 |
| `rerank_failed` | Reranker 실행 중 오류 발생 |
| `answered` | 답변 생성 및 검증 절차를 통과한 상태 |

RAG는 정해진 처리 순서에 따라 검색하고 답변하는 Pipeline이다. Agent는 목표에 따라 어떤 Tool을 사용할지 선택할 수 있다. RAG 검색 기능 자체를 Agent Tool로 제공할 수 있지만, Tool 호출 권한·입력·호출 한도·실행 결과 관리는 애플리케이션에서 검증해야 한다. 이번 수업은 Agent 자체의 구현보다는 후속 연결 지점을 이해하는 데 초점이 있다.

---

## 4. 핵심 용어 정리

| 용어 | 의미 |
|---|---|
| Query | 검색 질문 |
| History | 이전 대화 기록 |
| Standalone Query | 대화 기록 없이도 이해할 수 있는 독립 검색 질문 |
| Query Rewrite | 질문의 의미를 보존하며 검색에 적합한 형태로 변경 |
| Query Expansion | 검색에 도움이 되는 관련 표현·용어 확장 |
| Multi-query | 여러 검색 질문을 생성해 각각 검색하는 전략 |
| Deduplication | 중복 문서 제거 |
| `chunk_id` | 청크를 구별하는 고유 식별자 |
| Candidate-k | 1차 검색에서 확보할 후보 문서 수 |
| Cross-Encoder | 질문과 문서를 함께 입력해 쌍의 관련성을 평가하는 모델 |
| Reranker | 기존 후보의 관련성 점수를 바탕으로 순위를 재정렬하는 모델·기능 |
| Top-N | 재정렬 후 최종 선택할 문서 수 |
| Runnable | LangChain의 공통 실행 단위 |
| RunnableLambda | Python 함수를 Runnable로 감싸는 클래스 |
| LCEL | Runnable을 연결하는 LangChain 표현 방식 |
| `invoke()` | 입력을 전달해 Runnable을 실제 실행하는 메서드 |
| State | 단계 간 전달하는 중간 데이터 묶음 |
| Citation | 답변의 근거 출처 표시 |
| Grounding | 답변 내용이 실제 근거 자료에 기반하는지 확인하는 개념 |
| Latency | 처리 지연 시간 |

## 5. 실무 적용 시 주의사항

1. **원 질문 보존:** 검색용으로 Rewrite한 질문과 사용자가 입력한 원래 질문을 별도로 저장한다.
2. **의미 왜곡 방지:** 대화에 없는 날짜·조건·대상을 임의로 추가하지 않는다. 모호하면 확인을 요청한다.
3. **검색 조건 일관성:** Multi-query의 모든 검색에 동일한 Category·Version·권한 조건을 적용한다.
4. **후보와 최종 근거 구분:** Candidate-k는 넓게 확보하는 후보 수이고, Top-N은 최종 Context에 넣는 수다.
5. **출처 Metadata 보존:** 재정렬 과정에서 원본 Document와 `chunk_id`, `citation_id`, `source_locator`를 유지한다.
6. **점수 해석 주의:** Cross-Encoder 점수는 정답 확률이 아니며 모델에 따라 범위와 의미가 다르다.
7. **실패 상태 구분:** 근거 부족, 질문 모호함, 모델 실행 오류를 같은 상태로 처리하지 않는다.
8. **측정 결과 구분:** 교육용 고정 시연 값과 실제 모델 실행·측정 결과를 혼동하지 않는다.

### 실습 환경 참고

교안의 Cross-Encoder 예제는 `torch.cuda.is_available()`을 확인하고 `device="cuda:0"`을 사용하는 NVIDIA CUDA 환경을 전제로 한다. NVIDIA CUDA GPU가 없는 환경에서는 해당 검사를 통과하지 못한다. CPU 실행이 필요하면 모델을 `device="cpu"`로 로드하는 별도 경로를 사용하고, 실제 처리 시간을 측정해야 한다. CPU 실행은 교안의 CUDA 실행과 성능이 같다는 의미가 아니다.

---

## 6. 학습 결론

이번 수업에서는 기존 RAG의 검색 품질을 개선하기 위한 Query Rewrite, Multi-query, Cross-Encoder Reranking의 역할을 학습했다. Query Rewrite는 대화 맥락을 검색 가능한 독립 질문으로 바꾸고, Multi-query는 여러 표현으로 검색해 후보 범위를 넓힌다. 검색된 후보는 `chunk_id` 기준으로 중복을 제거하고, E5 기반 Retriever가 찾은 문서를 Cross-Encoder가 질문과 함께 비교해 재정렬한다. 최종적으로 상위 문서만 Context에 넣어 LLM에 전달한다.

LangChain의 핵심은 이러한 작업을 Runnable로 구성하고 `|`로 연결한 뒤 `invoke()`로 실행하는 것이다. Document는 본문과 출처 정보를 담는 자료 객체이며, State는 각 단계의 입력과 결과를 보관한다. FastAPI는 Pipeline을 서비스로 제공하고, Citation·Grounding 검증은 실제 사용한 근거와 답변의 일치 여부를 확인한다. 완성된 RAG 검색 기능은 이후 Agent Tool로 재사용할 수 있다.

**핵심 정리:** Query Rewrite는 질문을 명확하게 만들고, Multi-query는 검색 범위를 넓히며, Cross-Encoder는 검색된 후보의 순서를 정밀하게 다시 정한다. LangChain은 이 단계들을 연결하고 실행하는 역할을 한다.

---

## 7. 참고 자료

### 강의 교안

- `Day27_20261124.html` — LangChain RAG & Reranking

### 공식 문서

- [LangChain Python Documentation](https://docs.langchain.com/oss/python/langchain/overview)
- [LangChain Runnable Reference](https://reference.langchain.com/python/langchain-core/runnables)
- [Sentence Transformers — Cross-Encoders](https://sbert.net/examples/cross_encoder/applications/README.html)
- [Sentence Transformers — Cross-Encoder Usage](https://sbert.net/docs/cross_encoder/usage/usage.html)
- [Sentence Transformers — CrossEncoder API](https://sbert.net/docs/package_reference/cross_encoder/model.html)
- [BAAI — bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3)

