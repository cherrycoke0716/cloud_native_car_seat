import time
import logging
from kuksa_client.grpc import VSSClient
from kuksa_client.grpc import Datapoint

# 로그 설정 (실행 과정을 보기 위함)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SeatService")

# VSS 경로: 운전석 1열 시트의 위치 (0-100 사이의 퍼센트)
SEAT_POS_PATH = "Vehicle.Cabin.Seat.Row1.Pos1.Position"

def main():
    # 1. Databroker 연결 (WSL2에서 로컬 도커로 연결 시 localhost:55555)
    with VSSClient('127.0.0.1', 55555) as client:
        logger.info("Connected to KUKSA Databroker")

        # 2. 초기 값 설정 (시트를 0으로 초기화)
        logger.info(f"Initializing {SEAT_POS_PATH} to 0")
        client.set_current_values({
            SEAT_POS_PATH: Datapoint(0),
        })

        try:
            while True:
                # 3. 현재 시트 위치 값 가져오기 (Get)
                current_values = client.get_current_values([SEAT_POS_PATH])
                current_pos = current_values[SEAT_POS_PATH].value
                
                logger.info(f"Current Seat Position: {current_pos}%")

                # 4. 간단한 로직: 10씩 증가시키되 90 이상은 안전상 금지
                new_pos = current_pos + 10
                
                if new_pos > 90:
                    logger.warning("Safety Limit Reached! Resetting to 0.")
                    new_pos = 0
                
                # 5. 새로운 값 적용 (Set)
                logger.info(f"Setting Seat Position to: {new_pos}%")
                client.set_current_values({
                    SEAT_POS_PATH: Datapoint(new_pos),
                })

                time.sleep(2) # 2초마다 반복

        except KeyboardInterrupt:
            logger.info("Service stopped by user")

if __name__ == "__main__":
    main()