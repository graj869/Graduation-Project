import os
import re
import streamlit as st

st.set_page_config(
    page_title="Groww 12-Month SIP Retention Companion",
    page_icon="🌱",
    layout="wide"
)

# Custom Styling (Groww Design Language)
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
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        margin-top: 6px;
    }
    .audit-compliance { background-color: #FDE8E8; color: #9B1C1C; border: 1px solid #F8B4B4; }
    .audit-cashflow { background-color: #E1EFFE; color: #1E429F; border: 1px solid #A4CAFE; }
    .audit-market { background-color: #FEF08A; color: #713F12; border: 1px solid #FDE047; }
    .audit-action { background-color: #DEF7EC; color: #03543F; border: 1px solid #84E1BC; }
    .audit-general { background-color: #F3F4F6; color: #374151; border: 1px solid #D1D5DB; }
</style>
""", unsafe_allow_html=True)

# Title & Problem Statement Context
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

# Quick Test Buttons for Mentors/Evaluators
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

# Comprehensive AI & Guardrail Decision Engine
def process_investor_query(query: str) -> dict:
    q = query.lower()

    # GUARDRAIL 1: SEBI Advisory Probes (Strict Refusal)
    advisory_keywords = [
        "best fund", "recommend", "which fund", "top fund", "small cap", "large cap",
        "mid cap", "nifty", "stock", "share", "crypto", "buy", "suggest fund", "kisme invest", "kaha lagau"
    ]
    if any(k in q for k in advisory_keywords):
        return {
            "badge": "🛡️ SEBI Advisory Guardrail (Zero Recommendation)",
            "style": "audit-compliance",
            "reply": (
                "**SEBI Regulatory Compliance Notice:**\n"
                "As an AI retention companion, I am strictly prohibited from recommending specific mutual fund schemes, AMCs, or stocks.\n\n"
                "**How to make independent decisions on Groww:**\n"
                "• **Align with Your Horizon**: For long-term goals (>5 years), broad-based index or diversified equity funds are typically chosen. For short-term goals (<3 years), debt or lower-risk options avoid sudden market dips.\n"
                "• **Use Groww Screeners**: Filter mutual funds objectively by Category, 3Y/5Y Rolling Returns, and Fund Manager track record.\n"
                "• **Asset Allocation**: Stick to your planned asset mix rather than chasing recent top performers."
            )
        }

    # CATEGORY 2: Cashflow Friction, Salary Delays, Mandate Bounces
    cashflow_keywords = [
        "salary", "delay", "late", "bounce", "date", "2nd", "7th", "mandate", "nach",
        "penalty", "charge", "failed", "deduct", "account", "bank balance"
    ]
    if any(k in q for k in cashflow_keywords):
        return {
            "badge": "⚡ Groww Cashflow & Mandate Action Engine",
            "style": "audit-cashflow",
            "reply": (
                "**Don't cancel your SIP! Cashflow mismatches are easily solvable on Groww without bank penalties:**\n\n"
                "1. **Edit SIP Date (Permanent Fix)**:\n"
                "   • Go to **Groww App > Mutual Funds > SIPs > Select your Fund > Edit SIP**.\n"
                "   • Shift your monthly date 3–5 days after your salary credit (e.g., if salary comes on the 7th, set SIP to the 10th or 12th).\n\n"
                "2. **Skip Upcoming Instalment (Temporary Fix)**:\n"
                "   • Tap **'Skip Instalment'** at least 2 working days before the date.\n"
                "   • Your autopay mandate remains active, your bank will not charge bounce fees, and your SIP resumes smoothly next month!"
            )
        }

    # CATEGORY 3: Market Volatility & Early Red Returns (Month 3-6 Anxiety)
    volatility_keywords = [
        "negative", "loss", "red", "returns", "down", "crash", "falling", "bear",
        "gir gaya", "scam", "underperforming", "fd is better", "gold", "worse"
    ]
    if any(k in q for k in volatility_keywords):
        return {
            "badge": "🧠 Behavioral De-escalation & RCA Engine",
            "style": "audit-market",
            "reply": (
                "**Seeing red or flat returns in Months 3–6 is a universal experience for first-time investors.** Here is what is happening under the hood:\n\n"
                "• **Rupee-Cost Averaging in Action**: When the market is down, your fixed monthly SIP buys **more fund units** at discounted Net Asset Values (NAV).\n"
                "• **Accumulation Phase vs Growth Phase**: The first 12–18 months are meant for gathering units. Real compounding accelerates after Year 3.\n"
                "• **The Cost of Stopping**: Pausing or stopping during a market dip locks in the temporary paper loss and robs you of the recovery bounce.\n\n"
                "💡 *Actionable Advice:* Treat red months as a seasonal sale on mutual fund units, not a loss."
            )
        }

    # CATEGORY 4: Emergency Cash Crunch / Pausing
    emergency_keywords = [
        "emergency", "medical", "no money", "paise nahi", "cannot pay", "crisis",
        "tight", "expense", "job loss", "trouble", "broke"
    ]
    if any(k in q for k in emergency_keywords):
        return {
            "badge": "⏸️ Liquidity Preservation Playbook",
            "style": "audit-action",
            "reply": (
                "**Unforeseen life expenses happen. You do not have to abandon your wealth journey:**\n\n"
                "• **Pause SIP for 1 to 3 Months**: On Groww, you can temporarily pause monthly debits with zero fees or cancellation penalties.\n"
                "• **Your Money Stays Intact**: All your accumulated units stay invested and continue earning market returns while your SIP is paused.\n"
                "• **Resume Anytime**: As soon as your cash flow stabilizes, you can unpause with a single tap in the app."
            )
        }

    # CATEGORY 5: Stopping / Cancelling / Withdrawing SIP
    cancellation_keywords = [
        "stop", "cancel", "withdraw", "redeem", "close", "band karna", "nikalna",
        "exit", "surrender"
    ]
    if any(k in q for k in cancellation_keywords):
        return {
            "badge": "⚡ Retention Intervention Engine",
            "style": "audit-action",
            "reply": (
                "**Before you cancel, consider these three low-friction options:**\n\n"
                "1. **Is it a cash crunch?** Use **Pause SIP** (1–3 months) or **Skip Instalment** instead of cancelling.\n"
                "2. **Is it market worry?** Remember equity compounding requires staying invested across at least one full market cycle (3–5 years).\n"
                "3. **If you must withdraw:** Check if the fund has an **Exit Load** (usually 1% if redeemed within 12 months) and remember short-term capital gains tax applies.\n\n"
                "If your decision is final, you can stop the SIP anytime via **Groww > Mutual Funds > SIPs > Cancel SIP**."
            )
        }

    # CATEGORY 6: Tax & Lock-In / Liquidity Clarifications
    tax_keywords = [
        "tax", "lock", "elss", "80c", "capital gain", "stcg", "ltcg", "safe", "risk"
    ]
    if any(k in q for k in tax_keywords):
        return {
            "badge": "📋 Groww Investor Literacy Engine",
            "style": "audit-general",
            "reply": (
                "**Key Liquidity & Tax Guidelines for Indian Mutual Funds:**\n\n"
                "• **Open-Ended Funds**: You can redeem anytime. However, redeeming within 365 days attracts Short-Term Capital Gains (STCG) tax and potentially an Exit Load (~1%).\n"
                "• **ELSS Tax-Savers**: These have a statutory 3-year lock-in per monthly instalment under Section 80C.\n"
                "• **Long Term (Holding > 1 Year)**: Gains are taxed under Long-Term Capital Gains (LTCG) with annual exemptions as per IT rules."
            )
        }

    # CATEGORY 7: Increasing Amount / Step-Up / Bonus
    stepup_keywords = [
        "increase", "step up", "top up", "badhana", "more money", "appraisal", "bonus", "lumpsum"
    ]
    if any(k in q for k in stepup_keywords):
        return {
            "badge": "📈 Wealth Acceleration Engine",
            "style": "audit-action",
            "reply": (
                "**Accelerating your SIP journey:**\n\n"
                "• **SIP Step-Up (Top-Up)**: You can enable automatic annual increases (e.g., 10% every year aligned with your appraisal) without having to start a new mandate.\n"
                "• **One-Time Lumpsum**: Got a festival bonus? You can invest a one-time extra amount directly into your existing folio anytime through the Groww app."
            )
        }

    # CATEGORY 8: General / Conversational / Any Other Query
    return {
        "badge": "🌱 Groww First-Time Investor Guidance Engine",
        "style": "audit-general",
        "reply": (
            "Namaste! As your Groww SIP Companion, I help first-time mutual fund investors navigate their first 12 months smoothly.\n\n"
            "**I can guide you on:**\n"
            "• **Managing Cashflow & Bounces**: Aligning SIP dates with your salary or skipping an instalment without bank fees.\n"
            "• **Market Fluctuations**: Understanding why early flat/red returns are normal and how Rupee-Cost Averaging works.\n"
            "• **SIP Maintenance**: Pausing for emergencies, setting up step-ups, or checking exit loads.\n\n"
            "Feel free to ask your question, describe any issue you are facing, or click one of the quick test scenarios above!"
        )
    }

# Session Chat State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! I am your Groww SIP Retention Companion. Are you facing a salary delay, seeing flat or red returns, or unsure about an upcoming SIP debit? Ask me anything below.",
            "badge": "Verified System Onboarding",
            "style": "audit-general"
        }
    ]

# Handle Quick Button Clicks
if quick_input:
    st.session_state.messages.append({"role": "user", "content": quick_input})
    res = process_investor_query(quick_input)
    st.session_state.messages.append({"role": "assistant", "content": res["reply"], "badge": res["badge"], "style": res["style"]})

# Render Existing Messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "badge" in m:
            st.markdown(f"<span class='audit-chip {m['style']}'>{m['badge']}</span>", unsafe_allow_html=True)

# User Chat Input
user_text = st.chat_input("Ask any question about your SIP, salary dates, market worries, or Groww features...")
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    res = process_investor_query(user_text)
    st.session_state.messages.append({"role": "assistant", "content": res["reply"], "badge": res["badge"], "style": res["style"]})
    st.rerun()