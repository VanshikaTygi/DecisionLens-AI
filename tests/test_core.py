import io

import pandas as pd
import pytest

from src.data_loader import load_sales_data
from src.decision_engine import calculate_priority_score


def make_sample_data():
    return pd.DataFrame(
        [
            {
                "lead_id": "L001",
                "company_name": "HighValue Corp",
                "industry": "Technology",
                "location": "Delhi",
                "deal_value": 1000000,
                "sales_stage": "Negotiation",
                "lead_source": "Website",
                "website_visits": 20,
                "emails_opened": 10,
                "meetings_attended": 3,
                "previous_interactions": 6,
                "days_since_last_contact": 5,
                "converted": 0,
            },
            {
                "lead_id": "L002",
                "company_name": "LowValue Corp",
                "industry": "Retail",
                "location": "Mumbai",
                "deal_value": 100000,
                "sales_stage": "New Lead",
                "lead_source": "Referral",
                "website_visits": 0,
                "emails_opened": 0,
                "meetings_attended": 0,
                "previous_interactions": 0,
                "days_since_last_contact": 60,
                "converted": 0,
            },
        ]
    )


def test_priority_scoring_creates_score_and_priority():
    df = make_sample_data()

    result = calculate_priority_score(df)

    assert "priority_score" in result.columns
    assert "priority" in result.columns
    assert len(result) == 2


def test_high_engagement_opportunity_gets_higher_priority():
    df = make_sample_data()

    result = calculate_priority_score(df)

    high_score = result.loc[
        result["company_name"] == "HighValue Corp",
        "priority_score",
    ].iloc[0]

    low_score = result.loc[
        result["company_name"] == "LowValue Corp",
        "priority_score",
    ].iloc[0]

    assert high_score > low_score


def test_missing_required_column_raises_error():
    df = make_sample_data().drop(columns=["deal_value"])

    csv_data = io.StringIO()
    df.to_csv(csv_data, index=False)
    csv_data.seek(0)

    with pytest.raises(ValueError, match="Missing required columns"):
        load_sales_data(csv_data)


def test_empty_dataset_raises_error():
    df = make_sample_data().iloc[0:0]

    csv_data = io.StringIO()
    df.to_csv(csv_data, index=False)
    csv_data.seek(0)

    with pytest.raises(ValueError, match="empty"):
        load_sales_data(csv_data)