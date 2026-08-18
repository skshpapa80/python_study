import streamlit as st
import pandas as pd
import sqlite3

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="파이썬 타워 관리 시스템",
    page_icon="🏢",
    layout="wide"
)

DB_NAME = "building_manager.db"

# 데이터베이스 연결 함수
def get_connection():
    return sqlite3.connect(DB_NAME)

# 전체 데이터 로드 함수
def load_data():
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM tenants ORDER BY room_number ASC", conn)
    return df

# 메인 타이틀
st.title("🏢 파이썬 타워 통합 관리 대시보드")
st.caption("내 손으로 만드는 스마트 빌딩 관리 시스템 v1.0")
st.markdown("---")

# 데이터 로드
df = load_data()

# 사이드바 메뉴 구성
st.sidebar.header("📌 메뉴 선택")
menu = st.sidebar.radio("원하는 작업을 선택하세요:", ["📊 대시보드 개요", "📝 입주사 계약/퇴거", "💰 관리비 정산기"])

# -------------------------------------------------------------
# [메뉴 1] 대시보드 개요
# -------------------------------------------------------------
if menu == "📊 대시보드 개요":
    st.subheader("💡 건물 운영 현황 요약")

    # 핵심 KPI 지표 카드 (4열 배치)
    col1, col2, col3, col4 = st.columns(4)
    
    total_rooms = len(df)
    occupied_rooms = int(df['is_occupied'].sum()) if total_rooms > 0 else 0
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    total_expected_rent = int((df['monthly_rent'] * df['is_occupied']).sum())

    col1.metric("전체 호실 수", f"{total_rooms}개")
    col2.metric("입주 호실", f"{occupied_rooms}개")
    col3.metric("가동률 (입주율)", f"{occupancy_rate:.1f}%")
    col4.metric("월 임대 수입", f"{total_expected_rent:,}원")

    st.markdown("---")

    # 테이블 및 차트 영역 (2열 배치)
    col_left, col_right = st.columns([6, 4])

    with col_left:
        st.subheader("📋 전체 호실 목록 및 상태")
        display_df = df.copy()
        display_df['상태'] = display_df['is_occupied'].apply(lambda x: "🟢 입주중" if x == 1 else "🔴 공실")
        display_df['tenant_name'] = display_df['tenant_name'].fillna("-")
        
        # 보기 쉽게 컬럼명 변경
        renamed_df = display_df.rename(columns={
            'room_number': '호수',
            'tenant_name': '입주사명',
            'deposit': '보증금(원)',
            'monthly_rent': '월세(원)'
        })
        
        st.dataframe(
            renamed_df[['호수', '입주사명', '보증금(원)', '월세(원)', '상태']],
            use_container_width=True,
            hide_index=True
        )

    with col_right:
        st.subheader("📊 호실별 월세 현황")
        st.bar_chart(df.set_index('room_number')['monthly_rent'])

