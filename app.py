import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Data Analyst Pro",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Data Analyst Pro")
st.markdown("Upload a CSV file to explore and clean your dataset.")

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

# -----------------------------
# Load Dataset into Session State
# -----------------------------
if uploaded_file is not None:

    if (
        "uploaded_file_name" not in st.session_state
        or st.session_state.uploaded_file_name != uploaded_file.name
    ):
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.df = pd.read_csv(uploaded_file)

    df = st.session_state.df

    # -----------------------------
    # Success Message
    # -----------------------------
    st.success("✅ CSV uploaded successfully!")

    # -----------------------------
    # Dataset Shape
    # -----------------------------
    st.subheader("📐 Dataset Shape")

    st.write(f"**Number of Rows:** {df.shape[0]}")
    st.write(f"**Number of Columns:** {df.shape[1]}")

    # -----------------------------
    # Column Names
    # -----------------------------
    st.subheader("📝 Column Names")

    st.write(list(df.columns))

    # -----------------------------
    # Data Types
    # -----------------------------
    st.subheader("🔎 Data Types")

    st.dataframe(df.dtypes.astype(str).reset_index().rename(
        columns={
            "index": "Column",
            0: "Data Type"
        }
    ))

    # -----------------------------
    # Missing Values
    # -----------------------------
    st.subheader("❗ Missing Values")

    missing_values = df.isnull().sum()

    st.dataframe(
        missing_values.reset_index().rename(
            columns={
                "index": "Column",
                0: "Missing Values"
            }
        )
    )

    # -----------------------------
    # Summary Statistics
    # -----------------------------
    st.subheader("📊 Summary Statistics")

    st.dataframe(df.describe(include="all"))

    # -----------------------------
    # First Five Rows
    # -----------------------------
    st.subheader("👀 First 5 Rows")

    st.dataframe(df.head())

    # ======================================================
    # DATA QUALITY DASHBOARD
    # ======================================================

    st.markdown("---")
    st.header("🧹 Data Quality Dashboard")

    # Duplicate Rows
    duplicate_rows = df.duplicated().sum()

    st.write(f"**Duplicate Rows:** {duplicate_rows}")

    # Missing Percentage
    st.subheader("Missing Percentage by Column")

    missing_percentage = (
        (df.isnull().sum() / len(df)) * 100
    ).round(2)

    st.dataframe(
        missing_percentage.reset_index().rename(
            columns={
                "index": "Column",
                0: "Missing %"
            }
        )
    )

    # Unique Values
    st.subheader("Unique Values")

    unique_values = df.nunique()

    st.dataframe(
        unique_values.reset_index().rename(
            columns={
                "index": "Column",
                0: "Unique Values"
            }
        )
    )

    # Memory Usage
    memory_kb = df.memory_usage(deep=True).sum() / 1024

    st.write(f"**Total Memory Usage:** {memory_kb:.2f} KB")

    # -----------------------------
    # Cleaning Buttons
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Remove Duplicates"):
            st.session_state.df = df.drop_duplicates()
            st.success("Duplicate rows removed.")
            st.rerun()

    with col2:
        if st.button("Remove Missing Values"):
            st.session_state.df = df.dropna()
            st.success("Rows containing missing values removed.")
            st.rerun()

    # -----------------------------
    # Current Dataset
    # -----------------------------
    st.subheader("📄 Current Dataset")

    st.dataframe(st.session_state.df)

    # -----------------------------
    # Download Button
    # -----------------------------
    csv_data = st.session_state.df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

# -----------------------------
# No File Uploaded
# -----------------------------
else:

    st.info("Please upload a CSV file to begin.")