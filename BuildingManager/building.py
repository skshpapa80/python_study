from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Room:
    room_number: int         # 호수 (예: 101호)
    area_sqm: float          # 면적 (㎡)
    deposit: int             # 보증금 (원)
    monthly_rent: int        # 월세 (원)
    is_occupied: bool = False # 입주 여부
    tenant_name: Optional[str] = None # 입주사명

class BuildingManager:
    def __init__(self, name: str):
        self.name = name
        self.rooms: dict[int, Room] = {}

    def add_room(self, room: Room):
        self.rooms[room.room_number] = room
        print(f"✅ {room.room_number}호 등록이 완료되었습니다.")

    def calculate_total_expected_income(self) -> int:
        """입주된 방들의 총 월세 수입 계산"""
        return sum(r.monthly_rent for r in self.rooms.values() if r.is_occupied)

# 사용 예시
if __name__ == "__main__":
    my_building = BuildingManager("파이썬 타워")
    
    # 호실 정보 등록
    my_building.add_room(Room(101, 45.5, deposit=10000000, monthly_rent=850000, is_occupied=True, tenant_name="망고 소프트"))
    my_building.add_room(Room(102, 50.0, deposit=15000000, monthly_rent=1000000, is_occupied=False))

    print(f"💰 예상 월 임대 수익: {my_building.calculate_total_expected_income():,}원")
    