# -------------------------------------------------------------
# [메뉴 2] 입주사 계약 및 퇴거 관리
# -------------------------------------------------------------
elif menu == "📝 입주사 계약/퇴거":
    st.subheader("✍️ 입주 계약 및 퇴거 처리")

    tab1, tab2 = st.tabs(["신규 입주 계약", "퇴거 처리"])

    with tab1:
        st.write("빈 방에 새로운 입주사를 등록합니다.")
        vacant_rooms = df[df['is_occupied'] == 0]['room_number'].tolist()

        if not vacant_rooms:
            st.success("🎉 현재 모든 호실이 만실입니다!")
        else:
            with st.form("contract_form"):
                selected_room = st.selectbox("입주할 호수를 선택하세요", vacant_rooms)
                tenant_name = st.text_input("입주사 (회사/임차인 이름)")
                submitted = st.form_submit_button("계약 등록하기")

                if submitted:
                    if not tenant_name.strip():
                        st.error("입주사 이름을 입력해 주세요!")
                    else:
                        with get_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE tenants SET tenant_name = ?, is_occupied = 1 WHERE room_number = ?",
                                (tenant_name, selected_room)
                            )
                            conn.commit()
                        st.success(f"✅ {selected_room}호에 '{tenant_name}' 입주 계약이 완료되었습니다!")
                        st.rerun()

    with tab2:
        st.write("퇴거하는 호실의 정보를 공실로 전환합니다.")
        occupied_rooms = df[df['is_occupied'] == 1]['room_number'].tolist()

        if not occupied_rooms:
            st.info("현재 입주 중인 호실이 없습니다.")
        else:
            with st.form("vacate_form"):
                selected_vacate_room = st.selectbox("퇴거할 호수를 선택하세요", occupied_rooms)
                submitted_vacate = st.form_submit_button("퇴거 처리하기")

                if submitted_vacate:
                    with get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE tenants SET tenant_name = NULL, is_occupied = 0 WHERE room_number = ?",
                            (selected_vacate_room,)
                        )
                        conn.commit()
                    st.warning(f"🚪 {selected_vacate_room}호가 퇴거 처리되어 공실이 되었습니다.")
                    st.rerun()

# -------------------------------------------------------------
# [메뉴 3] 월간 관리비 정산기
# -------------------------------------------------------------
elif menu == "💰 관리비 정산기":
    st.subheader("⚡ 이번 달 공과금 및 관리비 산정")

    st.info("각 호실별 전기/수도 사용량을 입력하면 총 청구 금액이 자동 계산됩니다.")

    occupied_df = df[df['is_occupied'] == 1]

    if len(occupied_df) == 0:
        st.warning("현재 입주 중인 호실이 없어 관리비를 정산할 수 없습니다.")
    else:
        # 사용량 입력을 위한 Form 구성
        with st.form("utility_form"):
            st.markdown("#### 🔌 호실별 사용량 입력")
            
            utility_inputs = []
            for _, row in occupied_df.iterrows():
                col_r, col_e, col_w = st.columns([2, 4, 4])
                col_r.write(f"**{row['room_number']}호** ({row['tenant_name']})")
                e_val = col_e.number_input(f"{row['room_number']}호 전기(kWh)", min_value=0, value=200, key=f"e_{row['room_number']}")
                w_val = col_w.number_input(f"{row['room_number']}호 수도(m³)", min_value=0, value=15, key=f"w_{row['room_number']}")
                
                utility_inputs.append({
                    'room_number': row['room_number'],
                    'tenant_name': row['tenant_name'],
                    'monthly_rent': row['monthly_rent'],
                    'electricity_kwh': e_val,
                    'water_m3': w_val
                })

            calc_button = st.form_submit_button("⚡ 관리비 및 월세 자동 정산하기")

        if calc_button:
            result_df = pd.DataFrame(utility_inputs)
            
            # 단가 적용 계산 (전기 120원/kWh, 수도 850원/m³, 기본관리비 50,000원)
            result_df['전기료'] = result_df['electricity_kwh'] * 120
            result_df['수도료'] = result_df['water_m3'] * 850
            result_df['기본관리비'] = 50000
            result_df['총관리비'] = result_df['기본관리비'] + result_df['전기료'] + result_df['수도료']
            result_df['최종청구액'] = result_df['monthly_rent'] + result_df['총관리비']

            st.success("🎉 정산이 완료되었습니다!")
            st.markdown("### 📄 이번 달 최종 청구 내역서")
            
            # 화면에 내역서 표시
            st.dataframe(
                result_df[['room_number', 'tenant_name', 'monthly_rent', '총관리비', '최종청구액']].rename(columns={
                    'room_number': '호수', 'tenant_name': '입주사명', 'monthly_rent': '월세'
                }),
                use_container_width=True,
                hide_index=True
            )

            # CSV 내보내기 버튼 제공
            csv_data = result_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 엑셀(CSV) 청구서 다운로드",
                data=csv_data,
                file_name="monthly_invoice_report.csv",
                mime="text/csv"
            )
            