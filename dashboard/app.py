import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# auto-refresh dashboard 10s
st_autorefresh(interval=10000, limit=None, key="refresh")

# config cache
@st.cache_data(ttl=5)
def load_processed_data():
    return pd.read_csv('../data_pipeline/processed_sales_data.csv')

df = load_processed_data()
df['orderdate'] = pd.to_datetime(df['orderdate'])

latest_date = df['orderdate'].max().date()
previous_date = latest_date - pd.Timedelta(days=1)

# Lọc dữ liệu theo ngày
today_df = df[df['orderdate'].dt.date == latest_date].copy()
yesterday_df = df[df['orderdate'].dt.date == previous_date].copy()

st.title("Dashboard Doanh Thu")

# 1. Tổng doanh thu hôm nay
today_sales = today_df['sales'].sum()
yesterday_sales = yesterday_df['sales'].sum()
delta = today_sales - yesterday_sales
st.metric("Doanh thu hôm nay", f"${today_sales:,.0f}", delta=f"{delta:,.0f}")

# 2. Doanh thu theo Dòng sản phẩm hôm nay
st.subheader("Doanh thu hôm nay theo Dòng Sản phẩm")
product_today = today_df.groupby('productline')['sales'].sum().reset_index().sort_values(by='sales', ascending=True)

bar_today = alt.Chart(product_today).mark_bar().encode(
    y='productline',
    x='sales',
    color='productline'
).properties(title=f"Tổng Doanh thu theo Dòng Sản phẩm - {latest_date}")
st.altair_chart(bar_today, use_container_width=True)

# 3. Doanh thu theo Ngày
st.subheader("Doanh thu theo Ngày (2 ngày gần nhất)")
recent_days = df[(df['orderdate'].dt.date >= latest_date - pd.Timedelta(days=3)) &
                 (df['orderdate'].dt.date <= latest_date)]

daily_sales = recent_days.groupby('orderdate')['sales'].sum().reset_index()
daily_sales.columns = ['Ngày', 'Doanh thu']
max_sales = daily_sales['Doanh thu'].max()

line_chart = alt.Chart(daily_sales).mark_line(point=True).encode(
    x=alt.X('Ngày:T', title='Ngày'),
    y=alt.Y('Doanh thu:Q', scale=alt.Scale(domain=[0, max_sales + 50000]))
).properties(title=f"Doanh thu từ {daily_sales['Ngày'].min().date()} đến {daily_sales['Ngày'].max().date()}")
st.altair_chart(line_chart, use_container_width=True)

# 4. Phân phối Phương thức Thanh toán hôm nay
st.subheader("Phân phối Phương thức Thanh toán hôm nay")
payment_count = today_df['paymentmethod'].value_counts().reset_index()
payment_count.columns = ['paymentmethod', 'count']
fig = px.pie(payment_count, values='count', names='paymentmethod',
             title=f"Tỷ lệ Phương thức Thanh toán - {latest_date}",
             hole=0.3)
fig.update_traces(textinfo='percent+label')
st.plotly_chart(fig)

# 5. Doanh thu theo Phương thức Thanh toán
st.subheader("Doanh thu theo Phương thức Thanh toán hôm nay")
order = ['Credit Card', 'PayPal', 'Bank Transfer', 'Cash']
today_df.loc[:, 'paymentmethod'] = pd.Categorical(today_df['paymentmethod'], categories=order, ordered=True)
payment_sales = today_df.groupby('paymentmethod', observed=False)['sales'].sum().reset_index()

bar_payment = alt.Chart(payment_sales).mark_bar().encode(
    x='paymentmethod',
    y='sales',
    color='paymentmethod'
).properties(title="Doanh thu theo Phương thức Thanh toán")
st.altair_chart(bar_payment, use_container_width=True)

# 6. Doanh thu theo Quý
st.subheader("Doanh thu theo Quý")
quarterly_sales = df.groupby('quarter', observed=False)['sales'].sum().reset_index()
quarterly_sales.columns = ['Quý', 'Doanh thu']
st.dataframe(quarterly_sales.style.format({'Doanh thu': '{:,.0f}'}))

bar_quarter = alt.Chart(quarterly_sales).mark_bar().encode(
    x='Quý:O',
    y='Doanh thu:Q',
    color='Quý:O'
).properties(title="Tổng Doanh thu theo Quý")
st.altair_chart(bar_quarter, use_container_width=True)