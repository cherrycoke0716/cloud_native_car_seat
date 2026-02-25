import time
# from kuksa_client.grpc import VSSClient # 실제 KUKSA 클라이언트 임포트

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
    # client = VSSClient("127.0.0.1", 55555) # KUKSA Databroker 연결
    # client.connect()
    
    while True:
        # 1. 다음 위치 계산
        current_pos = calculate_next_position(current_pos)
        
        # 2. KUKSA Databroker로 값 전송 (VSS 표준 경로 사용)
        print(f"Set Vehicle.Cabin.Seat.Row1.Pos1.Position to: {current_pos}%")
        # client.set_current_values({'Vehicle.Cabin.Seat.Row1.Pos1.Position': current_pos})
        
        # 3. 2초 대기
        time.sleep(2)

if __name__ == "__main__":
    main()