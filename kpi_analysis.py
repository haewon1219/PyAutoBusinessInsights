import streamlit as st

def calculate_kpi(dataframe):
    """
    데이터프레임에서 KPI를 계산.
    """
    total_amount = dataframe['converted_amount'].sum()
    total_invoices = dataframe['number'].nunique()
    total_amount_rounded = round(total_amount / 1e8, 2)  # 억 단위로 변환
    return total_amount_rounded, total_invoices


def display_kpi(total_amount_rounded, total_invoices):
    """
    계산된 KPI를 Streamlit을 통해 표시.
    """
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label="총 인보이스 금액 (원화 기준)", value=f"{total_amount_rounded} 억 원")
    kpi2.metric(label="총 인보이스 수", value=total_invoices)
