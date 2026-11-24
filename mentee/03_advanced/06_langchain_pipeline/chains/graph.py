"""단계별 역할 분리: chains/graph.py / 독립 실행은 main.py."""

"""주입된 의존성과 실행 모드를 바탕으로 LangChain RAG 파이프라인 체인을 조립하는 그래프 모듈"""


# RAG 파이프라인 체인 조립 함수
# - dependencies 위치 인자를 create_rag_pipeline에 언패킹 전달하고 offline 플래그 적용
def wire_langchain_pipeline(dependencies, offline):
    """LCEL는 Runnable을 준비할 뿐이고 .invoke()가 실행 시작점입니다."""
    # BEGIN D27-06-A02
    # TODO D27-06-A02: LCEL는 Runnable을 준비할 뿐이고 .invoke()가 실행 시작점입니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 파이프라인 체인 팩토리(create_rag_pipeline) 임포트
    from coursekit.pipeline import create_rag_pipeline

    # 의존성 및 오프라인 옵션을 반영해 실행 대기 상태의 체인 반환
    return create_rag_pipeline(*dependencies, offline=offline)
    # raise NotImplementedError("D27-06-A02 미완성")
    # END D27-06-A02


"""
의존성 컬렉션(*dependencies)과 실행 모드(offline)를 create_rag_pipeline에 연결하여 
호출 시점(.invoke())에 실행될 RAG 파이프라인 Runnable을 구성하도록 구현하였다.
이를 통해 그래프 조립 책임과 실제 모델·검색 실행 시점을 명확히 분리하였다.
"""
