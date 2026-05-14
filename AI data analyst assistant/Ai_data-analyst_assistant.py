import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 AI Data Analyst Assistant")

# Upload file
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# ONLY run after upload
if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Preview
    st.subheader("📌 Dataset Preview")
    st.dataframe(df.head())

    # Dataset info
    st.subheader("📊 Dataset Info")

    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    # Missing values
    st.subheader("❌ Missing Values")

    st.write(df.isnull().sum())

    # ---------------- CHART SECTION ---------------- #

    st.subheader("📈 Interactive Charts")

    numeric_columns = df.select_dtypes(
        include=['number']
    ).columns

    # ---------------- BAR CHART ---------------- #

    st.subheader("📌 Bar Chart")

    x_bar = st.selectbox(
        "Select X-axis",
        df.columns,
        key="bar_x"
    )

    y_bar = st.selectbox(
        "Select Y-axis",
        numeric_columns,
        key="bar_y"
    )

    fig_bar = px.bar(
        df,
        x=x_bar,
        y=y_bar,
        title="Bar Chart"
    )

    st.plotly_chart(
    fig_bar,
    key="bar_chart"
    )

    # ---------------- PIE CHART ---------------- #

    st.subheader("🥧 Pie Chart")

    pie_column = st.selectbox(
        "Select Column",
        df.columns,
        key="pie"
    )

    pie_data = df[pie_column].value_counts().reset_index()

    pie_data.columns = [pie_column, "count"]

    fig_pie = px.pie(
        pie_data,
        names=pie_column,
        values="count",
        title="Pie Chart"
    )

    st.plotly_chart(
    fig_pie,
    key="pie_chart"
    )

    # ---------------- HISTOGRAM ---------------- #

    st.subheader("📊 Histogram")

    hist_column = st.selectbox(
        "Select Histogram Column",
        numeric_columns,
        key="hist"
    )

    fig_hist = px.histogram(
        df,
        x=hist_column,
        title="Histogram"
    )

    st.plotly_chart(
    fig_hist,
    key="hist_chart"
    )

    # ---------------- SCATTER PLOT ---------------- #

    st.subheader("🔵 Scatter Plot")

    x_scatter = st.selectbox(
        "Select Scatter X-axis",
        numeric_columns,
        key="scatter_x"
    )

    y_scatter = st.selectbox(
        "Select Scatter Y-axis",
        numeric_columns,
        key="scatter_y"
    )

    fig_scatter = px.scatter(
        df,
        x=x_scatter,
        y=y_scatter,
        title="Scatter Plot"
    )

    st.plotly_chart(
    fig_scatter,
    key="scatter_chart"
    )

    # ---------------- HEATMAP ---------------- #

    st.subheader("🔥 Correlation Heatmap")

    corr = df[numeric_columns].corr()

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        ax=ax
    )

    st.pyplot(
    fig,
    clear_figure=True
    )