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

# Custom Styling (Groww Brand Identity)
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
    .audit-action { background-color: #DEF7EC; color: #03543F; border: 1px solid #84E1BC; }
    .audit-cashflow { background-color: #E1EFFE; color: #1E429F; border: 1px solid #A4CAFE; }
    .audit-market { background-color: #FEF08A; color: #713F12; border: 1px solid #FDE047; }
</style>
""", unsafe_allow_html=True)

# Strategic Header
st.title("🌱 Groww 12-Month SIP Retention Companion")
st.caption("AI-Native Growth MVP: Tackling First-Time Mutual Fund Churn (Months 3–6) without Fear or Recommendations.")

# Top Strategic Context Cards
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

SYSTEM_PROMPT = """
You are the AI Retention Companion on Groww, designed to support first-time Indian mutual fund retail investors during their critical first 12 months.

MANDATORY SEBI & PRODUCT GUARDRAILS:
1. SEBI NON-ADVISORY: NEVER recommend specific mutual fund schemes, AMC names, stocks, or categories. If asked for recommendations ("which fund", "best small cap"), decline politely, state SEBI compliance, and explain asset allocation or time horizon principles.
2. ZERO FOMO / NO GUARANTEES: Never promise guaranteed returns, never say "double your money", and never use fear or urgency ("hurry", "loss ho jayega").
3. LEGAL & POLICE NOTICE CLARITY: Clarify that mutual funds are voluntary investments, NOT bank loans or EMIs. Missing a payment NEVER causes a police notice, legal action, or CIBIL default.
4. RETENTION PLAYBOOK ON GROWW:
   - For salary delays/bounces: Advise 'Skip Instalment' (prevents bank NACH bounce fees) or 'Edit SIP Date' (set 3-5 days after salary).
   - For temporary job loss/cash crunch: Guide user to 'Pause SIP for 1-3 Months' so existing units stay invested.
   - For bonus/lumpsum: Advise adding a One-Time investment into the same folio without creating duplicate SIPs.
   - For allotment delays (money debited but units not showing): Explain T+1 to T+2 business day NAV allotment by the AMC.
   - For red returns: Explain Rupee-Cost Averaging (RCA).
5. TONE: Calm, reassuring, educational, objective, and transparent.
"""

@st.cache_data(ttl=3600)
def discover_active_model(cleaned_key: str):
    """Dynamically queries Google AI Studio to discover which models are active for this key."""
    if not cleaned_key:
        return None
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    headers = {"x-goog-api-key": cleaned_key}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            models_data = res.json().get("models", [])
            # Priority preference: flash models
            for pref in ["models/gemini-2.0-flash", "models/gemini-1.5-flash", "models/gemini-1.5-flash-latest", "models/gemini-2.5-flash"]:
                for m in models_data:
                    if m.get("name") == pref and "generateContent" in m.get("supportedGenerationMethods", []):
                        return pref
            # Fallback to any model supporting generateContent
            for m in models_data:
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    return m.get("name")
    except Exception:
        pass
    return "models/gemini-1.5-flash"

def generate_ai_response(prompt: str, key: str):
    """Executes live AI call using dynamically resolved active endpoint."""
    if not key:
        return None, None, None
        
    cleaned_key = key.strip().replace('"', '').replace("'", "")
    model_name = discover_active_model(cleaned_key) or "models/gemini-1.5-flash"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": cleaned_key
    }
    payload = {
        "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\nUser Question: {prompt}"}]}],
        "generationConfig": {"temperature": 0.25}
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=6)
        if res.status_code == 200:
            text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            if any(w in prompt.lower() for w in ["best fund", "recommend", "which fund", "stock"]):
                badge = "🛡️ SEBI Advisory Guardrail Applied"
                style = "audit-compliance"
            else:
                badge = f"✨ Live Gemini AI ({model_name.replace('models/', '')})"
                style = "audit-ai"
            return text, badge, style
    except Exception:
        pass
    return None, None, None

def universal_smart_fallback(query: str) -> dict:
    """Comprehensive fallback classifying queries across all real-world retail investor friction points."""
    q = query.lower()

    # 1. Bonus / Extra Money / Lumpsum into Existing SIP (English & Hinglish)
    if any(k in q for k in ["bonus", "extra", "10,000", "10000", "5000", "lumpsum", "one-time", "purani sip", "daal sakta", "nayi shuru", "add money", "holi", "diwali"]):
        return {
            "badge": "📈 Wealth Acceleration & Folio Management",
            "style": "audit-action",
            "reply": (
                "**Aapko nayi SIP shuru karne ki bilkul zaroorat nahi hai!**\n\n"
                "Aap apne bonus ya extra paise ko usi purani SIP/folio me aasaani se add kar sakte hain:\n\n"
                "• **One-Time Lumpsum Option**: Groww dashboard par apne us fund par click karein aur **'One-Time' (Lumpsum)** select karein. Wahan apna amount daalkar payment kar dein.\n"
                "• **Same Folio Me Judega**: Yeh amount aapke purane units ke sath hi add ho jayega aur aapka monthly SIP mandate (AutoPay) pehle ki tarah chalta rahega.\n"
                "• **Clean Portfolio**: Ek hi fund me multiple SIPs banane se portfolio track karna mushkil hota hai, isliye One-Time investment karna best practice hai."
            )
        }

    # 2. SEBI Advisory Probes (Zero Recommendation Guardrail)
    if any(k in q for k in ["best fund", "recommend", "which fund", "top fund", "small cap", "large cap", "nifty", "stock", "crypto", "kisme invest", "kaha lagau"]):
        return {
            "badge": "🛡️ SEBI Advisory Guardrail (Zero Recommendation)",
            "style": "audit-compliance",
            "reply": (
                "**SEBI Regulatory Compliance Notice:**\n"
                "As an AI companion on Groww, I am strictly prohibited under SEBI guidelines from recommending specific mutual fund schemes, AMCs, or stocks.\n\n"
                "**How to evaluate funds objectively on Groww:**\n"
                "• **Rolling Returns (3Y & 5Y)**: Look for consistency across market ups and downs rather than last year's top performer.\n"
                "• **Expense Ratio & Tracking Error**: Lower expense ratios protect your compounding over long horizons.\n"
                "• **Horizon Matching**: Choose funds that match your goal duration (>5 years for equity)."
            )
        }

    # 3. Legal Panic / Police Case / Notice / CIBIL / Job Loss Fear
    if any(k in q for k in ["police", "case", "notice", "jail", "legal", "court", "cibil", "crime", "action aayega", "kanoon", "job chhod"]):
        return {
            "badge": "🛡️ Legal & Compliance Assurance Engine",
            "style": "audit-action",
            "reply": (
                "**Bilkul nahi! Koi police case, legal notice ya FIR nahi hoti.**\n\n"
                "• **SIP Loan ya EMI nahi hai**: Mutual Fund aapka voluntary investment hai. Agar bank me paise nahi honge toh SIP bas us mahine execute nahi hogi. Yeh koi loan default ya apradh nahi hai.\n"
                "• **Bank Bounce Charge se bachein**: Agar bank mandate try karega aur account balance nahi hoga, toh aapka bank ₹250–₹500 mandate bounce penalty kaat sakta hai.\n"
                "• **Action Plan**: Groww app me jakar **'Pause SIP for 1-3 Months'** kar dijiye. Isse mandate pause ho jayega, zero bank charge lagega, aur purana paisa safe rahega!"
            )
        }

    # 4. Allotment Delay / Missing Units / Fraud Fears (T+1 / T+2 Days)
    if any(k in q for k in ["fraud", "scam", "kat gaya", "portfolio 0", "not showing", "paisa doob", "kaha gaya", "gayab", "debited but", "units not"]):
        return {
            "badge": "⏱️ Transaction & Allotment Assurance",
            "style": "audit-cashflow",
            "reply": (
                "**Aapka paisa 100% safe hai, bilkul pareshan na hon!**\n\n"
                "Mutual Fund units allot hone ka ek standard cycle hota hai:\n"
                "• **Day 0**: Aapke bank se AutoPay debit hota hai.\n"
                "• **T+1 se T+2 Working Days**: AMC us din ke NAV par units allot karta hai.\n"
                "• Jaise hi AMC confirmation bhejta hai, Groww dashboard par units aur portfolio value reflect ho jati hai.\n\n"
                "Aap **Profile > All Orders** me jakar real-time order status dekh sakte hain."
            )
        }

    # 5. Changing / Reducing SIP Amount (₹2,000 to ₹1,000)
    if any(k in q for k in ["change", "reduce", "decrease", "kam karna", "ghatana", "amount"]) and any(k in q for k in ["sip", "monthly", "2000", "1000", "500", "expenses"]):
        return {
            "badge": "⚡ Flexible SIP Adjustment Engine",
            "style": "audit-action",
            "reply": (
                "**Yes! Reducing your monthly amount is much smarter than stopping your SIP completely:**\n\n"
                "1. Go to **Groww App > Mutual Funds > SIPs**.\n"
                "2. Select your active SIP and tap **'Edit SIP'**.\n"
                "3. Choose **'Edit Amount'**, change ₹2,000 to ₹1,000 (subject to the fund's minimum requirement, usually ₹500 or ₹1,000), and confirm with OTP.\n\n"
                "• If expenses are tight for only this month, you can also tap **'Skip Instalment'** with 1 tap."
            )
        }

    # 6. Tax Inquiries on Monthly Debits
    if any(k in q for k in ["tax", "tds", "income tax", "capital gain", "deduct tax"]):
        return {
            "badge": "📋 Taxation & Transparency Engine",
            "style": "audit-action",
            "reply": (
                "**No, you do NOT pay income tax when your SIP is debited each month:**\n\n"
                "• **Zero Tax on Monthly Investment**: Your monthly SIP buys units at that day's NAV without any TDS or deduction.\n"
                "• **Tax Only on Redemption**: Tax applies only when you sell (redeem) your units, and only on the profit earned (Capital Gains).\n"
                "• **Equity Timeline**: Holding units over 12 months qualifies as Long-Term Capital Gains (LTCG)."
            )
        }

    # 7. Redemption / Shaadi / Emergency Timeline
    if any(k in q for k in ["shaadi", "wedding", "nikalna", "withdraw", "redeem", "kitne din", "bank me kab"]):
        return {
            "badge": "📋 Liquidity & Redemption Engine",
            "style": "audit-action",
            "reply": (
                "**Paisa nikalna aur timeline:**\n\n"
                "• **Kitne din me aayega**: Equity mutual funds ka redemption period **T+2 se T+3 working days** hota hai. Amount direct aapke verified bank account me credit ho jayega.\n"
                "• **Exit Load Check**: Agar investment ko 1 saal se kam hua hai, toh ~1% exit load lag sakta hai.\n"
                "• **How to Redeem**: **Groww App > Dashboard > Select Fund > Redeem** par click karein."
            )
        }

    # 8. Salary Delay / Cashflow / Mandate Bounce
    if any(k in q for k in ["salary", "delay", "late", "bounce", "date", "mandate", "nach", "penalty", "fine"]):
        return {
            "badge": "⚡ Groww Cashflow & Mandate Action Engine",
            "style": "audit-cashflow",
            "reply": (
                "**Avoid Mandate Bounces and Bank Penalties on Groww:**\n\n"
                "1. **Edit SIP Date**: Set your debit date 3–5 days after your salary credit to prevent recurring bounces.\n"
                "2. **Skip Instalment**: If cash is tight this month, tap **'Skip Instalment'** at least 2 working days before the scheduled debit date to prevent bank NACH bounce charges."
            )
        }

    # 9. Volatility & Red Returns Panic (Months 3 to 6)
    if any(k in q for k in ["negative", "loss", "red", "returns", "down", "crash", "falling", "gir gaya"]):
        return {
            "badge": "🧠 Behavioral De-escalation & RCA Engine",
            "style": "audit-market",
            "reply": (
                "**Seeing red or negative returns in early months is normal:**\n\n"
                "• **Rupee-Cost Averaging**: When NAVs drop, your fixed SIP buys **more fund units** at a discount.\n"
                "• Early months represent the **accumulation phase**; compounding becomes visible after market recovery.\n"
                "• Stopping during a dip locks in paper losses and misses the recovery rally."
            )
        }

    # 10. Intelligent Universal Catch-All
    return {
        "badge": "🌱 Groww Retention Guidance Engine",
        "style": "audit-action",
        "reply": (
            f"**Regarding your question:**\n\n"
            "As your Groww SIP Companion, I help first-time investors navigate their journey without stress:\n"
            "• **Managing Cashflow**: You can edit instalment amounts, shift debit dates, or skip debits to avoid bank bounce fees.\n"
            "• **Market Perspective**: Short-term volatility benefits recurring SIPs by lowering average unit cost over time via Rupee-Cost Averaging.\n"
            "• **Flexibility**: Use 'Pause SIP' (1–3 months) during emergencies to keep accumulated units invested.\n\n"
            "How can I help you adjust your SIP settings today?"
        )
    }

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! I am your Groww SIP Retention Companion. Ask me anything about managing salary delays, changing SIP amounts, market dips, taxation, or Groww features.",
            "badge": "Verified System Onboarding",
            "style": "audit-compliance"
        }
    ]

# Handle Quick Test Prompts
if quick_input:
    st.session_state.messages.append({"role": "user", "content": quick_input})
    env_key = os.getenv("GEMINI_API_KEY", "")
    ai_text, badge, style = generate_ai_response(quick_input, env_key)
    if ai_text:
        reply_dict = {"reply": ai_text, "badge": badge, "style": style}
    else:
        reply_dict = universal_smart_fallback(quick_input)
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply_dict["reply"],
        "badge": reply_dict["badge"],
        "style": reply_dict["style"]
    })

# Render Conversation History
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
    ai_text, badge, style = generate_ai_response(user_text, env_key)
    
    if ai_text:
        reply_dict = {"reply": ai_text, "badge": badge, "style": style}
    else:
        reply_dict = universal_smart_fallback(user_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply_dict["reply"],
        "badge": reply_dict["badge"],
        "style": reply_dict["style"]
    })
    st.rerun()