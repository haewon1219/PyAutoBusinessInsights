import streamlit as st
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI
import os  # 추가
from dotenv import load_dotenv  # 추가

# .env 파일 로드
load_dotenv()  # 추가
openai_api_key = os.getenv("OPENAI_API_KEY")  # 추가

def render_dashboard(data):
    """대시보드 페이지를 렌더링합니다."""
    st.title('대시보드')

    # 사이드바에 고객별 필터 추가
    st.sidebar.header("데이터 필터")
    selected_customer = st.sidebar.selectbox(
        "고객별 필터",
        options=data['company_name'].unique(),
        index=0
    )

    # 고객별 데이터 필터링
    filtered_data = data[data['company_name'] == selected_customer]

    # 월별 매출 추이 시각화
    st.subheader("월별 매출 추이")
    monthly_sales = (
        filtered_data.groupby(filtered_data['date'].dt.to_period('M'))['converted_amount']
        .sum()
        .reset_index()
    )
    if not monthly_sales.empty:
        # 매출 추이 그래프 생성
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(monthly_sales['date'].astype(str), monthly_sales['converted_amount'], marker='o', linestyle='-', color='blue')
        ax.set_title(f'{selected_customer} - 월별 매출 추이')
        ax.set_xlabel('월')
        ax.set_ylabel('매출액 (원)')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # OpenAI를 활용한 인사이트 생성
        st.subheader("매출 추이에 대한 인사이트")
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=400,
            openai_api_key=openai_api_key
        )
        
        # 데이터 통계를 기반으로 프롬프트 생성
        prompt = f"""
        다음 데이터는 {selected_customer}의 2024년 1월부터 10월까지의 월별 매출 데이터입니다:
        {monthly_sales.to_string(index=False)}

        위 데이터를 기반으로, 월별 매출 추이에 대한 중요한 비즈니스 인사이트를 간결히 3줄로 도출하세요.
        """
        
        try:
            # OpenAI API 호출
            response = llm(prompt)
            
            # 응답에서 텍스트 추출
            content = response.content  # AIMessage 객체의 content 속성에 응답 텍스트가 저장됩니다.

            if content:
                # 줄 단위로 나누고 첫 3줄만 추출
                insights = content.strip().split('\n')[:3]
                for i, insight in enumerate(insights, 1):
                    st.write(f"{i}. {insight.strip()}")
            else:
                st.warning("OpenAI API 응답이 비어 있습니다. 프롬프트를 확인하거나 데이터 양을 조정하세요.")
        except Exception as e:
            st.error(f"OpenAI API를 통해 인사이트를 생성하는 데 실패했습니다: {e}")
    else:
        st.warning(f"{selected_customer}의 매출 데이터가 없습니다.")
