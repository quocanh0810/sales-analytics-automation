import pandas as pd
import joblib
import os
from faker import Faker
import random
from datetime import datetime
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
model_path = os.path.join(BASE_DIR, 'model', 'random_forest_sales.pkl')
encoder_path = os.path.join(BASE_DIR, 'model', 'product_encoder.pkl')

model = joblib.load(model_path)
product_encoder = joblib.load(encoder_path)

fake = Faker()

# Sinh dữ liệu
def generate_fake_data(num_records, override_date=None):
    data = []
    used_order_numbers = set()

    for _ in range(num_records):
        while True:
            order_number = random.randint(10000, 30000)
            if order_number not in used_order_numbers:
                used_order_numbers.add(order_number)
                break

        product_line = random.choices(
            ['Motorcycles', 'Classic Cars', 'Trucks and Buses', 'Vintage Cars', 'Planes', 'Ships', 'Trains'],
            weights=[30, 25, 15, 5, 5, 10, 10], k=1
        )[0]

        if product_line == 'Motorcycles':
            price_each = round(random.uniform(40, 80), 2)
            quantity_ordered = random.randint(30, 60)
        elif product_line == 'Classic Cars':
            price_each = round(random.uniform(60, 120), 2)
            quantity_ordered = random.randint(20, 50)
        elif product_line == 'Trucks and Buses':
            price_each = round(random.uniform(50, 90), 2)
            quantity_ordered = random.randint(50, 100)
        elif product_line == 'Planes':
            price_each = round(random.uniform(100, 200), 2)
            quantity_ordered = random.randint(5, 15)
        elif product_line == 'Ships':
            price_each = round(random.uniform(80, 150), 2)
            quantity_ordered = random.randint(5, 20)
        elif product_line == 'Trains':
            price_each = round(random.uniform(20, 50), 2)
            quantity_ordered = random.randint(10, 30)
        else:
            price_each = round(random.uniform(80, 130), 2)
            quantity_ordered = random.randint(5, 10)

        order_line_number = random.randint(1, 10)

        # Ngày đặt hàng
        if override_date:
            order_date = override_date.date()
        else:
            order_date = fake.date_between(datetime(2025, 1, 1), datetime(2025, 6, 30))

        year_id = order_date.year
        month_id = order_date.month
        qtr_id = (month_id - 1) // 3 + 1

        # Dự đoán SALES
        product_encoded = product_encoder.transform([product_line])[0]
        raw_sales = model.predict([[quantity_ordered, price_each, product_encoded, month_id]])[0]
        sales = round(max(0, float(raw_sales)), 2)

        status = random.choices(
            ['Shipped', 'Cancelled', 'In Process', 'Resolved', 'On Hold'],
            weights=[50, 10, 20, 10, 10], k=1
        )[0]

        payment_method = random.choices(
            ['Credit Card', 'PayPal', 'Bank Transfer', 'Cash'],
            weights=[40, 30, 20, 10], k=1
        )[0]

        msrp = round(price_each * random.uniform(0.8, 1.2), 2)
        product_code = f"S{random.randint(10, 99)}_{random.randint(1000, 9999)}"

        customer_name = fake.company()
        phone = fake.phone_number()
        address1 = fake.street_address()
        address2 = fake.secondary_address()
        city = fake.city()
        state = fake.state_abbr()
        postal_code = fake.zipcode()
        country = fake.country()
        territory = random.choice(['NA', 'EMEA', 'APAC', 'LATAM'])
        contact_last_name = fake.last_name()
        contact_first_name = fake.first_name()
        deal_size = 'Small' if sales < 2000 else ('Medium' if sales < 5000 else 'Large')

        data.append([
            order_number, quantity_ordered, price_each, order_line_number, sales,
            order_date, status, qtr_id, month_id, year_id, product_line, msrp, product_code,
            customer_name, phone, address1, address2, city, state, postal_code, country, territory,
            contact_last_name, contact_first_name, deal_size, payment_method
        ])

    df = pd.DataFrame(data, columns=[
        'ORDERNUMBER', 'QUANTITYORDERED', 'PRICEEACH', 'ORDERLINENUMBER', 'SALES',
        'ORDERDATE', 'STATUS', 'QTR_ID', 'MONTH_ID', 'YEAR_ID', 'PRODUCTLINE', 'MSRP', 'PRODUCTCODE',
        'CUSTOMERNAME', 'PHONE', 'ADDRESSLINE1', 'ADDRESSLINE2', 'CITY', 'STATE', 'POSTALCODE',
        'COUNTRY', 'TERRITORY', 'CONTACTLASTNAME', 'CONTACTFIRSTNAME', 'DEALSIZE', 'PAYMENTMETHOD'
    ])
    return df

if __name__ == "__main__":
    num_records = 10000
    df = generate_fake_data(num_records)
    output_path = os.path.join(BASE_DIR, 'data_generation', 'fake_sales_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Đã tạo {num_records} dòng dữ liệu và lưu vào {output_path}")