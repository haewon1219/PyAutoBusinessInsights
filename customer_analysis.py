import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

@st.cache_data
def load_data():
    """데이터베이스에서 데이터를 로드합니다."""
    engine = create_engine('mysql+pymysql://root:1024@localhost:3306/resultdb')
    query = "SELECT company_name, converted_amount, number FROM converted_invoices"
    return pd.read_sql(query, engine)

def render_customer_analysis(data):
    """고객사별 KMeans 클러스터링 분석 페이지"""
    st.title('고객사별 매출 분석')

    # 데이터 전처리
    st.subheader("데이터 요약")
    customer_data = data[['company_name', 'converted_amount', 'number']].copy()

    # 'converted_amount'와 'number'를 숫자 데이터로 변환
    customer_data['converted_amount'] = pd.to_numeric(customer_data['converted_amount'], errors='coerce')
    customer_data['number'] = pd.to_numeric(customer_data['number'], errors='coerce')

    # NaN 값 제거
    customer_data = customer_data.dropna(subset=['converted_amount', 'number'])

    # 값이 0 이상인 데이터만 필터링
    customer_data = customer_data[(customer_data['converted_amount'] > 0) & (customer_data['number'] > 0)]

    st.write("전처리된 데이터")
    st.dataframe(customer_data)

    if customer_data.empty:
        st.warning("고객사 데이터가 없습니다. 데이터를 확인해주세요.")
        return

    # 특징 데이터 추출
    X = customer_data[['converted_amount', 'number']]

    # 데이터 스케일링
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # KMeans 클러스터링 수행
    st.subheader("KMeans 클러스터링 분석")
    kmeans = KMeans(n_clusters=3, random_state=42)
    customer_data['cluster'] = kmeans.fit_predict(X_scaled)

    # 클러스터링 결과 요약
    cluster_summary = customer_data.groupby('cluster').agg(
        total_amount=('converted_amount', 'sum'),
        total_invoices=('number', 'sum'),
        customer_count=('company_name', 'nunique')
    ).reset_index()
    st.dataframe(cluster_summary)

    # 시각화
    st.subheader("고객사별 클러스터 시각화")
    fig, ax = plt.subplots(figsize=(10, 6))
    for cluster in customer_data['cluster'].unique():
        cluster_subset = customer_data[customer_data['cluster'] == cluster]
        ax.scatter(
            cluster_subset['converted_amount'],
            cluster_subset['number'],
            label=f'Cluster {cluster}',
            s=100,
            alpha=0.6
        )
    ax.set_xlabel('매출액 (원)')
    ax.set_ylabel('인보이스 수')
    ax.set_title('고객사별 매출 및 인보이스 클러스터링')
    ax.legend()
    st.pyplot(fig)

# Streamlit에서 데이터 로드 및 분석 페이지 호출
data = load_data()
render_customer_analysis(data)
