# 🔎 DecisionLens AI

## Evidence-First AI Decision Engine for Business Data

DecisionLens AI is an evidence-first AI decision engine that transforms business and sales data into traceable insights, prioritized opportunities, and actionable recommendations.

The system follows:

**Business Data → Evidence → Decision → Action**

---

## 🎯 Problem

Business teams often have large amounts of CRM and sales data but struggle to identify which opportunities require attention and why.

Traditional dashboards can display metrics, but they do not always connect those metrics directly to a recommended business action.

DecisionLens AI addresses this by combining programmatic business analytics with an AI decision assistant.

---

## 💡 Solution

DecisionLens AI:

- Analyses CRM and sales data from CSV files
- Validates uploaded business data
- Calculates transparent opportunity priority scores
- Identifies high-priority opportunities
- Shows the evidence behind each recommendation
- Generates AI-assisted business decisions
- Provides a practical next step for the sales team

The AI assistant receives calculated business evidence rather than the entire raw dataset, helping keep recommendations grounded in measurable data.

---

## ⭐ Key Features

### 1. Business Data Analysis

Upload a CRM or sales CSV and analyse business opportunities using structured business and engagement data.

### 2. Opportunity Prioritization

Each opportunity receives a transparent priority score based on business and engagement signals.

Opportunities are categorized into:

- High
- Medium
- Low

### 3. Evidence-First Decision Cards

Recommendations are supported by measurable evidence such as:

- Deal value
- Website visits
- Emails opened
- Meetings attended
- Previous interactions
- Days since last contact
- Sales stage

### 4. AI Decision Assistant

Users can ask a business question about an opportunity and receive an AI-generated response containing:

- Decision
- Reasoning
- Evidence
- Next Step

### 5. Visual Business Dashboard

The application provides:

- Dataset overview
- Priority distribution
- Opportunity tables
- Top opportunities
- Evidence metrics
- Recommended actions
- AI-generated decisions

---

## 🏗️ Architecture

```text
                CSV / CRM Data
                       │
                       ▼
              Data Validation
                       │
                       ▼
              Pandas Analytics
                       │
                       ▼
            Priority Score Engine
                       │
                       ▼
              Evidence Extraction
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
      Deterministic Action   AI Assistant
                                │
                                ▼
                         Decision + Why
                         + Evidence
                         + Next Step
```

---

## 🧮 Priority Scoring

DecisionLens AI calculates a transparent priority score using business signals including:

- Deal value
- Customer engagement
- Sales stage
- Recency of interaction

The calculated score is then used to categorize opportunities into High, Medium, or Low priority.

The scoring layer is deterministic and programmatic, while the AI layer is used to explain the available evidence and provide a practical recommendation.

---

## 📊 Sample Dataset

The project includes a synthetic CRM/sales dataset for demonstration and reproducibility.

### Dataset characteristics

- 500 business opportunities
- Company and industry information
- Deal value
- Sales stage
- Lead source
- Website visits
- Emails opened
- Meetings attended
- Previous interactions
- Days since last contact
- Conversion field

The included dataset is synthetic and is intended for demonstration purposes.

---

## 🤖 AI Technology

The AI decision assistant uses the Groq API with:

**Model:** `openai/gpt-oss-20b`

The AI layer is designed to:

- Use only the supplied business evidence
- Avoid inventing or changing business numbers
- Clearly distinguish facts from recommendations
- Provide practical next actions
- State when the available evidence is insufficient
- Avoid claiming certainty about business outcomes

The analytical scoring and evidence extraction are performed programmatically before the AI explanation is generated.

This creates the following flow:

```text
Business Data
      ↓
Programmatic Analysis
      ↓
Calculated Evidence
      ↓
Priority + Metrics
      ↓
AI Decision Assistant
      ↓
Decision + Why + Evidence + Next Step
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and analytics |
| Streamlit | Web application and dashboard |
| Pandas | Data loading and business-data analysis |
| NumPy | Numerical operations |
| Plotly | Interactive data visualization |
| Groq API | AI decision assistant |
| GPT-OSS-20B | AI model used through Groq |
| python-dotenv | Local environment variable management |
| GitHub | Version control and source repository |

---

## 📁 Project Structure

```text
DecisionLens-AI/
│
├── data/
│   ├── generate_sample_data.py
│   └── sample_sales_leads.csv
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── decision_engine.py
│   └── ai_assistant.py
│
├── tests/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

> **Security note:** `.env` contains the local Groq API key and must never be committed to GitHub. It is excluded through `.gitignore`.

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/VanshikaTygi/DecisionLens-AI.git
cd DecisionLens-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Groq API key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
```

Do not commit the `.env` file or expose the API key publicly.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## ☁️ Deployment

The application is designed to be deployed using Streamlit Community Cloud.

After deployment, configure the Groq API key through the platform's secrets management.

Use:

```text
GROQ_API_KEY = "your_groq_api_key"
```

The API key should not be hard-coded into the application or committed to GitHub.

### Live Demo

**Deployment URL:** To be added after deployment.

---

## 🧪 Reliability and Error Handling

DecisionLens AI includes handling for common data and AI failures, including:

- Invalid CSV structure
- Missing required columns
- Empty datasets
- Invalid uploaded data
- AI/API availability issues

If the AI assistant is temporarily unavailable, the analytical dashboard remains usable and the deterministic business analysis can still be viewed.

---

## 📌 Example Decision Flow

For a high-priority opportunity, DecisionLens AI can combine:

- High deal value
- Strong website engagement
- Email engagement
- Meeting activity
- Previous interactions
- Recent sales activity
- Current sales stage

The system then produces an evidence-backed recommendation and a practical next action.

Example:

```text
Decision:
Prioritize the opportunity for follow-up.

Why:
The opportunity has a high priority score, meaningful deal value,
and strong engagement signals.

Evidence:
- Website visits
- Emails opened
- Meetings attended
- Previous interactions
- Days since last contact

Next Step:
Schedule a follow-up with the opportunity.
```

---

## ⚠️ Limitations

- The included dataset is synthetic and intended for demonstration.
- The priority score is a transparent heuristic and is not a trained predictive model.
- AI recommendations are based only on the evidence supplied to the AI assistant.
- AI recommendations should support human decision-making rather than replace business judgment.
- The quality of recommendations depends on the quality and completeness of the business data.

---

## 🤝 AI Tools and External Resources Disclosure

The project uses the following AI and external resources:

### Groq API

Used to provide the AI decision-assistant functionality.

### GPT-OSS-20B

Used through the Groq API to generate evidence-grounded business decision explanations.

### ChatGPT

Used during development for coding assistance, debugging guidance, documentation support, project structuring, and development assistance.

### Dataset

The included business dataset is synthetic and generated specifically for demonstration and reproducibility.

External APIs, AI models, and AI development tools used in the project are disclosed as required by the challenge.

---

## 👤 Developer

**Vanshika Tyagi**

B.Tech CSE — AI & ML

GitHub:  
https://github.com/VanshikaTygi

---

## 🏆 Challenge Track

**Build Fast with AI — AI Decision Engine for Business Data**

**Problem Statement:** PS-04

**Project:** DecisionLens AI

---

## 📜 Project Motto

> **Turn business data → evidence → decisions → actions**