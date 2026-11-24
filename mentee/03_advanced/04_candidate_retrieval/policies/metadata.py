"""단계별 역할 분리: policies/metadata.py / 독립 실행은 main.py."""

"""후보 Document의 필수 출처 메타데이터 유효성과 요청 카테고리 일치 여부를 검증하는 정책 모듈"""


# 후보 문서 메타데이터 및 카테고리 일치 점검 함수
# - valid_document로 필수 메타데이터(chunk_id, source_locator 등) 검증 후 요청 category와 일치하는지 확인
def metadata_check(docs, payload):
    """각 Document의 chunk_id·source_locator·Category를 검사합니다."""
    # BEGIN D27-04-A03
    # TODO D27-04-A03: 각 Document의 chunk_id·source_locator·Category를 검사합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.

    # 문서 메타데이터 유효성 검증 유틸리티(valid_document) 호출
    from coursekit.documents import valid_document

    # 전체 문서 유효성 통과 및 요청 payload category 일치 여부 반환
    return all(
        valid_document(d).metadata["category"] == payload["category"] for d in docs
    )
    # raise NotImplementedError("D27-04-A03 미완성")
    # END D27-04-A03


"""
검색된 후보 Document의 출처 메타데이터 무결성을 확인하고 요청된 카테고리와 일치하는지 검사함으로써, 
후속 컨텍스트 구성 단계로 넘어가는 문서의 정합성과 필터 준수 여부를 보장하도록 구성하였다.
"""
