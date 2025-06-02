import pandas as pd
from sqlalchemy import create_engine

file_path = '../data_generation/cleaned_sales_data.csv'
df = pd.read_csv(file_path, encoding='ISO-8859-1')

df.columns = map(str.lower, df.columns)

engine = create_engine('postgresql://postgres:094189@localhost:5432/salesdb')

try:
    df.to_sql('sales_data', engine, index=False, if_exists='append')
    print("Nạp dữ liệu vào bảng sales_data thành công.")
except Exception as e:
    print(f"Lỗi khi nạp dữ liệu: {str(e)}")