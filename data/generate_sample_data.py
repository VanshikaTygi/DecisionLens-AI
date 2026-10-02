import numpy as np
import pandas as pd


# Fixed seed makes our synthetic dataset reproducible.
np.random.seed(42)

NUM_RECORDS = 500

industries = [
    "Technology",
    "Healthcare",
    "Finance",
    "Retail",
    "Education",
    "Manufacturing",
    "Logistics",
    "Real Estate",
]

locations = [
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Hyderabad",
    "Pune",
    "Chennai",
    "Gurugram",
    "Noida",
]

sales_stages = [
    "New Lead",
    "Qualified",
    "Demo",
    "Proposal",
    "Negotiation",
]

lead_sources = [
    "Website",
    "Referral",
    "LinkedIn",
    "Email Campaign",
    "Partner",
    "Advertisement",
]

# Generate company names.
company_names = [
    f"{name} {suffix}"
    for name, suffix in zip(
        np.random.choice(
            [
                "Apex",
                "Nova",
                "Vertex",
                "Summit",
                "BluePeak",
                "NextGen",
                "Orbit",
                "Prime",
                "Elevate",
                "Nexus",
            ],
            NUM_RECORDS,
        ),
        np.random.choice(
            [
                "Technologies",
                "Solutions",
                "Industries",
                "Systems",
                "Labs",
                "Enterprises",
            ],
            NUM_RECORDS,
        ),
    )
]

# Sales stages have different typical deal values.
stage_base_values = {
    "New Lead": 80000,
    "Qualified": 150000,
    "Demo": 220000,
    "Proposal": 350000,
    "Negotiation": 500000,
}

sales_stage = np.random.choice(
    sales_stages,
    NUM_RECORDS,
    p=[0.25, 0.25, 0.20, 0.18, 0.12],
)

deal_value = []

for stage in sales_stage:
    base = stage_base_values[stage]

    value = np.random.normal(
        loc=base,
        scale=base * 0.25,
    )

    deal_value.append(max(25000, round(value, -3)))

deal_value = np.array(deal_value)

# Engagement signals.
website_visits = np.random.poisson(lam=12, size=NUM_RECORDS)
website_visits = np.clip(website_visits, 0, 60)

emails_opened = np.random.poisson(lam=7, size=NUM_RECORDS)
emails_opened = np.clip(emails_opened, 0, 30)

meetings_attended = np.random.poisson(lam=2, size=NUM_RECORDS)
meetings_attended = np.clip(meetings_attended, 0, 10)

previous_interactions = np.random.poisson(lam=5, size=NUM_RECORDS)
previous_interactions = np.clip(previous_interactions, 0, 25)

# Smaller number = more recently contacted.
days_since_last_contact = np.random.randint(
    1,
    61,
    size=NUM_RECORDS,
)

# Build a synthetic conversion probability.
stage_score = {
    "New Lead": 0.05,
    "Qualified": 0.15,
    "Demo": 0.25,
    "Proposal": 0.40,
    "Negotiation": 0.55,
}

conversion_probability = np.array(
    [
        stage_score[stage]
        + min(visits / 200, 0.15)
        + min(meetings / 30, 0.10)
        + min(opens / 60, 0.08)
        - min(days / 500, 0.10)
        for stage, visits, meetings, opens, days in zip(
            sales_stage,
            website_visits,
            meetings_attended,
            emails_opened,
            days_since_last_contact,
        )
    ]
)

conversion_probability = np.clip(
    conversion_probability,
    0.02,
    0.90,
)

converted = np.random.binomial(
    1,
    conversion_probability,
)

data = pd.DataFrame(
    {
        "lead_id": [
            f"DL-{i:04d}"
            for i in range(1, NUM_RECORDS + 1)
        ],
        "company_name": company_names,
        "industry": np.random.choice(
            industries,
            NUM_RECORDS,
        ),
        "location": np.random.choice(
            locations,
            NUM_RECORDS,
        ),
        "deal_value": deal_value.astype(int),
        "sales_stage": sales_stage,
        "lead_source": np.random.choice(
            lead_sources,
            NUM_RECORDS,
        ),
        "website_visits": website_visits,
        "emails_opened": emails_opened,
        "meetings_attended": meetings_attended,
        "previous_interactions": previous_interactions,
        "days_since_last_contact": days_since_last_contact,
        "converted": converted,
    }
)

output_path = "data/sample_sales_leads.csv"

data.to_csv(
    output_path,
    index=False,
)

print(f"Created {len(data)} synthetic sales records.")
print(f"Saved to: {output_path}")
print("\nColumns:")
print(", ".join(data.columns))

print("\nFirst 5 records:")
print(data.head())