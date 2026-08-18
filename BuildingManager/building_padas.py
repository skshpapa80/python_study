import sqlite3
import pandas as pd
from datetime import datetime

class BuildingAnalytics:
    def __init__(self, db_name: str = "building_manager.db"):
        self.db_name = db_name

    def get_dataframe(self) -> pd.DataFrame:
        """SQLite 데이터를 Pandas DataFrame으로 불러오기"""
        with sqlite3.connect(self.db_name) as conn:
            query = "SELECT * FROM tenants"
            df = pd.read_sql_query(query, conn)
        return df

    def calculate_monthly_bills(self, utility_data: list[dict], 
                                electricity_rate: float = 120.0, 
                                water_rate: float = 850.0) -> pd.DataFrame:
        """
        호실별 사용량 데이터를 받아 총 청구 금액(월세 + 관리비) 계산
        
        utility_data 예시:
        [{'room_number': 101, 'electricity_kwh': 250, 'water_m3': 15}, ...]
        """
        df = self.get_dataframe()
        
        # 사용량 데이터 프레임 생성 및 기존 입주 정보와 Merge (INNER JOIN)
        util_df = pd.DataFrame(utility_data)
        merged_df = pd.merge(df, util_df, on='room_number', how='left')

        # 공실인 경우 사용량 0 처리
        merged_df['electricity_kwh'] = merged_df['electricity_kwh'].fillna(0)
        merged_df['water_m3'] = merged_df['water_m3'].fillna(0)

        # 개별 공과금 계산 (사용량 * 단가)
        merged_df['electricity_fee'] = merged_df['electricity_kwh'] * electricity_rate
        merged_df['water_fee'] = merged_df['water_m3'] * water_rate
        
        # 기본 공용 관리비 (평당/면적당 계산 가능하지만, 여기선 기본 50,000원 적용)
        merged_df['base_maintenance'] = merged_df['is_occupied'].apply(lambda x: 50000 if x == 1 else 0)

        # 총 관리비 = 기본 관리비 + 전기료 + 수도료
        merged_df['total_maintenance'] = (
            merged_df['base_maintenance'] + 
            merged_df['electricity_fee'] + 
            merged_df['water_fee']
        )

        # 총 청구액 = 월세 + 총 관리비
        merged_df['total_invoice'] = merged_df['monthly_rent'] * merged_df['is_occupied'] + merged_df['total_maintenance']

        return merged_df

    def generate_summary_report(self, billed_df: pd.DataFrame):
        """건물 전체 요약 리포트 출력"""
        total_rooms = len(billed_df)
        occupied_rooms = billed_df['is_occupied'].sum()
        occupancy_rate = (occupied_rooms / total_rooms) * 100 if total_rooms > 0 else 0

        total_rent = billed_df['monthly_rent'] * billed_df['is_occupied']
        total_rent_income = total_rent.sum()
        total_maintenance_income = billed_df['total_maintenance'].sum()
        grand_total = billed_df['total_invoice'].sum()

        print("==========================================")
        print(f"🏢 건물 월간 정산 요약 ({datetime.now().strftime('%Y-%m')})")
        print("==========================================")
        print(f"• 전체 호실 수   : {total_rooms}개")
        print(f"• 입주 호실 수   : {occupied_rooms}개 (가동률: {occupancy_rate:.1f}%)")
        print(f"• 총 월세 수입   : {total_rent_income:,.0f}원")
        print(f"• 총 관리비 수입 : {total_maintenance_income:,.0f}원")
        print(f"------------------------------------------")
        print(f"💰 이번 달 총 청구액 : {grand_total:,.0f}원")
        print("==========================================")

# 🧪 실행 및 테스트 예시
if __name__ == "__main__":
    analytics = BuildingAnalytics()

    # 각 호실별 이번 달 전기(kWh), 수도(m³) 사용량 샘플 데이터
    monthly_utilities = [
        {'room_number': 101, 'electricity_kwh': 320, 'water_m3': 18},
        {'room_number': 102, 'electricity_kwh': 0, 'water_m3': 0},      # 공실
        {'room_number': 201, 'electricity_kwh': 540, 'water_m3': 32},
    ]

    # 관리비 계산 실행
    billed_result = analytics.calculate_monthly_bills(monthly_utilities)

    # 주요 컬럼만 정돈하여 출력
    display_columns = ['room_number', 'tenant_name', 'monthly_rent', 'total_maintenance', 'total_invoice']
    print("\n[📋 호실별 청구 내역]")
    print(billed_result[display_columns].to_string(index=False))

    # 요약 리포트 출력
    print("\n")
    analytics.generate_summary_report(billed_result)

    # 엑셀/CSV 파일로 내보내기
    billed_result.to_csv("monthly_building_report.csv", index=False, encoding="utf-8-sig")
    print("\n📄 'monthly_building_report.csv' 파일로 리포트가 저장되었습니다!")
    