"""검색과 Reranker가 공통으로 요구하는 ID·Metadata 검증."""

# 문서 ID 및 필수 메타데이터 유효성 검증 함수 임포트
# - valid_document : 단일 Document 객체의 ID·메타데이터 규약 검사
from coursekit.documents import valid_document

"""검색 및 재순위화 단계에서 공유하는 후보 문서 ID·메타데이터 유효성 검증 모듈"""


# 후보 문서 목록 일괄 검증 함수
# - 각 문서에 valid_document를 적용해 검증된 Document 리스트 반환
def validate_candidates(documents):
    # 전체 문서 유효성 검사 수행 및 결과 리스트 반환
    return [valid_document(d) for d in documents]


"""
검색과 재순위화 단계가 공통으로 요구하는 문서 ID 및 메타데이터 무결성을 
valid_document로 일괄 확인하도록 구성하여 단계 간 입력 규약을 통일하였다.
"""
