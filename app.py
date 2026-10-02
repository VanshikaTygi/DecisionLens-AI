import streamlit as st

from src.data_loader import load_sales_data
from src.decision_engine import calculate_priority_score


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


# Run the decision engine
df = calculate_priority_score(df)

# Now display the dashboard
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

st.subheader("🎯 Opportunity Priority")

high_count = int((df["priority"] == "High").sum())
medium_count = int((df["priority"] == "Medium").sum())
low_count = int((df["priority"] == "Low").sum())

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔴 High Priority", high_count)

with col2:
    st.metric("🟡 Medium Priority", medium_count)

with col3:
    st.metric("🟢 Low Priority", low_count)


st.subheader("🔥 Top Opportunities")

top_opportunities = (
    df[
        [
            "company_name",
            "deal_value",
            "sales_stage",
            "priority_score",
            "priority",
        ]
    ]
    .sort_values("priority_score", ascending=False)
    .head(10)
)


st.dataframe(
    top_opportunities,
    use_container_width=True,
)

st.subheader("🔎 Evidence Behind Top Decision")

top_row = df.sort_values(
    "priority_score",
    ascending=False
).iloc[0]

st.markdown(
    f"### {top_row['company_name']}"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Priority",
        top_row["priority"]
    )

with col2:
    st.metric(
        "Priority Score",
        f"{top_row['priority_score']:.2f}"
    )

with col3:
    st.metric(
        "Deal Value",
        f"₹{top_row['deal_value']:,.0f}"
    )

st.markdown("#### Evidence")

evidence_col1, evidence_col2 = st.columns(2)

with evidence_col1:
    st.write(
        f"🌐 Website visits: **{top_row['website_visits']}**"
    )
    st.write(
        f"📧 Emails opened: **{top_row['emails_opened']}**"
    )
    st.write(
        f"🤝 Meetings attended: **{top_row['meetings_attended']}**"
    )

with evidence_col2:
    st.write(
        f"💬 Previous interactions: **{top_row['previous_interactions']}**"
    )
    st.write(
        f"📅 Days since last contact: **{top_row['days_since_last_contact']}**"
    )
    st.write(
        f"📊 Sales stage: **{top_row['sales_stage']}**"
    )

st.markdown("#### Recommended Action")

if top_row["priority"] == "High":
    recommendation = (
        "Follow up soon because this opportunity shows a strong "
        "combination of business value, engagement and sales-stage signals."
    )
elif top_row["priority"] == "Medium":
    recommendation = (
        "Review this opportunity and consider follow-up based on "
        "recent engagement and deal value."
    )
else:
    recommendation = (
        "Keep this opportunity under observation and prioritize "
        "higher-scoring opportunities first."
    )

st.info(recommendation)
