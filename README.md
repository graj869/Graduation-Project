# 🌱 Groww 12-Month SIP Retention Companion (AI Growth MVP)

> **Principal PM Graduation Project**: Increasing 12-Month Mutual Fund SIP Retention for First-Time Retail Investors on Groww through Behavioral Coaching and Friction-Free Self-Serve Interventions.

---

## 📌 1. Executive Summary & Problem Statement

First-time mutual fund investors in India (typically aged 22–28, salaried, Tier 1–3 cities) experience a dramatic drop-off in their SIP journey between **Month 3 and Month 6**. 

### The Industry Phenomenon:
1. **Early Return Disappointment (Months 3–6)**: First-time investors enter equity markets with expectations anchored in Fixed Deposits (guaranteed linear returns) or social media bull-run hype. When short-term market fluctuations show flat or negative (-2% to -5%) returns in Month 4, loss aversion triggers panic redemptions.
2. **Salary & Cashflow Mismatch**: 60%+ of SIP debit dates are inadvertently scheduled on the 1st to 5th of the month. When salaries are delayed (e.g. 7th to 10th), the auto-debit bounces, incurring hefty bank NACH bounce penalties (₹450–₹590 per failure). After 1–2 bounces, users cancel the mandate in frustration.
3. **Misconception of Lock-in & Penalties**: Many first-time investors mistakenly conflate mutual funds with Insurance (LIC) or Recurring Deposits (RDs), fearing CIBIL score damage, legal notices, or heavy AMC penalties if they miss an instalment.
4. **Execution-Only Platform Boundaries**: As an execution platform regulated by SEBI, Groww cannot legally offer personalized stock or fund recommendations. The AI must remain strictly educational and habit-reinforcing.

---

## 📐 2. Metric Decomposition & Retention Math

### Primary North Star Metric:
$$\text{12-Month Active SIP Retention Rate} = \frac{\text{Investors from Cohort } C \text{ with } \ge 1 \text{ successful SIP debit in Month 12}}{\text{Total Investors in Cohort } C \text{ who initiated their first SIP in Month 1}} \times 100$$

### Retention Cohort Drop-off Anatomy:
```
Month 1: [====================] 100%  (Onboarding & First Debit)
Month 2: [==================  ]  88%  (Familiarity Phase)
Month 3: [==============      ]  68%  <-- Drop-off accelerates (First market dip)
Month 4: [===========         ]  52%  <-- Critical Churn Zone (Flat/Red portfolio anxiety)
Month 6: [=========           ]  44%  <-- Salary mismatch & bank bounce fatigue
Month 12:[=======             ]  36%  <-- Baseline 12-Month Retention
```
* **Baseline 12-Month Retention**: ~36%
* **MVP Target 12-Month Retention**: **48% (+1200 bps improvement)**
* **Mechanism**: 
  - Alleviate early return anxiety via Rupee Cost Averaging visual coaching.
  - Eliminate bank bounce churn by migrating users to post-salary dates (e.g., 8th/10th).
  - Convert cancellations into temporary **Groww SIP Pause** (1–3 months) or **Skip Instalment**.

---

## 🏗️ 3. System Architecture & Safety Pipeline

