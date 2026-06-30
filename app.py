import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Data Analyst Pro",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Data Analyst Pro")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("CSV uploaded successfully!")

    st.subheader("Dataset Shape")
    st.write(f"**Number of rows:** {len(df)}")
    st.write(f"**Number of columns:** {len(df.columns)}")

    st.subheader("Column Names")
    st.write(list(df.columns))

    st.subheader("Data Types")
    st.write(df.dtypes)

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    st.subheader("Summary Statistics")
    st.dataframe(df.describe())

    st.subheader("First 5 Rows")
    st.dataframe(df.head())

else:
    st.write("Please upload a CSV file.")