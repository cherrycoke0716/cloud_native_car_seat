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
        
        # 메타데이터 등록 시도 (VSS 트리에 해당 경로가 없으면 등록)
        try:
            logger.info("Registering Vehicle.Cabin.Seat.Row1.Pos1.Position")
            # client.set_metadata가 비동기 메서드일 수 있으나, 동기 컨텍스트에서는 동기적으로 호출됨을 가정하거나, 
            # 0.4.0 버전 이상에서는 ensure_startup_connection=True 기본값이면 연결됨.
            # 하지만 VSSClient는 동기/비동기가 나뉨. 여기서는 동기 컨텍스트인지 확인 필요.
            # kuksa_client.grpc.VSSClient vs kuksa_client.grpc.aio.VSSClient
            # 현재 import는 kuksa_client.grpc.VSSClient (동기)
            from kuksa_client.grpc import Metadata
            client.set_metadata({
                'Vehicle.Cabin.Seat.Row1.Pos1.Position': Metadata(
                    data_type='uint8',
                    description='Seat position of row 1 pos 1',
                    entry_type='Actuator'
                )
            })
            logger.info("Metadata registered successfully")
        except Exception as e:
            logger.warning(f"Metadata registration skipped or failed: {e}")

        while True:
            # 1. 다음 위치 계산
            current_pos = calculate_next_position(current_pos)
            
            # 2. KUKSA Databroker로 값 전송
            logger.info(f"Set Vehicle.Cabin.Seat.Row1.Pos1.Position to: {current_pos}%")
            
            try:
                client.set_current_values({
                    'Vehicle.Cabin.Seat.Row1.Pos1.Position': Datapoint(current_pos),
                })
            except Exception as e:
                logger.error(f"Error setting value: {e}")
                
            # 3. 2초 대기
            time.sleep(2)

if __name__ == "__main__":
    main()