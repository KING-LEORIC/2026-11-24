"""HTTP Request/Response Schema는 공통 Pydantic 계약을 그대로 재사용."""

# 공통 HTTP 요청·대화 턴 Pydantic 스키마 임포트
# - RagRequest : RAG API 요청 스키마
# - Turn : 대화 이력 단일 턴 스키마
from coursekit.api import RagRequest, Turn

"""공통 API 요청·대화 턴 Pydantic 모델을 외부로 재노출하는 스키마 재사용 모듈"""

# 외부 공개 스키마 심볼 목록 정의
__all__ = ["RagRequest", "Turn"]

"""
coursekit.api가 정의한 공통 Pydantic 요청·대화 스키마를 중복 정의 없이 재사용·재노출하여 
API 입·출력 계약의 일관성을 유지하도록 구성하였다.
"""
