import os
import re
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Groww SIP Retention Companion",
    page_icon="🌱",
    layout="wide"
)

# Custom Styling to match Groww design system
st.markdown("""
<style>
    .metric-card {
        background-color: #f7f9fb;
        border-radius: 10px;
        padding: 14px 18px;
        border-left: 4px solid #00D09C;
        margin-bottom: 12px;
    }
    .badge-guardrail {
        background-color: #E8F8F5;
        color: #00875A;
        font-size: 11px;
        padding: 3px 8px;
        border-radius: 12px;
        font-weight: 600;
        display: inline-block;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🌱 Groww AI Growth Engine")
    st.caption("PM Graduation Project: 12-Month SIP Retention")
    st.markdown("---")
    
    st.markdown("#### Gemini API Authentication")
    env_key = os.getenv("GEMINI_API_KEY", "")
    
    use_manual = st.checkbox("Override / Input API Key Manually", value=not bool(env_key))
    if use_manual:
        api_key = st.text_input("Enter Key", value=env_key, type="password")
    else:
        api_key = env_key
        st.success("🟢 Key loaded from .env")

    st.markdown("---")
    st.markdown("#### 🛡️ Compliance & Guardrails")
    st.markdown("✅ **No Fund/Stock Advice** (SEBI Compliant)")
    st.markdown("✅ **No FOMO / Urgent Nudges**")
    st.markdown("✅ **Eval-Gated Fallback Engine**")

st.title("🌱 Groww 12-Month SIP Retention Companion")
st.caption("AI-Native Growth Intervention for First-Time Indian Mutual Fund Investors")

# Top KPI highlights
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='metric-card'><b>Target Metric</b><br>12-Month Active SIP Retention</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='metric-card'><b>High-Risk Churn Window</b><br>Months 3 – 6 (Initial Anxiety)</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='metric-card'><b>Intervention Pillar</b><br>Cashflow Mismatch & Panic De-escalation</div>", unsafe_allow_html=True)

SYSTEM_PROMPT = """
You are the Groww SIP Journey Assistant designed specifically to retain first-time Indian retail investors.
CONSTRAINTS:
1. Never suggest specific mutual fund schemes, stocks, AMCs, or categories.
2. If the user asks for recommendations, decline politely and explain principles like diversification.
3. For cash crunches or salary delays, suggest native actions: 'Skip Next Instalment', 'Pause SIP for 1-3 Months', or 'Change SIP Date'.
4. For negative returns in early months, explain Rupee Cost Averaging without fear or false promises.
"""

def deterministic_eval_engine(user_query: str) -> dict:
    """Deterministic fallback and guardrail rule engine."""
    q = user_query.lower()
    
    # Check 1: Recommendation probe (SEBI Compliance Guardrail)
    if any(k in q for k in ["best fund", "which fund", "recommend", "small cap", "large cap", "kisme invest", "kaha lagau"]):
        return {
            "source": "🛡️ SEBI Compliance Guardrail",
            "reply": (
                "Main kisi specific mutual fund ya stock ki recommendation nahi de sakta, "
                "kyunki Groww par hum independent aur unbiased investing ko promote karte hain.\n\n"
                "**Aapke liye smart approach:**\n"
                "• Apne investment horizon (3 saal, 5 saal ya 10 saal) ke hisaab se risk profile decide karein.\n"
                "• Existing SIP ko consistently chalne dein taaki Rupee-Cost Averaging ka pura fayda mile."
            )
        }
        
    # Check 2: Salary delay / Cash crunch / Bounce risk
    if any(k in q for k in ["salary late", "paise nahi", "bounce", "paise kam", "delay", "tangi", "cash crunch"]):
        return {
            "source": "⚡ Groww Retention Action Engine",
            "reply": (
                "Salary delay ki wajah se SIP cancel karne ki bilkul zaroorat nahi hai! Groww par aap bina penalty ke ye options use kar sakte hain:\n\n"
                "1. **Skip Instalment:** Is mahine ki instalment skip kar dijiye. Bank se koi mandate penalty nahi lagegi aur agle mahine SIP apne aap resume ho jayegi.\n"
                "2. **Edit SIP Date:** Agar har mahine salary late aati hai, toh SIP date ko salary aane ke 2-3 din baad (e.g. 7th ya 10th) par shift kar lein.\n"
                "3. **Pause SIP:** 1 se 3 mahine ke liye SIP temporary pause karein taaki cash flow recover ho sake."
            )
        }

    # Check 3: Market dip / Negative returns panic (Months 3-6 Churn)
    if any(k in q for k in ["loss", "negative", "red", "returns kam", "gir gaya", "band kar du", "stop"]):
        return {
            "source": "🧠 Panic De-escalation Engine",
            "reply": (
                "Pehle 3 se 6 mahino mein portfolio ka flat ya thoda negative dikhna bilkul normal hai. "
                "Isko **Rupee-Cost Averaging** ke roop mein samjhein:\n\n"
                "• Jab market down hota hai, aapki wahi SIP amount **zyada units** purchase karti hai.\n"
                "• Jab market recover karega, toh yahi low-cost units aapke portfolio ko strong growth dengi.\n"
                "• Agar emergency nahi hai, toh SIP ko band karne ke bajaye consistent rehna sabse safe rehta hai."
            )
        }
        
    # General helpful response
    return {
        "source": "🌱 SIP Retention Assistant",
        "reply": (
            "Aapki SIP journey ko smooth banana hamara focus hai. "
            "Aap instalment date edit kar sakte hain, temporary pause/skip kar sakte hain, "
            "ya market volatility ke dauran long-term compounding principles samajh sakte hain. "
            "Aap is mahine kya challenge face kar rahe hain?"
        )
    }

def generate_response(prompt: str, key: str) -> dict:
    cleaned_key = key.strip() if key else ""
    
    # Try remote API if key is present
    if cleaned_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": cleaned_key
        }
        payload = {
            "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\nUser: {prompt}"}]}],
            "generationConfig": {"temperature": 0.2}
        }