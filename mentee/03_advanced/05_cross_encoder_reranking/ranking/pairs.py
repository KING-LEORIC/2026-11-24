"""단계별 역할 분리: ranking/pairs.py / 독립 실행은 main.py."""

"""질의와 후보 문서 본문을 결합해 CrossEncoder 입력용 (질문, 문서본문) 쌍 목록을 생성하는 모듈"""


# CrossEncoder 입력 쌍 목록 생성 함수
# - 각 후보 Document의 page_content와 question을 튜플로 묶어 리스트 반환
def create_pairs(question, docs):
    """CrossEncoder 입력은 [질문, 문서본문]의 쌍 목록입니다."""
    # BEGIN D27-05-A01
    # TODO D27-05-A01: CrossEncoder 입력은 [질문, 문서본문]의 쌍 목록입니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 질의 및 문서 본문 튜플 리스트 구성 및 반환
    return [(question, d.page_content) for d in docs]
    # raise NotImplementedError("D27-05-A01 미완성")
    # END D27-05-A01


"""
후보 문서 목록과 사용자 질의를 CrossEncoder 스코어러 입력 형식인 (질문, 본문) 쌍으로 변환하도록 구현하였다.
원본 문서 본문 순서를 유지한 채 쌍 목록을 생성하여 재순위화 입력 인터페이스를 표준화하였다.
"""
