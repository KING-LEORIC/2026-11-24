"""환경 설정은 coursekit.config에서 검증. 이 파일은 API 계층 진입점만 맡습니다."""

# coursekit 설정 검증 함수 임포트
# - require_cuda : CUDA 가용 디바이스 확인
# - require_setting : 필수 환경 설정값 조회 및 검증
# - schema_name : 대상 DB/벡터 스키마명 조회
from coursekit.config import require_cuda, require_setting, schema_name

"""API 계층 진입점에서 CUDA 장치, 스키마명 및 LLM 모델 설정을 검증·반환하는 런타임 점검 모듈"""


# 런타임 환경 설정 검증 함수
# - device, schema, llm_model 필수 설정값 확인 후 딕셔너리로 반환
def validate_runtime():
    # 검증된 디바이스, 스키마 및 LLM 모델 정보 반환
    return {
        "device": require_cuda(),
        "schema": schema_name(),
        "llm_model": require_setting("LLM_MODEL"),
    }


"""
API 진입 시점에 GPU(CUDA), 스키마, LLM 모델 등 필수 런타임 환경을 coursekit.config 규약으로 검증하여 
실행 전제 조건 충족 여부를 명확히 확인하도록 구성하였다.
"""