```
+-----------------------------------------------------------------------------------+
|                              USER INTERFACE LAYER                                 |
|   Streamlit App (Groww Emerald Theme #00D09C) | Mobile-Responsive Container       |
|   - 💬 AI Retention Companion      - ⚙️ Cashflow Manager    - 📊 Evidence Hub    |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        INTENT CLASSIFIER & PROMPT ENGINE                          |
|   - Inputs: User Query / Scenario Pills (Month 4 Loss, Salary Delay, Advisory Trap)|
|   - Precedence: 1. Advisory Guard -> 2. Return Anxiety -> 3. Lock-in -> 4. Cashflow|
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        FOUNDATION MODEL INFERENCE LAYER                           |
|   Google Gemini (gemini-2.5-flash via google-genai SDK, temperature=0.2)          |
|   System Instruction: Zero-tolerance on fund recommendations, Zero-FOMO/Urgency   |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     TWO-TIER EVAL-GATED GUARDRAIL ENGINE                          |
|                                                                                   |
|  [Tier 1: Heuristic Regex Filter]                                                 |
|     - Detects banned tickers, buy/sell imperatives, urgency/FOMO language         |
|         |                                                                         |
|         +---> (If Flagged) ------------+                                          |
|         |                              |                                          |
|  [Tier 2: LLM Safety Evaluator]        |                                          |
|     - Verifies: 0 Fund Names,          |                                          |
|                 0 FOMO,                v                                          |
|                 SEBI Non-Advisory   +------------------------------------------+  |
|         |                           |      DETERMINISTIC SAFE FALLBACK         |  |
|         +---> (If Flagged) -------->|  - Politely decline recommendation       |  |
|         |                           |  - Surface Groww Pause/Skip self-serve   |  |
|         v (If Approved)             |  - Reassure on Rupee Cost Averaging      |  |
|  [Render Verified Response]         +------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## ⚖️ 4. Regulatory & Behavioral Constraints

1. **SEBI Non-Advisory Mandate**: Groww is an execution-only platform. The companion **never** recommends, rates, or compares specific mutual fund schemes (e.g., *Parag Parikh Flexi Cap*, *Quant Small Cap*, *HDFC Top 100*).
2. **Zero Fear/FOMO/Urgency**: Phrases like *"Last chance to buy"*, *"Market will crash"*, or *"Hurry before rally ends"* are completely prohibited. Tone is calm, long-term, and rational.
3. **Compounding Preservation**: When users face liquidity shortages, the system actively discourages SIP mandate cancellation and guides them to **SIP Pause** (1–3 months) or **Skip Instalment** with zero fees.

---

## 🚀 5. Local Setup & Execution Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Google Gemini API Key ([Get free API key](https://aistudio.google.com/))

### Step 1: Clone and Navigate
```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/Graduation-Project.git
cd Graduation_project
```

### Step 2: Set Up Virtual Environment & Dependencies
```bash
# Create and activate .venv
python3 -m venv .venv
source .venv/bin/activate

# Install verified pinned dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
```bash
cp .env.example .env
```
Open `.env` and set your key:
```ini
GEMINI_API_KEY=AIzaSyYourActualKeyHere
```
*(Note: If you do not have a `.env` file, you can enter the key securely in the app sidebar at runtime).*

### Step 4: Run Discovery Engine Evaluation
```bash
# Generate 50 synthetic feedback samples (JSON & CSV)
python discovery_engine/synthetic_feedback_data.py

# Run the 20-item Golden Set benchmark evaluation
python discovery_engine/classifier_eval.py
```

### Step 5: Launch the Streamlit MVP
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ 6. Streamlit Community Cloud Deployment

To host this MVP live for PM evaluation:
1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "feat: complete Groww SIP retention AI MVP"
   git push -u origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io/).
3. Select your repository: `<YOUR_GITHUB_USERNAME>/Graduation-Project`.
4. Main file path: `app.py`.
5. Under **Advanced Settings > Secrets**, add your Gemini API Key:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   ```
6. Click **Deploy**!

---

## 📁 7. Project Structure

```
Graduation_project/
├── .env.example                      # Template for Gemini API Key
├── .gitignore                        # Git exclusion rules
├── README.md                         # Architecture, metric math, setup guide
├── EVIDENCE_LOG.md                   # 20-item Golden Set validation & correction cases
├── requirements.txt                  # Pinned dependencies
├── app.py                            # Streamlit MVP with Groww UI & Cashflow Simulator
└── discovery_engine/
    ├── synthetic_feedback_data.py    # 50-item Indian investor feedback generator
    ├── synthetic_feedback.json       # Generated dataset in JSON
    ├── synthetic_feedback.csv        # Generated dataset in CSV
    └── classifier_eval.py            # Golden Set benchmark & correction pipeline
```
