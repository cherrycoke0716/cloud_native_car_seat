import pytest
from src.seat_service import calculate_next_position

def test_seat_position_increment():
    """10%씩 정상적으로 증가하는지 테스트"""
    assert calculate_next_position(0) == 10
    assert calculate_next_position(50) == 60
    assert calculate_next_position(80) == 90

def test_seat_position_safety_reset():
    """90% 초과 시 0%로 리셋되는지 테스트"""
    # 현재 위치가 90일 때, 다음 위치는 100이 되므로 0으로 리셋되어야 함
    assert calculate_next_position(90) == 0
    
    # 현재 위치가 85일 때, 다음 위치는 95가 되므로 0으로 리셋되어야 함
    assert calculate_next_position(85) == 0