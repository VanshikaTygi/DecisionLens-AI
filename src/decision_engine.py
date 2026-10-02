import pandas as pd


STAGE_SCORES = {
    "New Lead": 0.55,
    "Qualified": 0.75,
    "Proposal": 1.00,
    "Negotiation": 0.90,
    "Closed Won": 0.00,
    "Closed Lost": 0.00,
}


def normalize_series(series: pd.Series) -> pd.Series:
    """
    Convert a numeric series to a 0-1 scale.
    """

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(1.0, index=series.index)

    return (series - minimum) / (maximum - minimum)


def calculate_priority_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a transparent 0-100 priority score
    for each sales opportunity.
    """

    result = df.copy()

    # 1. Deal value signal
    deal_value_score = normalize_series(
        result["deal_value"]
    )

    # 2. Engagement signal
    website_score = normalize_series(
        result["website_visits"]
    )

    email_score = normalize_series(
        result["emails_opened"]
    )

    meeting_score = normalize_series(
        result["meetings_attended"]
    )

    engagement_score = (
        website_score * 0.40
        + email_score * 0.35
        + meeting_score * 0.25
    )

    # 3. Recency signal
    # More recent contact = higher score.
    recency_score = (
        1
        - (result["days_since_last_contact"] / 60)
    ).clip(0, 1)

    # 4. Sales-stage signal
    stage_score = (
        result["sales_stage"]
        .map(STAGE_SCORES)
        .fillna(0.50)
    )

    # Final weighted score
    result["priority_score"] = (
        deal_value_score * 35
        + engagement_score * 30
        + recency_score * 20
        + stage_score * 15
    )

    result["priority_score"] = (
        result["priority_score"]
        .round(2)
    )

    # Priority category
    result["priority"] = pd.cut(
        result["priority_score"],
        bins=[-1, 40, 70, 100],
        labels=["Low", "Medium", "High"],
    )

    # Sort highest priority first
    result = result.sort_values(
        "priority_score",
        ascending=False,
    ).reset_index(drop=True)

    return result