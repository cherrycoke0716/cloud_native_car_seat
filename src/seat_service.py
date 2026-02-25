import time
import os
import logging
from kuksa_client.grpc import VSSClient, Datapoint

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SeatService")

def calculate_next_position(current_position: int) -> int:
    """
    현재 위치에서 10%를 증가시키고, 
    증가된 위치가 90%를 초과하면 0%로 리셋하는 안전 로직
    """
    next_position = current_position + 10
    if next_position > 90:
        return 0
    return next_position

def main():
    current_pos = 0
    
    # Docker 환경 변수 지원 ('databroker' 호스트네임 사용)
    # 로컬 테스트 시에는 localhost로 폴백
    broker_host = os.getenv("KUKSA_DATA_BROKER_ADDR", "127.0.0.1")
    broker_port = int(os.getenv("KUKSA_DATA_BROKER_PORT", 55555))
    
    logger.info(f"Connecting to KUKSA Databroker at {broker_host}:{broker_port}")
    
    # client 연결 (insecure)
    with VSSClient(broker_host, broker_port, root_certificates=None) as client:
        logger.info("Connected to Databroker")
        
        # 메타데이터 등록 시도는 생략합니다. (Vehicle.Speed는 기본 제공)
        logger.info("Using default VSS path: Vehicle.Speed")

        while True:
            # 1. 다음 위치 계산
            current_pos = calculate_next_position(current_pos)
            
            # 2. KUKSA Databroker로 값 전송
            logger.info(f"Set Vehicle.Speed to: {current_pos}")
            
            try:
                client.set_current_values({
                    'Vehicle.Speed': Datapoint(current_pos),
                })
            except Exception as e:
                logger.error(f"Error setting value: {e}")
                
            # 3. 2초 대기
            time.sleep(2)

if __name__ == "__main__":
    main()