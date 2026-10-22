"""
Discovery Engine: Synthetic Feedback Generator
==============================================
Generates 50 realistic first-time Indian retail mutual fund investor feedback items
harvested across r/IndiaInvestments, Google Play Store reviews, and personal finance forums.

Root Causes Captured:
1. CASHFLOW_MISMATCH: Salary credited post-SIP debit, month-end crunch, NACH bounce fee shock.
2. EARLY_RETURN_ANXIETY: Months 3-6 portfolio flat/red vs Fixed Deposit / Savings expectations.
3. LOCKIN_FLEXIBILITY_MISCONCEPTION: Assumption that SIP is like an RD/Insurance with penalties,
   fear of CIBIL impact, ignorance of Groww Pause/Skip/Date change features.
4. ADVISORY_SEEKING: Demanding specific fund/stock picks, switching to "top performing" funds.
5. UNRECOGNIZED_OTHER: General app/UI inquiries, KYC/bank mandate setup issues.
"""

import json
import os
import pandas as pd

FEEDBACK_DATASET = [
    # --- CASHFLOW_MISMATCH (1-15) ---
    {
        "id": "FB_001",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "23yo Software Trainee (Bangalore)",
        "tenure_months": 3,
        "raw_text": "My SIP debit date is 1st of every month, but my company credits salary only on the 7th. My bank charged me Rs 590 for NACH bounce! How do I change this without stopping the investment?",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.88
    },
    {
        "id": "FB_002",
        "source": "Play Store Review",
        "persona": "25yo BPO Associate (Pune)",
        "tenure_months": 4,
        "raw_text": "Diwali bonus was spent and now I have zero balance in HDFC account. Will Groww report me to CIBIL if my SIP bounces this month? Thinking of cancelling completely.",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.92
    },
    {
        "id": "FB_003",
        "source": "Financial Forum",
        "persona": "27yo Marketing Exec (Delhi NCR)",
        "tenure_months": 2,
        "raw_text": "Rent is due on 30th and SIP debits on 2nd. Every month I'm left scraping by. Can I move the auto-debit to mid-month or is the date fixed forever?",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.79
    },
    {
        "id": "FB_004",
        "source": "Play Store Review",
        "persona": "24yo Tier-2 Retail Store Manager (Jaipur)",
        "tenure_months": 5,
        "raw_text": "Bank deducted Rs 450 bounce charges because salary got delayed by 3 days. Mutual funds are eating away my savings in bank penalties. Stopping my SIP today.",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.95
    },
    {
        "id": "FB_005",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "29yo Freelance Designer (Goa)",
        "tenure_months": 4,
        "raw_text": "Client payment delayed by 2 weeks. I have 2 SIPs of 2500 running. Can I skip just this month's installment without terminating the whole mandate?",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.74
    },
    {
        "id": "FB_006",
        "source": "Play Store Review",
        "persona": "22yo Graduate Intern (Hyderabad)",
        "tenure_months": 1,
        "raw_text": "First SIP cut from account before my first salary came in. Account went into negative balance. Very bad experience, I want my money refunded.",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.91
    },
    {
        "id": "FB_007",
        "source": "Twitter/X Support",
        "persona": "26yo Operations Analyst (Mumbai)",
        "tenure_months": 5,
        "raw_text": "Unexpected medical bill this month. Need to hold my 5000 SIP for next 2 months until I rebuild my emergency buffer. Is temporary pause possible on Groww?",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.65
    },
    {
        "id": "FB_008",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "24yo Sales Officer (Chandigarh)",
        "tenure_months": 3,
        "raw_text": "Why is SIP date locked? In my company incentives come on 15th, but I set SIP for 5th by mistake. Every month I worry about insufficient funds.",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.81
    },
    {
        "id": "FB_009",
        "source": "Financial Forum",
        "persona": "31yo Small Business Owner (Indore)",
        "tenure_months": 6,
        "raw_text": "Quarterly GST payment due next week, cashflow is tight. Can I skip only the upcoming instalment without having to re-do the whole e-mandate again?",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.70
    },
    {
        "id": "FB_010",
        "source": "Play Store Review",
        "persona": "25yo Junior Accountant (Kolkata)",
        "tenure_months": 3,
        "raw_text": "SBI penalised me 295 rupees for unsuccessful auto debit. Better to close SIP and do manual lumpsum whenever I have extra cash.",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.89
    },
    {
        "id": "FB_011",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "28yo IT Consultant (Noida)",
        "tenure_months": 4,
        "raw_text": "Switching jobs this month, so there is a 20-day salary hiatus between companies. Can I pause my 3 active SIPs for 60 days without closing them?",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.60
    },
    {
        "id": "FB_012",
        "source": "Twitter/X Support",
        "persona": "23yo Teacher (Coimbatore)",
        "tenure_months": 2,
        "raw_text": "My salary was credited on 10th instead of 1st due to festival holidays. Mandate failed. Does Groww retry automatically or will my investment lapse?",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.68
    },
    {
        "id": "FB_013",
        "source": "Play Store Review",
        "persona": "24yo Tech Support (Chennai)",
        "tenure_months": 5,
        "raw_text": "Every month end I have zero balance. Auto debit on 28th is worst decision I made. Need to push debit date to 5th after payday.",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.84
    },
    {
        "id": "FB_014",
        "source": "Financial Forum",
        "persona": "27yo Pharma Sales Rep (Ahmedabad)",
        "tenure_months": 3,
        "raw_text": "Traveling for work and salary reimbursement is delayed. If account has insufficient funds on SIP day, how much penalty does Groww charge?",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.73
    },
    {
        "id": "FB_015",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "25yo Graphic Designer (Bangalore)",
        "tenure_months": 6,
        "raw_text": "I got an annual insurance premium due this month. Can't afford the 4000 SIP right now. How many months can I pause before the bank cancels the autopay?",
        "ground_truth_category": "CASHFLOW_MISMATCH",
        "churn_risk_score": 0.77
    },

    # --- EARLY_RETURN_ANXIETY (16-30) ---
    {
        "id": "FB_016",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "24yo First-Time Investor (Lucknow)",
        "tenure_months": 4,
        "raw_text": "Invested Rs 3000 every month for 4 months in Nifty 50 Index. Total invested is 12,000 but current value is 11,650! Even SBI savings bank gives 3% interest. Why am I losing capital?",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.94
    },
    {
        "id": "FB_017",
        "source": "Play Store Review",
        "persona": "26yo Bank Clerk (Nagpur)",
        "tenure_months": 5,
        "raw_text": "Mutual funds are subject to market risks, but nobody told me it will stay red for 5 months continuously. Better to put money in Post Office FD with guaranteed 7.1%.",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.91
    },
    {
        "id": "FB_018",
        "source": "Financial Forum",
        "persona": "28yo Govt Employee (Bhopal)",
        "tenure_months": 3,
        "raw_text": "My friend said mutual funds give 15% CAGR. 3 months completed and my XIRR is -4.2%. Is my fund bad or did I start at the wrong market peak?",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.86
    },
    {
        "id": "FB_019",
        "source": "Play Store Review",
        "persona": "23yo Junior Developer (Kochi)",
        "tenure_months": 6,
        "raw_text": "Six months of disciplined SIP, but my portfolio returns are literally zero (0.12%). What is the point of taking equity risk if returns are worse than saving account?",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.89
    },
    {
        "id": "FB_020",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "25yo Content Creator (Mumbai)",
        "tenure_months": 4,
        "raw_text": "Every time I open the app after SIP deduction, the market crashes next day. I have lost 800 rupees on my 10k investment. Should I redeem now before it drops further?",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.96
    },
    {
        "id": "FB_021",
        "source": "Twitter/X Support",
        "persona": "30yo HR Executive (Gurgaon)",
        "tenure_months": 5,
        "raw_text": "My flexicap fund has given negative returns for last 5 months. Instagram finfluencers said SIP never loses money. Feeling cheated. Stopping it.",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.93
    },
    {
        "id": "FB_022",
        "source": "Play Store Review",
        "persona": "27yo Civil Engineer (Patna)",
        "tenure_months": 3,
        "raw_text": "Red portfolio for 90 days. Why does rupee cost averaging sound good in theory but in practice I just have less money than I put in?",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.85
    },
    {
        "id": "FB_023",
        "source": "Financial Forum",
        "persona": "24yo Business Analyst (Chennai)",
        "tenure_months": 4,
        "raw_text": "I see Nifty reached all-time high on news, but my own mutual fund shows -1.5% return after 4 installments. How is that even mathematically possible?",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.82
    },
    {
        "id": "FB_024",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "26yo Mechanical Engineer (Surat)",
        "tenure_months": 5,
        "raw_text": "5 months invested. Total profit is Rs 42 on 25,000 principal. My father was right, fixed deposit is peaceful. Equity is just stress.",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.90
    },
    {
        "id": "FB_025",
        "source": "Play Store Review",
        "persona": "22yo Customer Support (Thane)",
        "tenure_months": 2,
        "raw_text": "Second instalment debited and portfolio shows -300 loss. I am a student living on pocket money, cannot afford to lose my hard-saved cash.",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.94
    },
    {
        "id": "FB_026",
        "source": "Twitter/X Support",
        "persona": "29yo Architect (Bengaluru)",
        "tenure_months": 6,
        "raw_text": "Half a year into my investing journey and my absolute return is negative 2%. When does the compounding magic actually start working?",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.80
    },
    {
        "id": "FB_027",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "24yo Quality Assurance (Trivandrum)",
        "tenure_months": 3,
        "raw_text": "War news and inflation causing markets to dip. My 3 months of savings are down 6%. Should I stop SIP and wait for war to end?",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.87
    },
    {
        "id": "FB_028",
        "source": "Play Store Review",
        "persona": "28yo High School Teacher (Varanasi)",
        "tenure_months": 4,
        "raw_text": "Every month portfolio drops by 200 Rs. Is my fund manager sleeping? I want safe guaranteed instruments, not gambling.",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.92
    },
    {
        "id": "FB_029",
        "source": "Financial Forum",
        "persona": "25yo Logistics Coordinator (Visakhapatnam)",
        "tenure_months": 5,
        "raw_text": "Been putting 2000/mo since 5 months. Value is 9,800. Lost 200 rupees. Everyone on YouTube said you double money in bull market.",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.93
    },
    {
        "id": "FB_030",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "23yo UI Intern (Noida)",
        "tenure_months": 4,
        "raw_text": "I feel anxious every time the red percentage appears on my home screen. Does DCA really work or am I throwing good money after bad?",
        "ground_truth_category": "EARLY_RETURN_ANXIETY",
        "churn_risk_score": 0.84
    },

    # --- LOCKIN_FLEXIBILITY_MISCONCEPTION (31-40) ---
    {
        "id": "FB_031",
        "source": "Play Store Review",
        "persona": "24yo Retail Clerk (Kanpur)",
        "tenure_months": 2,
        "raw_text": "Is mutual fund SIP like LIC policy? If I miss paying for two months, will my previous invested money get confiscated or locked for 5 years?",
        "ground_truth_category": "LOCKIN_FLEXIBILITY_MISCONCEPTION",
        "churn_risk_score": 0.85
    },
    {
        "id": "FB_032",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "27yo Call Center Exec (Delhi)",
        "tenure_months": 3,
        "raw_text": "I thought mutual fund SIP has mandatory 3-year lockin. If I need my money for home renovation next month, can I withdraw without penalty?",
        "ground_truth_category": "LOCKIN_FLEXIBILITY_MISCONCEPTION",
        "churn_risk_score": 0.72
    },
    {
        "id": "FB_033",
        "source": "Financial Forum",
        "persona": "29yo Small Trader (Madurai)",
        "tenure_months": 4,
        "raw_text": "Can I stop my SIP without paying exit load? My agent told me if you break SIP before 12 months AMC will charge heavy fines.",
        "ground_truth_category": "LOCKIN_FLEXIBILITY_MISCONCEPTION",
        "churn_risk_score": 0.81
    },
    {
        "id": "FB_034",
        "source": "Twitter/X Support",
        "persona": "22yo Recent Graduate (Ranchi)",
        "tenure_months": 1,
        "raw_text": "Will skipping an instalment impact my CIBIL credit score? I am scared the bank will file a default report against my PAN card.",
        "ground_truth_category": "LOCKIN_FLEXIBILITY_MISCONCEPTION",
        "churn_risk_score": 0.79
    },
    {
        "id": "FB_035",
        "source": "Play Store Review",
        "persona": "26yo Lab Technician (Cuttack)",
        "tenure_months": 5,
        "raw_text": "I want to take a break from investing for 3 months due to wedding expenses. Do I have to cancel the entire SIP or is there any pause button?",
        "ground_truth_category": "LOCKIN_FLEXIBILITY_MISCONCEPTION",
        "churn_risk_score": 0.68
    },
    {
        "id": "FB_036",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "25yo Telecom Engineer (Chandigarh)",
        "tenure_months": 3,
        "raw_text": "Is ELSS tax saving lockin applied to all mutual funds? I have an index fund SIP. Am I trapped for 3 years or can I redeem anytime?",
        "ground_truth_category": "LOCKIN_FLEXIBILITY_MISCONCEPTION",
        "churn_risk_score": 0.70
    },
    {
        "id": "FB_037",
        "source": "Financial Forum",
        "persona": "30yo Govt Contractor (Guwahati)",
        "tenure_months": 6,
        "raw_text": "If I cancel my auto-debit on Groww, will AMC send legal notice to my house? My uncle said SIP is an agreement with mutual fund house.",
        "ground_truth_category": "LOCKIN_FLEXIBILITY_MISCONCEPTION",
        "churn_risk_score": 0.88
    },
    {
        "id": "FB_038",
        "source": "Play Store Review",
        "persona": "23yo Food Delivery Partner (Delhi)",
        "tenure_months": 2,
        "raw_text": "Earnings fluctuated this week. Don't want to get penalised if balance is low. Can I just pause for 1 month and resume in April?",
        "ground_truth_category": "LOCKIN_FLEXIBILITY_MISCONCEPTION",
        "churn_risk_score": 0.76
    },
    {
        "id": "FB_039",
        "source": "Twitter/X Support",
        "persona": "27yo IT Recruiter (Kolkata)",
        "tenure_months": 4,
        "raw_text": "Does Groww charge any fee for pausing a SIP? Where is the pause button? I only see 'Delete SIP' option in settings.",
        "ground_truth_category": "LOCKIN_FLEXIBILITY_MISCONCEPTION",
        "churn_risk_score": 0.73
    },
    {
        "id": "FB_040",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "24yo Digital Marketer (Mysore)",
        "tenure_months": 3,
        "raw_text": "People say recurring deposit (RD) has premature penalty. Does SIP also deduct interest if I withdraw my units after 6 months?",
        "ground_truth_category": "LOCKIN_FLEXIBILITY_MISCONCEPTION",
        "churn_risk_score": 0.75
    },

    # --- ADVISORY_SEEKING (41-45) ---
    {
        "id": "FB_041",
        "source": "Play Store Review",
        "persona": "24yo College Student (Dehradun)",
        "tenure_months": 2,
        "raw_text": "Tell me which small cap fund will give 40% return like Quant did last year. I want to shift my 2000 SIP there immediately.",
        "ground_truth_category": "ADVISORY_SEEKING",
        "churn_risk_score": 0.60
    },
    {
        "id": "FB_042",
        "source": "Reddit (r/IndiaInvestments)",
        "persona": "28yo Bank Associate (Surat)",
        "tenure_months": 5,
        "raw_text": "Should I invest in Parag Parikh Flexi Cap or HDFC Top 100? Give me one best recommendation for 10-year horizon.",
        "ground_truth_category": "ADVISORY_SEEKING",
        "churn_risk_score": 0.55
    },
    {
        "id": "FB_043",
        "source": "Financial Forum",
        "persona": "26yo Mechanical Engineer (Pune)",
        "tenure_months": 3,
        "raw_text": "Defense and PSU funds gave 80% rally. My index fund is moving like a tortoise. Should I stop index fund and buy defense sector fund?",
        "ground_truth_category": "ADVISORY_SEEKING",
        "churn_risk_score": 0.64
    },
    {
        "id": "FB_044",
        "source": "Twitter/X Support",
        "persona": "25yo Software QA (Noida)",
        "tenure_months": 4,
        "raw_text": "Gold is hitting record highs. Is it better to switch my monthly equity SIP to Nippon India Gold ETF right now?",
        "ground_truth_category": "ADVISORY_SEEKING",
        "churn_risk_score": 0.58
    },
    {
        "id": "FB_045",
        "source": "Play Store Review",
        "persona": "31yo Civil Engineer (Patna)",
        "tenure_months": 6,
        "raw_text": "Which mutual fund scheme is safest for 5000 per month with zero chance of loss? Please suggest direct name.",
        "ground_truth_category": "ADVISORY_SEEKING",
        "churn_risk_score": 0.62
    },

    # --- UNRECOGNIZED_OTHER (46-50) ---
    {
        "id": "FB_046",
        "source": "Play Store Review",
        "persona": "29yo Small Trader (Indore)",
        "tenure_months": 1,
        "raw_text": "How do I change my registered email address and nominee details on Groww app? Not able to find in profile.",
        "ground_truth_category": "UNRECOGNIZED_OTHER",
        "churn_risk_score": 0.20
    },
    {
        "id": "FB_047",
        "source": "Twitter/X Support",
        "persona": "26yo Executive (Bangalore)",
        "tenure_months": 4,
        "raw_text": "Where can I download my Capital Gains statement for filing ITR-2? Please guide navigation steps.",
        "ground_truth_category": "UNRECOGNIZED_OTHER",
        "churn_risk_score": 0.15
    },
    {
        "id": "FB_048",
        "source": "Play Store Review",
        "persona": "23yo Analyst (Gurgaon)",
        "tenure_months": 2,
        "raw_text": "Biometric fingerprint login is not working after the latest Android 14 update. Have to type PIN every time.",
        "ground_truth_category": "UNRECOGNIZED_OTHER",
        "churn_risk_score": 0.35
    },
    {
        "id": "FB_049",
        "source": "Financial Forum",
        "persona": "27yo Account Manager (Chennai)",
        "tenure_months": 5,
        "raw_text": "Can I add two bank accounts and choose which one to debit for which SIP? Currently all debits go to Canara bank.",
        "ground_truth_category": "UNRECOGNIZED_OTHER",
        "churn_risk_score": 0.30
    },
    {
        "id": "FB_050",
        "source": "Play Store Review",
        "persona": "25yo School Teacher (Shimla)",
        "tenure_months": 3,
        "raw_text": "Dark mode toggle is too hidden inside settings. Please bring it directly to top bar of home screen.",
        "ground_truth_category": "UNRECOGNIZED_OTHER",
        "churn_risk_score": 0.10
    }
]

def export_synthetic_datasets(output_dir: str = "discovery_engine"):
    """Exports feedback dataset as both JSON and CSV files."""
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "synthetic_feedback.json")
    csv_path = os.path.join(output_dir, "synthetic_feedback.csv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(FEEDBACK_DATASET, f, indent=2, ensure_ascii=False)

    df = pd.DataFrame(FEEDBACK_DATASET)
    df.to_csv(csv_path, index=False)

    print(f"✅ Exported {len(FEEDBACK_DATASET)} feedback items to:")
    print(f"   - {json_path}")
    print(f"   - {csv_path}")

    # Summary by category
    summary = df['ground_truth_category'].value_counts()
    print("\n📊 Dataset Distribution by Root Cause:")
    for cat, count in summary.items():
        print(f"   - {cat}: {count} ({count/len(df)*100:.1f}%)")
    
    return json_path, csv_path

if __name__ == "__main__":
    export_synthetic_datasets()
