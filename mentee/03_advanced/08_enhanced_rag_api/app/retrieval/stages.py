"""단계별 역할 분리: app/retrieval/stages.py / 독립 실행은 main.py."""

"""Rewrite → Retrieve → Rerank → Context → Generation·Validation 단계가 연결된 서비스 체인을 생성하는 모듈"""


# 서비스용 RAG 체인 생성 함수
# - offline 옵션에 따라 coursekit.runtime.create_demo_chain으로 전체 단계 체인 구성
def make_service_chain(offline):
    """Rewrite → Retrieve → Rerank → Context → Generation·Validation을 연결합니다."""
    # BEGIN D27-08-A01
    # TODO D27-08-A01: Rewrite → Retrieve → Rerank → Context → Generation·Validation을 연결합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 데모·서비스용 체인 팩토리(create_demo_chain) 임포트
    from coursekit.runtime import create_demo_chain

    # 실행 모드(offline) 반영 체인 생성 및 반환
    return create_demo_chain(offline=offline)
    # raise NotImplementedError("D27-08-A01 미완성")
    # END D27-08-A01


"""
질의 재작성부터 검색, 재순위화, 컨텍스트 구성, 생성 및 검증까지 이어지는 RAG 체인을 
create_demo_chain으로 연결하여 서비스 계층에서 재사용할 수 있도록 구성하였다.
"""
