import pandas as pd


REQUIRED_COLUMNS = [
    "lead_id",
    "company_name",
    "industry",
    "location",
    "deal_value",
    "sales_stage",
    "lead_source",
    "website_visits",
    "emails_opened",
    "meetings_attended",
    "previous_interactions",
    "days_since_last_contact",
    "converted",
]


def load_sales_data(file_path: str) -> pd.DataFrame:
    """Load the sales dataset from a CSV file."""

    df = pd.read_csv(file_path)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("The uploaded dataset is empty.")

    return df