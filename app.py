import streamlit as st

from src.data_loader import load_sales_data


st.set_page_config(
    page_title="DecisionLens AI",
    page_icon="🔎",
    layout="wide",
)


st.title("🔎 DecisionLens AI")

st.subheader("Evidence-first AI decision engine")

st.write(
    "Turn business data into actionable, traceable decisions "
    "with evidence-backed recommendations."
)


st.divider()

st.header("📊 Business Data")


st.write(
    "Upload a CRM or sales CSV to analyze your business opportunities."
)


uploaded_file = st.file_uploader(
    "Upload your sales dataset",
    type=["csv"],
)


if uploaded_file is not None:

    try:
        df = load_sales_data(uploaded_file)

        st.success(
            f"Dataset loaded successfully: {len(df):,} opportunities."
        )

    except Exception as error:
        st.error(f"Unable to load the dataset: {error}")

        st.stop()

else:

    st.info(
        "No file uploaded. Using the built-in sample sales dataset "
        "for demonstration."
    )

    try:
        df = load_sales_data(
            "data/sample_sales_leads.csv"
        )

    except Exception as error:
        st.error(
            f"Unable to load the sample dataset: {error}"
        )

        st.stop()


st.subheader("Dataset Overview")


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Opportunities",
        f"{len(df):,}",
    )


with col2:
    st.metric(
        "Total Deal Value",
        f"₹{df['deal_value'].sum():,.0f}",
    )


with col3:
    st.metric(
        "Average Deal Value",
        f"₹{df['deal_value'].mean():,.0f}",
    )


st.subheader("Sales Data")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)