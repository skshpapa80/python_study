import sqlite3
from typing import Optional, List, Dict

class BuildingDB:
    def __init__(self, db_name: str = "building_manager.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        """데이터베이스 연결 객체 반환"""
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """테이블이 없으면 자동으로 생성"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tenants (
                    room_number INTEGER PRIMARY KEY,
                    tenant_name TEXT,
                    deposit INTEGER NOT NULL,
                    monthly_rent INTEGER NOT NULL,
                    is_occupied INTEGER DEFAULT 0
                )
            """)
            conn.commit()
        print("📁 DB 및 테이블 초기화 완료!")

    # 1. CREATE: 입주사 및 호실 정보 등록
    def add_room(self, room_number: int, deposit: int, monthly_rent: int, 
                 tenant_name: Optional[str] = None, is_occupied: bool = False):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO tenants (room_number, tenant_name, deposit, monthly_rent, is_occupied)
                VALUES (?, ?, ?, ?, ?)
            """, (room_number, tenant_name, deposit, monthly_rent, 1 if is_occupied else 0))
            conn.commit()
        print(f"✅ {room_number}호 정보 저장 완료!")

    # 2. READ: 전체 호실/입주사 목록 조회
    def get_all_rooms(self) -> List[Dict]:
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row  # 컬럼명으로 접근 가능하도록 설정
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tenants ORDER BY room_number ASC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    # 3. UPDATE: 입주 상태 및 계약 변경
    def update_tenant(self, room_number: int, tenant_name: str, is_occupied: bool = True):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tenants 
                SET tenant_name = ?, is_occupied = ?
                WHERE room_number = ?
            """, (tenant_name, 1 if is_occupied else 0, room_number))
            conn.commit()
        print(f"🔄 {room_number}호 입주 정보가 수정되었습니다.")

    # 4. DELETE: 퇴거 처리 (데이터 삭제 또는 공실 전환)
    def vacate_room(self, room_number: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tenants 
                SET tenant_name = NULL, is_occupied = 0
                WHERE room_number = ?
            """, (room_number,))
            conn.commit()
        print(f"🚪 {room_number}호 퇴거 처리가 완료되었습니다 (공실 전환).")

# 🧪 실행 및 테스트 예시
if __name__ == "__main__":
    db = BuildingDB()

    # 1. 샘플 호실 데이터 등록
    db.add_room(101, deposit=10000000, monthly_rent=850000, tenant_name="망고 소프트", is_occupied=True)
    db.add_room(102, deposit=15000000, monthly_rent=1000000, is_occupied=False)
    db.add_room(201, deposit=20000000, monthly_rent=1500000, tenant_name="코드 카페", is_occupied=True)

    # 2. 조회 및 출력
    print("\n--- 🏢 현재 건물 입주 현황 ---")
    rooms = db.get_all_rooms()
    for r in rooms:
        status = f"입주중 ({r['tenant_name']})" if r['is_occupied'] else "빈 방 (공실)"
        print(f"• {r['room_number']}호 | 보증금: {r['deposit']:,}원 | 월세: {r['monthly_rent']:,}원 | 상태: {status}")

    # 3. 102호 입주 계약 진행 (UPDATE)
    print("\n--- 102호 신규 입주 계약 ---")
    db.update_tenant(102, tenant_name="파이썬 스튜디오")

    # 4. 101호 퇴거 처리 (VACATE)
    print("\n--- 101호 퇴거 처리 ---")
    db.vacate_room(101)
    