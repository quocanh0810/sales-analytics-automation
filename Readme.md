# Sales Analytics Dashboard - Real-Time Simulation with Streamlit

## Cài đặt môi trường

```bash
# 1. Tạo virtual environment
python3 -m venv env
source env/bin/activate

# 2. Cài đặt các thư viện cần thiết
pip install pandas sqlalchemy psycopg2-binary streamlit faker plotly altair streamlit-autorefresh
```

---

## Khởi động PostgreSQL

Mở terminal mới và chạy:
```bash
/Library/PostgreSQL/17/bin/pg_ctl -D /Library/PostgreSQL/17/data start
psql -U postgres
CREATE DATABASE salesdb;
psql -U postgres -d salesdb -f /path/to/schema_salesdb.sql
```

---

## Các bước chạy hệ thống

### 1️ Train mô hình dự đoán doanh thu

```bash
cd model
python3 train_model.py
```

> Sinh file `random_forest_sales.pkl` và `product_encoder.pkl` để dùng trong bước sinh dữ liệu.

---

### 2️ Sinh dữ liệu giả lập ban đầu

```bash
python3 data_generation/generate_fake_sales_data.py
```

> Output: `data_generation/fake_sales_data.csv`

---

### 3️ Làm sạch dữ liệu thủ công (nếu cần)

```bash
# Chạy hết file data_preparation.ipynb để clean dữ liệu
Jupyter Notebook: data_preparation/data_preparation.ipynb
```

> Input: `fake_sales_data.csv`  
> Output: `cleaned_sales_data.csv`

---

### 4️ Load dữ liệu vào PostgreSQL

```bash
python3 data_preparation/load_to_db.py
```

---

### 5️ Chạy pipeline ETL

```bash
python3 data_pipeline/data_pipeline.py
```

> Tạo file `processed_sales_data.csv` xử lý để hiển thị lên dashboard

---

### 6️ Sinh dữ liệu tự động theo ngày

Mỗi 10 giây hệ thống sẽ tự động sinh dữ liệu cho ngày tiếp theo và cập nhật dashboard.

```bash
python3 data_preparation/demo_auto_generate.py
```

---

### 7️ Chạy Dashboard

```bash
cd dashboard
streamlit run app.py
```

## Cấu trúc thư mục

```
.
├── model/                      # Model RandomForest và encoder
│   ├── train_model.py
│   └── *.pkl
├── data_generation/           # Sinh dữ liệu giả
│   └── generate_fake_sales_data.py
├── data_preparation/          # Làm sạch, xử lý dữ liệu
│   ├── clean_data.py
│   ├── load_to_db.py
│   └── demo_auto_generate.py
├── data_pipeline/             # Tạo file phân tích cho dashboard
│   └── data_pipeline.py
├── dashboard/                 # Giao diện hiển thị Streamlit
│   └── app.py
├── data_pipeline/processed_sales_data.csv
├── PT_NVTM.docx               # Báo cáo
└── README.md
```


## Dashboard hiển thị các thông tin

- Tổng doanh thu hôm nay
- Doanh thu theo dòng sản phẩm
- Doanh thu theo phương thức thanh toán
- Biểu đồ biến động doanh thu 5 ngày gần nhất
- Tổng doanh thu theo quý

