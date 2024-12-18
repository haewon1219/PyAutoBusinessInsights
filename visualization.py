import streamlit as st
import matplotlib.pyplot as plt

def visualize_sales_trends(user_prompt, dataframe):
    """
    사용자 프롬프트에 따라 데이터프레임의 데이터를 시각화.
    """
    import re

    month_match = re.findall(r'(\d+)월', user_prompt)
    if month_match:
        months = [int(month) for month in month_match]
        st.subheader(f"{' '.join(month_match)}월 세일즈 금액 추이")
        month_data = dataframe[dataframe['date'].dt.month.isin(months)]
        if not month_data.empty:
            monthly_sales = month_data.groupby(month_data['date'].dt.day)['converted_amount'].sum().reset_index()
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(monthly_sales['date'], monthly_sales['converted_amount'], marker='o', linestyle='-', color='blue')
            ax.set_title(f"{' '.join(month_match)}월 Sales Trend")
            ax.set_xlabel('Day of Month')
            ax.set_ylabel('Total Sales Amount (원)')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning(f"{' '.join(month_match)}월 데이터가 없습니다. 데이터를 확인해주세요.")
