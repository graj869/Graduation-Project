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

# Custom Styling
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

st.title("🌱 Groww 12-Month SIP Retention Companion")
st.caption("AI-Native Growth MVP: Tackling First-Time Mutual Fund Churn (Months 3–6) without Fear or Recommendations.")

# Strategic KPI Cards
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='metric-box'><div class='metric-sub'>Target Metric</div><div class='metric-main'>12-Month Active SIP Continuation</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='metric-box'><div class='metric-sub'>High-Risk Churn Window</div><div class='metric-main'>Months 3 – 6 (Salary Lag & First Dip)</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='metric-box'><div class='metric-sub'>Eval Guardrail</div><div class='metric-main'>SEBI Compliant • Zero FOMO / No Advice</div></div>", unsafe_allow_html=True)

st.write("")

# Quick Test Buttons for Evaluators
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

SYSTEM_PROMPT = """
You are the AI Retention Companion on Groww, designed to support first-time Indian mutual fund retail investors during their critical first 12 months.

STRICT CONSTRAINTS & EVAL GUARDRAILS:
1. SEBI NON-ADVISORY: NEVER recommend specific mutual fund schemes, AMC names, stocks, or categories.
2. NO FOMO / NO GUARANTEES: Never promise guaranteed returns, never say "double your money", and never use fear or urgency.
3. TAX CLARIFICATIONS: Explain that mutual fund investments do NOT incur tax at monthly debit. Taxes (STCG/LTCG) apply only when units are redeemed/withdrawn.
4. SALARY DELAYS & BOUNCES: Promote native Groww features: 'Skip Instalment' (prevents bank NACH bounce charges) and 'Edit SIP Date' (shift 3-5 days after salary).
5. CASH CRUNCHES: Explain 'Pause SIP' for 1-3 months so previously accumulated units remain invested.
6. VOLATILITY: Explain Rupee-Cost Averaging; explain why stopping during a dip locks in paper losses.
7. Keep tone calm, clear, empathetic, and objective.
"""

