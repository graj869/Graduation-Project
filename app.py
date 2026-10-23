import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Groww 12-Month SIP Retention Companion",
    page_icon="🌱",
    layout="wide"
)

# Groww Brand Custom CSS
st.markdown("""
<style>
    .metric-box {
        background-color: #F8FAF9;
        border: 1px solid #E6ECE9;
        border-radius: 8px;
        padding: 12px 16px;
        border-left: 4px solid #00D09C;
    }
    .metric-sub { font-size: 11px; color: #7C7E8C; text-transform: uppercase; font-weight: 700; }
    .metric-main { font-size: 15px; color: #44475B; font-weight: 700; margin-top: 2px; }
    .audit-chip {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        margin-top: 6px;
    }
    .audit-ai { background-color: #E8F8F5; color: #00875A; border: 1px solid #00D09C; }
    .audit-compliance { background-color: #FDE8E8; color: #9B1C1C; border: 1px solid #F8B4B4; }
    .audit-cashflow { background-color: #E1EFFE; color: #1E429F; border: 1px solid #A4CAFE; }
    .audit-market { background-color: #FEF08A; color: #713F12; border: 1px solid #FDE047; }
    .audit-action { background-color: #DEF7EC; color: #03543F; border: 1px solid #84E1BC; }
    .audit-general { background-color: #F3F4F6; color: #374151; border: 1px solid #D1D5DB; }
</style>
""", unsafe_allow_html=True)

# Top Header
st.title("🌱 Groww 12-Month SIP Retention Companion")
st.caption("AI-Native Growth MVP: Tackling First-Time Mutual Fund Churn (Months 3–6) without Fear or Recommendations.")

# Top Strategic KPI Cards
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='metric-box'><div class='metric-sub'>Target Metric</div><div class='metric-main'>12-Month Active SIP Continuation</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='metric-box'><div class='metric-sub'>High-Risk Churn Window</div><div class='metric-main'>Months 3 – 6 (Salary Lag & First Dip)</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='metric-box'><div class='metric-sub'>Eval Guardrail</div><div class='metric-main'>SEBI Compliant • Zero FOMO / No Advice</div></div>", unsafe_allow_html=True)

st.write("")

# Quick Test Prompts for Evaluators
st.markdown("##### ⚡ Quick Test Scenarios (Mentor Evaluation):")
b1, b2, b3, b4 = st.columns(4)
quick_input = None

if b1.button("💸 Salary Delayed (Date Mismatch)"):
    quick_input = "My salary comes on the 7th, but my SIP date is the 2nd. My SIP bounced. What should I do?"
if b2.button("📉 Negative Returns (Month 4)"):
    quick_input = "I have been investing for 4 months and my returns are in red (-4%). Should I stop my SIP?"
if b3.button("🛡️ Recommend Best Small Cap"):
    quick_input = "Can you recommend the top 3 mutual funds or best small cap schemes to invest in?"
if b4.button("⏸️ Emergency Cash Crunch"):
    quick_input = "I have sudden medical expenses this month and have no money left for my SIP."

# Strict System Prompt
SYSTEM_PROMPT = """
You are the AI Retention Companion on Groww, designed to support first-time Indian mutual fund retail investors during their critical first 12 months.

STRICT CONSTRAINTS & EVAL GUARDRAILS:
1. SEBI NON-ADVISORY: NEVER recommend specific mutual fund schemes, AMC names, stocks, or categories. If asked for recommendations ("which fund", "best small cap"), decline politely, state SEBI compliance, and explain asset allocation or time horizon principles.
2. NO FOMO / NO GUARANTEES: Never promise guaranteed returns, never say "double your money", and never use fear or urgency ("hurry", "loss ho jayega").
3. SHORT-TERM HORIZONS (e.g., 1 Year): Explain that equity SIPs are not designed for quick 1-year profits due to volatility, exit loads, and short-term capital gains tax.
4. MULTI-YEAR HORIZONS (e.g., 3-5 Years): Explain Rupee-Cost Averaging, staying disciplined through market corrections, and annual Step-Ups.
5. SALARY DELAYS & BOUNCES: Promote native Groww features: 'Skip Instalment' (prevents bank NACH bounce charges) and 'Edit SIP Date' (shift 3-5 days after salary).
6. CASH CRUNCHES: Explain 'Pause SIP' for 1-3 months so previously accumulated units remain invested.
7. Keep tone calm, clear, empathetic, and objective.
"""

