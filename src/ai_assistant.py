import os

from dotenv import load_dotenv
from groq import Groq


# Load environment variables from .env
load_dotenv()


def get_groq_client():
    """
    Create and return a Groq client using the API key
    stored in the environment.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found. "
            "Please check your .env file."
        )

    return Groq(api_key=api_key)


def generate_decision_recommendation(
    question,
    company_name,
    deal_value,
    sales_stage,
    priority,
    priority_score,
    website_visits,
    emails_opened,
    meetings_attended,
    previous_interactions,
    days_since_last_contact,
):
    """
    Generate a grounded business recommendation using Groq.

    The AI receives calculated business facts rather than
    the complete dataset, helping keep recommendations
    focused and evidence-based.
    """

    client = get_groq_client()

    prompt = f"""
You are the AI decision assistant inside DecisionLens AI,
an evidence-first business decision engine.

Your job is to help a sales manager make a decision using
ONLY the business evidence provided below.

IMPORTANT RULES:
1. Do not invent or change any numbers.
2. Do not introduce information that is not provided.
3. Base the recommendation on the evidence.
4. Clearly distinguish facts from your recommendation.
5. Keep the answer concise and practical.
6. If the evidence is insufficient, say so.
7. Do not claim certainty about whether a deal will convert.

BUSINESS QUESTION:
{question}

OPPORTUNITY:
Company: {company_name}
Deal Value: ₹{deal_value:,.0f}
Sales Stage: {sales_stage}
Priority: {priority}
Priority Score: {priority_score:.2f}

EVIDENCE:
Website Visits: {website_visits}
Emails Opened: {emails_opened}
Meetings Attended: {meetings_attended}
Previous Interactions: {previous_interactions}
Days Since Last Contact: {days_since_last_contact}

Return the response in this format:

Decision:
<one clear recommendation>

Why:
<2-3 sentences explaining the recommendation using the evidence>

Evidence:
- <specific evidence point>
- <specific evidence point>
- <specific evidence point>

Next Step:
<one practical action for the sales team>
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful, evidence-first business "
                    "decision assistant."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_tokens=300,
    )

    return response.choices[0].message.content