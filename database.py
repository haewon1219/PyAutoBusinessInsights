import pandas as pd
from sqlalchemy import create_engine

def load_data(engine, query):
    """
    데이터베이스에서 데이터를 로드.
    """
    try:
        dataframe = pd.read_sql(query, engine)
        return dataframe
    except Exception as e:
        raise Exception(f"데이터 로드 중 오류가 발생했습니다: {e}")