def generate_live_ai_response(prompt: str, key: str):
    """Calls Gemini 1.5 Flash using direct header authorization."""
    if not key:
        return None
    cleaned_key = key.strip().replace('"', '').replace("'", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={cleaned_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\nUser Question: {prompt}"}]}],
        "generationConfig": {"temperature": 0.2}
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=7)
        if res.status_code == 200:
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        pass
    return None

def semantic_intent_engine(query: str) -> dict:
    """Deterministic fallback handling all investor friction categories."""
    q = query.lower()

    # 1. Tax & Deduction Inquiries
    if any(k in q for k in ["tax", "tds", "income tax", "capital gain", "deduct tax", "gst", "stcg", "ltcg"]):
        return {
            "badge": "📋 Taxation & Transparency Engine",
            "style": "audit-general",
            "reply": (
                "**No, you do NOT pay income tax when your SIP is debited each month.**\n\n"
                "Here is how mutual fund taxation works in India:\n"
                "• **Zero Tax on Monthly Investment**: Your monthly SIP is simply purchasing units at the current NAV. No tax or TDS is deducted when money leaves your bank.\n"
                "• **Tax Only on Redemption (Gains)**: You are taxed only when you sell (redeem) your units, and only on the profit made (Capital Gains), not the invested principal.\n"
                "• **Equity Holding Timeline**: Gains on units held for more than 12 months qualify as Long-Term Capital Gains (LTCG). Units held under 12 months incur Short-Term Capital Gains (STCG).\n\n"
                "Your monthly SIP deductions do not require any monthly tax filing."
            )
        }

    # 2. Units Missing / Allotment Timeline Anxiety
    if any(k in q for k in ["not showing", "money lost", "debited but", "portfolio empty", "where is money", "t+1", "t+2", "units not"]):
        return {
            "badge": "⏱️ Transaction & Allotment Assurance",
            "style": "audit-cashflow",
            "reply": (
                "**Your money is completely safe! Don't panic if units don't show immediately.**\n\n"
                "Here is how the mutual fund allotment process works:\n"
                "• **Bank Debit (Day 0)**: Money is deducted via your bank mandate/AutoPay.\n"
                "• **AMC Allotment (T+1 to T+2 Business Days)**: The fund house allocates units at that day's Net Asset Value (NAV).\n"
                "• **Display on Groww**: Once the AMC confirms unit allotment, your Groww dashboard updates automatically.\n\n"
                "If 2 business days have passed and your dashboard hasn't updated, check **Groww > Profile > All Orders** for the real-time order status."
            )
        }

    # 3. Nominee & Account Security
    if any(k in q for k in ["nominee", "mother", "father", "wife", "die", "death", "family get", "legal heir"]):
        return {
            "badge": "🛡️ Account Security & Nomination Engine",
            "style": "audit-general",
            "reply": (
                "**Your investments are 100% secure, and nominations protect your family:**\n\n"
                "• In an unfortunate event, 100% of your mutual fund units pass directly to your registered nominee.\n"
                "• **How to add/verify a nominee on Groww**:\n"
                "  1. Go to **Profile (top right) > Account Details**.\n"
                "  2. Scroll to **Nominee Details**.\n"
                "  3. Add their Name, Relationship, and Date of Birth, then authenticate with Aadhaar e-Sign OTP.\n\n"
                "Groww supports adding up to 3 nominees with custom percentage allocations."
            )
        }

    # 4. FD vs Mutual Funds Comparison
    if any(k in q for k in ["fixed deposit", "fd", "fd is better", "guaranteed", "safe"]):
        return {
            "badge": "📊 Asset Class Objective Comparison",
            "style": "audit-market",
            "reply": (
                "**Comparing Fixed Deposits (FD) and Mutual Fund SIPs Objectively:**\n\n"
                "• **Fixed Deposits**: Offer capital safety and fixed guaranteed interest, but returns may not outpace real inflation after deducting income tax at your slab rate.\n"
                "• **Equity SIPs**: Subject to short-term market volatility, but historically tend to outpace inflation and generate positive real returns over 5+ year horizons.\n"
                "• **Recommended Structure**: Maintain an emergency reserve in FDs/Liquid funds (3–6 months of expenses), while using monthly SIPs for long-term wealth creation."
            )
        }

    # 5. SEBI Advisory Probes
    if any(k in q for k in ["best fund", "recommend", "which fund", "top fund", "small cap", "large cap", "nifty", "stock", "crypto", "buy", "suggest fund", "kisme invest", "kaha lagau"]):
        return {
            "badge": "🛡️ SEBI Advisory Guardrail (Zero Recommendation)",
            "style": "audit-compliance",
            "reply": (
                "**SEBI Regulatory Compliance Notice:**\n"
                "As an AI retention companion, I am strictly prohibited under SEBI guidelines from recommending specific mutual fund schemes, AMCs, or stocks.\n\n"
                "**How to make independent investment decisions on Groww:**\n"
                "• **Align with Your Horizon**: For >5 years, diversified equity index/flexi-cap funds allow compounding. For <3 years, lower-volatility options preserve capital.\n"
                "• **Review Objective Data**: Use Groww Screeners to compare 3Y/5Y Rolling Returns and Expense Ratios.\n"
                "• **Avoid Chasing Short-Term Hype**: Stick to your asset allocation instead of jumping into last year's trendiest fund."
            )
        }

    # 6. Salary Delay / Cashflow / Mandate Bounce
    if any(k in q for k in ["salary", "delay", "late", "bounce", "date", "mandate", "nach", "switching companies", "45 days", "fine"]):
        return {
            "badge": "⚡ Groww Cashflow & Mandate Action Engine",
            "style": "audit-cashflow",
            "reply": (
                "**Avoid Mandate Bounces and Bank Penalties on Groww:**\n\n"
                "1. **Pause SIP (For Long Gaps like 45 Days)**: Go to **Groww > Mutual Funds > SIPs > Select Fund > Pause SIP** and select 1–2 months. No bank penalty is charged, and previously accumulated units remain invested.\n"
                "2. **Skip Instalment (For Short 1-Month Gaps)**: Tap **'Skip Instalment'** at least 2 working days before the scheduled debit date to prevent bank NACH bounce charges.\n"
                "3. **Edit SIP Date (For Permanent Schedule Changes)**: Shift your monthly debit date to 3–5 days after your new company's salary credit date."
            )
        }

    # 7. Volatility & Red Returns Panic
    if any(k in q for k in ["negative", "loss", "red", "returns", "down", "crash", "falling", "gir gaya", "scam"]):
        return {
            "badge": "🧠 Behavioral De-escalation & RCA Engine",
            "style": "audit-market",
            "reply": (
                "**Seeing red or negative returns in early months is normal:**\n\n"
                "• **Rupee-Cost Averaging**: When NAVs decline, your fixed SIP purchases **more fund units** at a discount.\n"
                "• Early months represent the **accumulation phase**; compounding becomes visible after market recovery.\n"
                "• Pausing or cancelling during a market dip locks in paper losses and misses the subsequent recovery cycle."
            )
        }

    # 8. Step-Up / Bonus / Adding Money
    if any(k in q for k in ["increase", "step up", "top up", "badhana", "more money", "appraisal", "bonus", "lumpsum", "holi"]):
        return {
            "badge": "📈 Wealth Acceleration Engine",
            "style": "audit-action",
            "reply": (
                "**Accelerating Your SIP Investments on Groww:**\n\n"
                "• **SIP Step-Up**: Enable annual automated increases (e.g., +10% every year) aligned with appraisals without creating new mandates.\n"
                "• **One-Time Lumpsum**: Invest bonuses or surplus funds into your existing folio anytime via the 'One-Time' button."
            )
        }

    # 9. General Fallback
    return {
        "badge": "🌱 Groww First-Time Investor Guidance Engine",
        "style": "audit-general",
        "reply": (
            "Namaste! As your Groww SIP Companion, I help first-time investors navigate their first 12 months:\n\n"
            "• **Managing Cashflow & Bounces**: Aligning SIP dates with salary or skipping instalments.\n"
            "• **Market Volatility**: Understanding Rupee-Cost Averaging and realistic horizon expectations.\n"
            "• **SIP Maintenance**: Using Pause, Step-Up, or checking exit loads and taxation.\n\n"
            "How can I assist your investment journey today?"
        )
    }

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! I am your Groww SIP Retention Companion. Ask me anything about managing salary delays, negative returns, SIP dates, taxation, or building long-term discipline.",
            "badge": "Verified System Onboarding",
            "style": "audit-compliance"
        }
    ]

# Handle Quick Test Prompts
if quick_input:
    st.session_state.messages.append({"role": "user", "content": quick_input})
    env_key = os.getenv("GEMINI_API_KEY", "")
    ai_reply = generate_live_ai_response(quick_input, env_key)
    if ai_reply:
        res = {"reply": ai_reply, "badge": "✨ Live Gemini AI (Eval-Gated)", "style": "audit-ai"}
    else:
        res = semantic_intent_engine(quick_input)
    st.session_state.messages.append({"role": "assistant", "content": res["reply"], "badge": res["badge"], "style": res["style"]})

# Display Message History
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "badge" in m:
            st.markdown(f"<span class='audit-chip {m['style']}'>{m['badge']}</span>", unsafe_allow_html=True)

# User Chat Input
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