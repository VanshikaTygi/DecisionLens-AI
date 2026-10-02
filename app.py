import streamlit as st
import pandas as pd
import plotly.express as px

from src.ai_assistant import generate_decision_recommendation
from src.data_loader import load_sales_data
from src.decision_engine import calculate_priority_score


st.set_page_config(
    page_title="DecisionLens AI",
    page_icon="🔎",
    layout="wide",
)

st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Section headings */
    h1, h2, h3 {
        color: #172033;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e5e9f2;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.55rem 1rem;
    }

    /* Input box */
    div[data-baseweb="input"] {
        border-radius: 8px;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    /* Horizontal separators */
    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #172033, #263b66);
        padding: 28px 32px;
        border-radius: 16px;
        margin-bottom: 25px;
    ">
        <h1 style="color:white; margin-bottom:6px;">
            🔎 DecisionLens AI
        </h1>
        <p style="color:#dbe5f5; font-size:17px; margin:0;">
            Evidence-first AI decision engine for business data
        </p>
        <p style="color:#aebdd6; font-size:14px; margin-top:10px;">
            Turn business data → evidence → decisions → actions
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

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

with st.container(border=True):
    st.subheader("📊 Opportunity Priority Overview")

    priority_counts = (
        df["priority"]
        .value_counts()
        .reindex(["High", "Medium", "Low"])
        .fillna(0)
    )

    fig = px.bar(
        x=priority_counts.index,
        y=priority_counts.values,
        labels={
            "x": "Priority",
            "y": "Number of Opportunities",
        },
        title="Opportunity Distribution by Priority",
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    st.plotly_chart(fig, use_container_width=True)

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


st.subheader("📌 Evidence Signals")

e1, e2, e3 = st.columns(3)

with e1:
    st.metric(
        "🌐 Website Visits",
        int(top_row["website_visits"])
    )

with e2:
    st.metric(
        "✉️ Emails Opened",
        int(top_row["emails_opened"])
    )

with e3:
    st.metric(
        "🤝 Meetings",
        int(top_row["meetings_attended"])
    )

e4, e5, e6 = st.columns(3)

with e4:
    st.metric(
        "💬 Interactions",
        int(top_row["previous_interactions"])
    )

with e5:
    st.metric(
        "📅 Days Since Contact",
        int(top_row["days_since_last_contact"])
    )

with e6:
    st.metric(
        "🏢 Sales Stage",
        top_row["sales_stage"]
    )


st.subheader("💡 Recommended Action")

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

st.divider()

with st.container(border=True):

    st.subheader("🤖 DecisionLens AI Assistant")

    st.caption(
        "Ask a business question and receive an evidence-grounded "
        "recommendation based on the selected opportunity."
    )

    question = st.text_input(
        "Business question",
        value="Should we prioritize this opportunity for follow-up?",
        label_visibility="visible",
    )

    generate_ai = st.button(
        "✨ Generate AI Decision",
        type="primary",
        use_container_width=False,
    )

    if generate_ai:

        with st.spinner("Analyzing business evidence..."):

            try:
                ai_response = generate_decision_recommendation(
                    question=question,
                    company_name=top_row["company_name"],
                    deal_value=top_row["deal_value"],
                    sales_stage=top_row["sales_stage"],
                    priority=top_row["priority"],
                    priority_score=top_row["priority_score"],
                    website_visits=top_row["website_visits"],
                    emails_opened=top_row["emails_opened"],
                    meetings_attended=top_row["meetings_attended"],
                    previous_interactions=top_row["previous_interactions"],
                    days_since_last_contact=top_row["days_since_last_contact"],
                )

                st.success("AI decision generated successfully.")

                st.markdown("### 🧠 AI Decision")
                st.markdown(ai_response)

            except Exception as e:
                st.error(
                    "The AI assistant is temporarily unavailable. "
                    "The analytical dashboard is still available."
                )
                st.caption(f"Technical detail: {str(e)}")