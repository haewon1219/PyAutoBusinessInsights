import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from database import load_data
from kpi_analysis import calculate_kpi, display_kpi
from langchain_analysis import analyze_data_with_prompt
from dashboard import render_dashboard
import matplotlib.pyplot as plt
from matplotlib import rc
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()  # 추가
openai_api_key = os.getenv("OPENAI_API_KEY")

# 한글 폰트 설정
rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# Streamlit 앱 설정
st.set_page_config(page_title="세일즈 성과 분석", layout="wide")

# MySQL 데이터베이스 연결 설정
resultdb_engine = create_engine('mysql+pymysql://root:1024@localhost:3306/resultdb')

# 데이터 로드
converted_invoices_query = "SELECT * FROM converted_invoices"
converted_invoices_df = load_data(resultdb_engine, converted_invoices_query)

# 날짜 컬럼을 datetime 형식으로 변환
converted_invoices_df['date'] = pd.to_datetime(converted_invoices_df['date'], errors='coerce')
converted_invoices_df = converted_invoices_df.dropna(subset=['date'])  # 유효하지 않은 날짜 제거

if converted_invoices_df.empty:
    st.warning('데이터가 제공되지 않아 분석 및 시각화를 수행할 수 없습니다. 데이터를 확인해주세요.')
else:
    # 페이지 설정
    page = st.sidebar.selectbox("페이지 선택", ["KPI 분석 및 인사이트", "대시보드"])

    if page == "KPI 분석 및 인사이트":
        st.title('세일즈 성과 분석 및 주요 인사이트')

        # KPI 계산 및 표시
        total_amount_rounded, total_invoices = calculate_kpi(converted_invoices_df)
        display_kpi(total_amount_rounded, total_invoices)

        # 데이터 테이블 표시
        st.subheader('전체 데이터')
        st.dataframe(converted_invoices_df)

        # 사용자 프롬프트 입력
        user_prompt = st.text_input('원하는 인사이트를 입력하세요')

        if st.button('분석 실행'):
            if user_prompt:
                try:
                    analysis_result = analyze_data_with_prompt(converted_invoices_df, user_prompt)
                    st.subheader('분석 결과')
                    st.write(analysis_result)
                except Exception as e:
                    st.error(f"분석 중 오류가 발생했습니다: {e}")
            else:
                st.warning('분석을 위해 프롬프트를 입력해주세요.')

    elif page == "대시보드":
        render_dashboard(converted_invoices_df)
