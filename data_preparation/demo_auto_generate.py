import time
import pandas as pd
import sys
import os
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from data_generation.generate_fake_sales_data import generate_fake_data
from data_preparation.clean_data import clean_sales_data
from data_pipeline.data_pipeline import transform_data

engine = create_engine('postgresql://postgres:094189@localhost:5432/salesdb')

# Ngày bắt đầu sinh dữ liệu từ file CSV
csv_path = os.path.join(BASE_DIR, 'data_pipeline', 'processed_sales_data.csv')

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df['orderdate'] = pd.to_datetime(df['orderdate'])
    last_date = df['orderdate'].max().date()
    current_date = datetime.combine(last_date + timedelta(days=1), datetime.min.time())
    print(f"Khởi tạo ngày bắt đầu sinh dữ liệu là: {current_date.date()}")
else:
    current_date = datetime(2025, 7, 1)
    print("Chưa có file processed_sales_data.csv. Bắt đầu từ 2025-07-01.")

def append_new_sales(order_date):
    try:
        # 1. init data
        raw_data = generate_fake_data(num_records=random.randint(300, 600), override_date=order_date)

        # 2. clean data
        cleaned_data = clean_sales_data(raw_data)

        # 3. save db
        cleaned_data.columns = [col.lower() for col in cleaned_data.columns]
        cleaned_data.to_sql('sales_data', engine, index=False, if_exists='append')
        print(f"Đã thêm dữ liệu cho ngày {order_date.strftime('%Y-%m-%d')}")
    except Exception as e:
        print(f"Lỗi khi thêm vào CSDL: {e}")
        return

    try:
        # 4. update processed_sales_data.csv
        df = pd.read_sql("SELECT * FROM sales_data", engine)
        transformed_df = transform_data(df)
        output_path = os.path.join(BASE_DIR, 'data_pipeline', 'processed_sales_data.csv')
        transformed_df.to_csv(output_path, index=False)
        print("Đã cập nhật lại processed_sales_data.csv.")
        print("=" * 60)
    except Exception as e:
        print(f"Lỗi khi cập nhật processed_sales_data.csv: {e}")

if __name__ == "__main__":
    print("Bắt đầu sinh dữ liệu mỗi 10 giây (1 ngày mới).")
    try:
        while True:
            append_new_sales(order_date=current_date)
            current_date += timedelta(days=1)
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nĐã dừng sinh dữ liệu.")