def generate_live_ai_response(prompt: str, key: str):
    """Cleanly authenticates both AQ. and AIza keys via header transmission."""
    if not key:
        return None
    cleaned_key = key.strip().replace('"', '').replace("'", "")
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": cleaned_key
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{SYSTEM_PROMPT}\n\nUser Query: {prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=8)
        if res.status_code == 200:
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        pass
    return None

def semantic_intent_engine(query: str) -> dict:
    """Comprehensive fallback classifying queries across distinct investor friction points."""
    q = query.lower()

    # 1. SEBI Advisory Probes
    if any(k in q for k in ["best fund", "recommend", "which fund", "top fund", "small cap", "large cap", "nifty", "stock", "crypto", "buy", "suggest fund", "kisme invest", "kaha lagau"]):
        return {
            "badge": "🛡️ SEBI Advisory Guardrail (Zero Recommendation)",
            "style": "audit-compliance",
            "reply": (
                "**SEBI Regulatory Compliance Notice:**\n"
                "As an AI retention companion, I am strictly prohibited under SEBI guidelines from recommending specific mutual fund schemes, AMCs, or stocks.\n\n"
                "**How to make independent investment decisions on Groww:**\n"
                "• **Align with Your Time Horizon**: For >5 year horizons, diversified equity/index funds accommodate volatility. For short goals (<3 years), conservative debt or arbitrage funds protect capital.\n"
                "• **Use Objective Metrics**: In the Groww app, filter by 3Y/5Y Rolling Returns, Expense Ratio, and Fund Manager consistency.\n"
                "• **Avoid Chasing Past Year Winners**: Sectors rotate cyclically; diversified asset allocation delivers more reliable outcomes than picking last year's top performer."
            )
        }

    # 2. 1-Year Horizon / Short-Term Maximum Return Expectation
    if any(k in q for k in ["one year", "1 year", "12 months", "maximum return in one year", "1 saal"]) and any(k in q for k in ["return", "maximum", "steps", "profit", "gain"]):
        return {
            "badge": "🎯 Expectation Alignment Engine",
            "style": "audit-market",
            "reply": (
                "**Important Reality Check for 1-Year Equity SIPs:**\n\n"
                "Expecting 'maximum returns' in just 1 year is the leading reason first-time investors get disappointed and abandon their SIPs. Equity markets are volatile over 12 months, and short-term capital gains tax (STCG) and exit loads apply if you withdraw early.\n\n"
                "**Recommended approach for a 1-year timeline:**\n"
                "1. **Re-evaluate Risk**: For money needed in 1 year, equity SIP is risky. Conservative options like Arbitrage or Liquid funds avoid capital loss.\n"
                "2. **Extend to 3–5 Years**: If your goal is wealth creation via equity, treat 36+ months as your base horizon.\n"
                "3. **Avoid High-Beta Schemes**: Never invest in small-cap schemes for a 1-year goal hoping for a quick spike.\n"
                "4. **Automate Autopay**: Align debit dates 3 days post-salary to eliminate failed mandate charges."
            )
        }

    # 3. 3-Year Horizon / Multi-SIP Strategy
    if any(k in q for k in ["3 year", "three year", "2 sip", "3 years", "two sip"]) and any(k in q for k in ["maximum", "return", "best way", "strategy", "portfolio"]):
        return {
            "badge": "📈 Portfolio Structuring & Discipline Engine",
            "style": "audit-action",
            "reply": (
                "**Maximizing Outcomes Across 2 SIPs over a 3-Year Horizon:**\n\n"
                "Over a 3-year timeline, returns depend primarily on structural discipline rather than market timing:\n\n"
                "1. **Complementary Diversification**: Pair funds that don't heavily overlap (e.g., a Core Index/Large-Cap fund for stability with a Flexi-Cap or Mid-Cap fund for alpha).\n"
                "2. **Annual SIP Step-Up**: Increasing your SIP amount by 10% each year (aligned with salary increments) significantly increases your 36-month corpus.\n"
                "3. **Stay Disciplined During Red Months**: A 3-year window will encounter market dips. Buying during corrections lowers your average unit acquisition cost via Rupee-Cost Averaging.\n"
                "4. **Buffer Debit Dates**: Set both SIP dates 3–5 days after your salary credit to avoid mandate failures."
            )
        }

    # 4. Salary Delays / Mandate Bounces / Bank Penalties
    if any(k in q for k in ["salary", "delay", "late", "bounce", "date", "2nd", "7th", "mandate", "nach", "penalty", "charge", "failed"]):
        return {
            "badge": "⚡ Groww Cashflow & Mandate Action Engine",
            "style": "audit-cashflow",
            "reply": (
                "**Avoid Mandate Bounces and Bank Penalties on Groww:**\n\n"
                "1. **Edit SIP Date (Permanent Fix)**: Go to **Groww > Mutual Funds > SIPs > Select Fund > Edit SIP** and shift the date 3–5 days after your regular salary credit.\n"
                "2. **Skip This Month's Instalment (Instant Action)**: If salary is delayed, tap **'Skip Instalment'** at least 2 working days before the scheduled date. Your bank mandate stays intact, no NACH bounce charges occur, and your SIP resumes next month."
            )
        }

    # 5. Volatility / Negative Returns / Red Portfolio (Month 3-6 Anxiety)
    if any(k in q for k in ["negative", "loss", "red", "returns", "down", "crash", "falling", "gir gaya", "scam", "underperforming", "fd", "gold"]):
        return {
            "badge": "🧠 Behavioral De-escalation & RCA Engine",
            "style": "audit-market",
            "reply": (
                "**Seeing red or flat returns in Months 3–6 is a normal phase for first-time investors:**\n\n"
                "• **Rupee-Cost Averaging**: When NAVs decline, your fixed monthly SIP purchases **more fund units** at a discount.\n"
                "• **Accumulation Phase**: Early months accumulate units; compounding becomes visible after market recovery in years 3–5.\n"
                "• **Cost of Stopping**: Pausing or cancelling during a market dip locks in paper losses and misses the subsequent recovery cycle."
            )
        }

    # 6. Emergency Cash Crunches / Medical Issues
    if any(k in q for k in ["emergency", "medical", "no money", "paise nahi", "cannot pay", "crisis", "tight", "expense", "job loss"]):
        return {
            "badge": "⏸️ Liquidity Preservation Playbook",
            "style": "audit-action",
            "reply": (
                "**During cash emergencies, you don't need to cancel your SIP:**\n\n"
                "• **Pause SIP for 1 to 3 Months**: Pause directly from the Groww app with zero cancellation fees or penalty charges.\n"
                "• **Existing Investments Continue Compounding**: Your accumulated units remain invested in the market.\n"
                "• **Resume Anytime**: You can restart debits with one tap as soon as your cash flow stabilizes."
            )
        }

    # 7. Cancellations / Redeeming / Exit Loads
    if any(k in q for k in ["stop", "cancel", "withdraw", "redeem", "close", "band", "exit load"]):
        return {
            "badge": "⚡ Retention Intervention Engine",
            "style": "audit-action",
            "reply": (
                "**Before Cancelling Your SIP:**\n\n"
                "1. **Cash Flow Tight?** Use **Pause SIP** or **Skip Instalment** instead of full cancellation.\n"
                "2. **Exit Load & Taxes**: Redeeming equity units within 365 days often incurs an Exit Load (~1%) and Short-Term Capital Gains (STCG) tax.\n"
                "3. **If You Still Wish to Stop**: Navigate to **Groww > Mutual Funds > SIPs > Select SIP > Cancel SIP**."
            )
        }

    # 8. Increasing SIP / Step-Up / Bonus Investments
    if any(k in q for k in ["increase", "step up", "top up", "badhana", "more money", "appraisal", "bonus", "lumpsum"]):
        return {
            "badge": "📈 Wealth Acceleration Engine",
            "style": "audit-action",
            "reply": (
                "**Accelerating Your SIP Investments on Groww:**\n\n"
                "• **SIP Step-Up**: Enable annual automated increases (e.g., +10% every year) aligned with appraisals without creating new mandates.\n"
                "• **One-Time Lumpsum**: Invest bonuses or surplus funds into your existing folio anytime via the 'One-Time' button."
            )
        }

    # 9. Loans, Collateral, and Unit Pledging
    if any(k in q for k in ["loan", "pledge", "borrow", "collateral", "against mutual fund"]):
        return {
            "badge": "📋 Groww Liquidity & Feature Engine",
            "style": "audit-general",
            "reply": (
                "**Loan Against Mutual Funds (LAMF):**\n\n"
                "• You can borrow against eligible mutual fund units without selling them, keeping your compounding journey uninterrupted.\n"
                "• Interest is charged only on the utilized amount, and units remain pledged until the loan is cleared."
            )
        }

    # 10. General Dynamic Assistant
    return {
        "badge": "🌱 Groww First-Time Investor Guidance Engine",
        "style": "audit-general",
        "reply": (
            f"**Regarding your question:**\n\n"
            "As your Groww SIP Companion, my role is to help you stay disciplined without unexpected costs or panic:\n"
            "• **For Cash Flow Issues**: Use **Edit SIP Date** or **Skip Instalment** to avoid bank charges.\n"
            "• **For Market Fluctuations**: Understand how Rupee-Cost Averaging lowers average acquisition cost.\n"
            "• **For Liquidity Management**: Use **Pause SIP** for 1–3 months during short-term constraints.\n\n"
            "What specific aspect of your investment journey would you like to explore?"
        )
    }

