import streamlit as st
import pandas as pd
from login import login


from backend.database import (
    create_database,
    save_history,
    get_history
)


from backend.data_loader import load_data
from backend.analytics import (
    total_rows,
    total_columns,
    missing_values,
    average_age,
    average_salary
)

from backend.filters import filter_city

from backend.charts import (
    age_chart,
    salary_chart,
    salary_line_chart,
    city_chart
)

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- Login Session ----------------
if "login" not in st.session_state:
    st.session_state["login"] = False

# ---------------- Login Page ----------------
if not st.session_state["login"]:
    login()
    st.stop()

create_database()

# ---------------- Sidebar ----------------
st.sidebar.title("📊 AI Dashboard")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📂 Upload Dataset",
        "📊 Dashboard",
        "📜 Upload History",
        "🚪 Logout"
    ]
)

# ---------------- Logout ----------------
if menu == "🚪 Logout":

    st.session_state["login"] = False
    st.rerun()

# ---------------- Home ----------------
elif menu == "🏠 Home":

    st.markdown("""
    <h1 style='text-align:center;
    color:#1565C0;
    font-size:45px;
    font-weight:bold;'>

    📊 AI Data Analysis Dashboard

    </h1>
    """, unsafe_allow_html=True)

    st.success("Welcome to AI Data Analysis Dashboard")

    st.write("""
    ### Project Features

    ✅ User Login

    ✅ Upload CSV Dataset

    ✅ Dashboard Analytics

    ✅ Interactive Charts

    ✅ AI Insights

    ✅ Search & Filter

    ✅ Download CSV
    """)

# ---------------- Upload Dataset ----------------
elif menu == "📂 Upload Dataset":

    st.title("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = load_data(uploaded_file)

        st.session_state["df"] = df

        save_history(
            uploaded_file.name,
            df.shape[0],
            df.shape[1]
        )

        st.success("✅ Dataset Uploaded Successfully")

        st.dataframe(df.head(), use_container_width=True)

        # ---------------- Dashboard ----------------
elif menu == "📊 Dashboard":

    st.title("📊 Dashboard")

    if "df" not in st.session_state:
        st.warning("⚠ Please upload a dataset first.")
        st.stop()

    # Load Dataset
    df = st.session_state["df"]

    # ---------------- KPI ----------------
    c1, c2, c3 = st.columns(3)

    c1.metric("📄 Total Rows", total_rows(df))
    c2.metric("📊 Total Columns", total_columns(df))
    c3.metric("❌ Missing Values", missing_values(df))

    st.divider()

    # ---------------- Dataset Summary ----------------
    st.subheader("📊 Dataset Summary")

    st.write("**Average Age :**", average_age(df))
    st.write("**Average Salary :**", average_salary(df))

    st.divider()

    # ---------------- Filter ----------------
    filtered_df = df.copy()

    if "City" in df.columns:

        city = st.selectbox(
            "🏙 Select City",
            ["All"] + list(df["City"].unique())
        )

        filtered_df = filter_city(df, city)

    st.divider()

    # ---------------- Search ----------------
    if "Name" in filtered_df.columns:

        search = st.text_input("🔎 Search Name")

        if search:

            filtered_df = filtered_df[
                filtered_df["Name"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

    st.divider()



        # ---------------- Charts ----------------
    st.subheader("📊 Charts")

    col1, col2 = st.columns(2)

    # Age Bar Chart
    with col1:
        if "Age" in filtered_df.columns:
            st.plotly_chart(
                age_chart(filtered_df),
                use_container_width=True
            )

    # Salary Pie Chart
    with col2:
        if "Salary" in filtered_df.columns:
            st.plotly_chart(
                salary_chart(filtered_df),
                use_container_width=True
            )

    st.divider()

    # ---------------- Salary Trend ----------------
    if "Salary" in filtered_df.columns:

        st.subheader("📈 Salary Trend")

        st.plotly_chart(
            salary_line_chart(filtered_df),
            use_container_width=True
        )

    st.divider()

    # ---------------- City Distribution ----------------
    if "City" in filtered_df.columns:

        st.subheader("🏙 Employees by City")

        st.plotly_chart(
            city_chart(filtered_df),
            use_container_width=True
        )

    st.divider()

    # ---------------- Dataset ----------------
    st.subheader("📋 Complete Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.divider()

    # ---------------- Download ----------------
    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered CSV",
        data=csv,
        file_name="filtered_dataset.csv",
        mime="text/csv"
    )


    st.divider()

    # ---------------- AI Insights ----------------
    st.subheader("🤖 AI Insights")

    total_emp = len(filtered_df)

    st.success(f"✅ Total Employees : {total_emp}")

    if "Age" in filtered_df.columns:
        st.info(f"👤 Average Age : {filtered_df['Age'].mean():.2f}")
        st.info(f"🔼 Maximum Age : {filtered_df['Age'].max()}")
        st.info(f"🔽 Minimum Age : {filtered_df['Age'].min()}")

    if "Salary" in filtered_df.columns:
        st.success(f"💰 Average Salary : ₹ {filtered_df['Salary'].mean():,.2f}")
        st.success(f"💰 Highest Salary : ₹ {filtered_df['Salary'].max():,.0f}")
        st.success(f"💰 Lowest Salary : ₹ {filtered_df['Salary'].min():,.0f}")

    if "City" in filtered_df.columns:
        top_city = filtered_df["City"].mode()[0]
        st.info(f"🏙 Most Employees are from : {top_city}")

    st.markdown("---")

    st.subheader("🧠 AI Recommendation")

    recommendation = ""

    if "Salary" in filtered_df.columns:

        avg_salary = filtered_df["Salary"].mean()

        if avg_salary > 50000:
            recommendation += "✔ Employees have a good average salary.\n\n"
        else:
            recommendation += "✔ Salary levels are comparatively lower.\n\n"

    if filtered_df.isnull().sum().sum() == 0:
        recommendation += "✔ Dataset contains no missing values.\n\n"
    else:
        recommendation += "✔ Clean the missing values before further analysis.\n\n"

    if "City" in filtered_df.columns:
        recommendation += f"✔ Most employees belong to {top_city}."

    st.success(recommendation)


    # ---------------- Upload History ----------------
elif menu == "📜 Upload History":

    st.title("📜 Upload History")

    history = get_history()

    if history:

        history_df = pd.DataFrame(
            history,
            columns=[
                "ID",
                "Filename",
                "Rows",
                "Columns"
            ]
        )

        st.dataframe(
            history_df,
            use_container_width=True
        )

    else:
        st.info("No upload history found.")