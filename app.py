import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="AI Data Analyst Pro",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Data Analyst Pro")
st.markdown("Upload a CSV file to explore, analyze, visualize, and clean your dataset.")

# =====================================================
# File Upload
# =====================================================

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

# =====================================================
# Main Application
# =====================================================

if uploaded_file is not None:

    # Load uploaded file only once
    if (
        "uploaded_file_name" not in st.session_state
        or st.session_state.uploaded_file_name != uploaded_file.name
    ):
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.df = pd.read_csv(uploaded_file)

    # Working dataframe
    df = st.session_state.df

    st.success("✅ CSV uploaded successfully!")

    # =====================================================
    # Dataset Shape
    # =====================================================

    st.subheader("📐 Dataset Shape")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    # =====================================================
    # Column Names
    # =====================================================

    st.subheader("📝 Column Names")
    st.write(list(df.columns))

    # =====================================================
    # Data Types
    # =====================================================

    st.subheader("🔎 Data Types")

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values
    })

    st.dataframe(dtype_df, use_container_width=True)

    # =====================================================
    # Missing Values
    # =====================================================

    st.subheader("❗ Missing Values")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(missing_df, use_container_width=True)

    # =====================================================
    # Summary Statistics
    # =====================================================

    st.subheader("📊 Summary Statistics")

    st.dataframe(
        df.describe(include="all"),
        use_container_width=True
    )

    # =====================================================
    # First Five Rows
    # =====================================================

    st.subheader("👀 First 5 Rows")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    # =====================================================
    # Data Quality Dashboard
    # =====================================================

    st.markdown("---")
    st.header("🧹 Data Quality Dashboard")

    duplicate_rows = df.duplicated().sum()

    st.metric("Duplicate Rows", duplicate_rows)

    # Missing Percentage

    st.subheader("Missing Percentage by Column")

    missing_percentage = (
        df.isnull().sum() / len(df) * 100
    ).round(2)

    missing_percentage_df = pd.DataFrame({
        "Column": missing_percentage.index,
        "Missing %": missing_percentage.values
    })

    st.dataframe(
        missing_percentage_df,
        use_container_width=True
    )

    # Unique Values

    st.subheader("Unique Values")

    unique_df = pd.DataFrame({
        "Column": df.columns,
        "Unique Values": df.nunique().values
    })

    st.dataframe(
        unique_df,
        use_container_width=True
    )

    # Memory Usage

    memory_kb = df.memory_usage(deep=True).sum() / 1024

    st.metric(
        "Memory Usage (KB)",
        f"{memory_kb:.2f}"
    )

    # =====================================================
    # Cleaning Buttons
    # =====================================================

    st.subheader("🧹 Cleaning Tools")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🗑 Remove Duplicates"):

            st.session_state.df = df.drop_duplicates()

            st.success("Duplicate rows removed.")

            st.rerun()

    with col2:

        if st.button("❌ Remove Missing Values"):

            st.session_state.df = df.dropna()

            st.success("Rows with missing values removed.")

            st.rerun()

    # Refresh dataframe after cleaning

    df = st.session_state.df

    # =====================================================
    # Current Dataset
    # =====================================================

    st.subheader("📄 Current Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )

    # =====================================================
    # Download Button
    # =====================================================

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

    # =====================================================
    # Interactive Data Visualization
    # =====================================================

    st.markdown("---")
    st.header("📈 Interactive Data Visualization")

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_columns) > 0:

        # Histogram

        selected_column = st.selectbox(
            "Select Numeric Column",
            numeric_columns
        )

        st.subheader(f"Histogram of {selected_column}")

        histogram = px.histogram(
            df,
            x=selected_column,
            nbins=20,
            title=f"Distribution of {selected_column}"
        )

        st.plotly_chart(
            histogram,
            use_container_width=True
        )

        # Box Plot

        st.subheader(f"Box Plot of {selected_column}")

        box_plot = px.box(
            df,
            y=selected_column,
            title=f"Box Plot of {selected_column}",
            points="outliers"
        )

        st.plotly_chart(
            box_plot,
            use_container_width=True
        )

        # Scatter Plot

        if len(numeric_columns) >= 2:

            st.subheader("Scatter Plot")

            x_axis = st.selectbox(
                "Select X-axis",
                numeric_columns,
                key="scatter_x"
            )

            y_axis = st.selectbox(
                "Select Y-axis",
                numeric_columns,
                index=1,
                key="scatter_y"
            )

            scatter_plot = px.scatter(
                df,
                x=x_axis,
                y=y_axis,
                title=f"{y_axis} vs {x_axis}"
            )

            st.plotly_chart(
                scatter_plot,
                use_container_width=True
            )

        else:

            st.info(
                "Scatter plot requires at least two numeric columns."
            )

    else:

        st.warning(
            "No numeric columns found in this dataset."
        )

else:

    st.info("📁 Please upload a CSV file to begin.")