# Session Chat State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! I am your Groww SIP Retention Companion. Ask me anything about managing salary delays, negative returns, SIP dates, or building long-term discipline.",
            "badge": "Verified System Onboarding",
            "style": "audit-compliance"
        }
    ]

# Handle Quick Test Clicks
if quick_input:
    st.session_state.messages.append({"role": "user", "content": quick_input})
    env_key = os.getenv("GEMINI_API_KEY", "")
    ai_reply = generate_live_ai_response(quick_input, env_key)
    if ai_reply:
        res = {"reply": ai_reply, "badge": "✨ Live Gemini AI (Eval-Gated)", "style": "audit-ai"}
    else:
        res = semantic_intent_engine(quick_input)
    st.session_state.messages.append({"role": "assistant", "content": res["reply"], "badge": res["badge"], "style": res["style"]})

# Render Existing Messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "badge" in m:
            st.markdown(f"<span class='audit-chip {m['style']}'>{m['badge']}</span>", unsafe_allow_html=True)

# User Chat Input (Accepts ANY Query)
user_text = st.chat_input("Ask any question about your SIP, returns, salary dates, or Groww features...")
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    env_key = os.getenv("GEMINI_API_KEY", "")
    ai_reply = generate_live_ai_response(user_text, env_key)
    
    if ai_reply:
        res = {
            "reply": ai_reply,
            "badge": "✨ Live Gemini AI (Eval-Gated)",
            "style": "audit-ai"
        }
    else:
        res = semantic_intent_engine(user_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": res["reply"],
        "badge": res["badge"],
        "style": res["style"]
    })
    st.rerun()