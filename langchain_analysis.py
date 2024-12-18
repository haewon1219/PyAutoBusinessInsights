import os  # 추가
from dotenv import load_dotenv  # 추가

# .env 파일 로드
load_dotenv()  # 추가
openai_api_key = os.getenv("OPENAI_API_KEY")  # 추가

def analyze_data_with_prompt(dataframe, user_prompt):
    """
    LangChain을 사용하여 데이터 분석.
    """
    from langchain_openai import ChatOpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=800,
        openai_api_key=openai_api_key  # .env에서 불러온 키 사용
    )
    prompt = PromptTemplate(template="{user_prompt}: {stats}")
    chain = LLMChain(llm=llm, prompt=prompt)

    data_stats = dataframe.describe().to_string()
    result = chain.run(stats=data_stats, user_prompt=user_prompt)
    return result
