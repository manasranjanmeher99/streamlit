import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Title
st.title("📊 Sales Analytics Dashboard")

# Load Data
df = pd.read_csv(r"D:\python\streamlit\sales_data.csv")

# Convert Date Column

df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

# Sidebar Filters
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Filter Data
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# KPIs
total_sales = df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df.shape[0]

# KPI Columns
col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹{total_sales}")
col2.metric("📈 Total Profit", f"₹{total_profit}")
col3.metric("🛒 Total Orders", total_orders)

st.markdown("---")

# Sales Trend Chart
st.subheader("📅 Monthly Sales Trend")

sales_trend = filtered_df.groupby("Date")["Sales"].sum().reset_index()

fig1 = px.line(
    sales_trend,
    x="Date",
    y="Sales",
    title="Sales Over Time"
)

st.plotly_chart(fig1, use_container_width=True)

# Top Products
st.subheader("🏆 Top Products")

product_sales = filtered_df.groupby("Product")["Sales"].sum().reset_index()

fig2 = px.bar(
    product_sales,
    x="Product",
    y="Sales",
    title="Product Sales"
)

st.plotly_chart(fig2, use_container_width=True)

# Region-wise Sales
st.subheader("🌍 Region-wise Sales")

region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig3 = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    title="Sales by Region"
)

st.plotly_chart(fig3, use_container_width=True)

# Show Dataset
st.subheader("📄 Sales Data")

st.dataframe(filtered_df)