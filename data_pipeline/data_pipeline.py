import pandas as pd
from sqlalchemy import create_engine
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

engine = create_engine('postgresql://postgres:094189@localhost:5432/salesdb')

def extract_data():
    try:
        query = "SELECT * FROM sales_data"
        df = pd.read_sql(query, engine)
        print("Trích xuất dữ liệu thành công.")
        return df
    except Exception as e:
        print(f"Lỗi khi trích xuất dữ liệu: {e}")
        return None

def transform_data(df):
    try:
        date_col = next((col for col in df.columns if col.lower() == 'orderdate'), None)

        if not date_col:
            raise ValueError("Không tìm thấy cột 'orderdate' trong dữ liệu!")

        df['orderdate'] = pd.to_datetime(df[date_col])

        # Tạo thêm các cột phân tích
        df['year_month'] = df['orderdate'].dt.to_period('M').astype(str)
        df['quarter'] = df['orderdate'].dt.quarter

        print("Dữ liệu đã được chuyển đổi.")
        return df
    except Exception as e:
        print(f"Lỗi khi xử lý dữ liệu: {e}")
        return None

def load_data(df):
    try:
        output_path = os.path.join(BASE_DIR, 'data_pipeline', 'processed_sales_data.csv')
        df.to_csv(output_path, index=False)
        print(f"Dữ liệu đã được lưu tại: {output_path}")
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu: {e}")

if __name__ == "__main__":
    data = extract_data()
    if data is not None:
        processed_data = transform_data(data)
        if processed_data is not None:
            load_data(processed_data)