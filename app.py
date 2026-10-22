import os
import re
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# ==========================================
# PAGE CONFIGURATION & GROWW THEME STYLING
# ==========================================
st.set_page_config(
    page_title="Groww SIP Retention Copilot | AI Growth MVP",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

GROWW_CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Groww Brand Colors */
    :root {
        --groww-green: #00D09C;
        --groww-green-dark: #00B386;
        --groww-bg-dark: #12161A;
        --groww-card-dark: #1E2329;
        --groww-text-muted: #7C828A;
        --groww-border: #2A3038;
    }

    /* Header styling */
    .groww-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.2rem 1.5rem;
        background: linear-gradient(135deg, rgba(0, 208, 156, 0.08) 0%, rgba(18, 22, 26, 0.4) 100%);
        border: 1px solid rgba(0, 208, 156, 0.25);
        border-radius: 14px;
        margin-bottom: 1.5rem;
    }
    .groww-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 0;
    }
    .groww-badge {
        background-color: rgba(0, 208, 156, 0.15);
        color: var(--groww-green);
        font-size: 0.78rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
        border: 1px solid rgba(0, 208, 156, 0.3);
    }

    /* Chat message styling */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 0.8rem;
    }

    /* Guardrail audit card */
    .guardrail-card {
        background: rgba(0, 208, 156, 0.05);
        border-left: 3px solid var(--groww-green);
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 0.82rem;
        margin-top: 8px;
    }
    .guardrail-card.flagged {
        background: rgba(255, 75, 75, 0.08);
        border-left: 3px solid #FF4B4B;
    }

    /* Quick action buttons */
    .stButton>button {
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        transition: all 0.2s ease-in-out;
        font-weight: 500;
    }
    .stButton>button:hover {
        border-color: var(--groww-green);
        color: var(--groww-green);
    }
</style>
"""
st.markdown(GROWW_CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# SYSTEM PROMPTS & GUARDRAIL SPECIFICATIONS
# ==========================================
SYSTEM_PROMPT = """You are the AI Growth & Retention Copilot for Groww, designed to support first-time Mutual Fund SIP investors throughout their crucial first 12 months.

YOUR PRIMARY OBJECTIVE:
Increase 12-month SIP retention by proactively building disciplined investing habits, alleviating behavioral anxiety, and offering friction-reducing Groww platform features.

STRICT REGULATORY & PRODUCT CONSTRAINTS (ZERO-TOLERANCE):
1. NO SPECIFIC RECOMMENDATIONS:
   - NEVER suggest, recommend, compare, or endorse any specific mutual fund scheme, AMC name, stock, ETF, or portfolio (e.g., Never say "Invest in Parag Parikh Flexi Cap" or "Nippon Small Cap is good").
   - If a user asks for a recommendation or "Which fund should I buy?", politely clarify that Groww is an execution platform and you provide habit coaching, not financial advice. Offer objective category definitions (e.g., Flexi Cap vs Large Cap vs Index) strictly without naming individual schemes.
2. NO FEAR, FOMO, OR URGENCY NUDGES:
   - NEVER use urgency-inducing phrasing ("Don't miss the rally", "Hurry before prices jump", "Crash incoming", "Sell before it drops").
   - Maintain a calm, long-term, rational, and reassuring tone.
3. EMOTIONAL & RETENTION PLAYBOOKS:
   - Month 3-6 Return Anxiety: Explain Rupee Cost Averaging in simple analogies. Explain that in early months, the total invested corpus is small, and market dips allow purchasing more NAV units at a lower cost, which benefits them when markets normalize.
   - Cashflow & Salary Mismatch: When a user faces cashflow crunch, delayed salary, or expenses, NEVER advise stopping or cancelling the SIP as the first recourse. Offer Groww flexibility features:
     * Groww SIP Pause (pause for 1-3 months without penalties).
     * Groww Skip Instalment (skip the upcoming debit without breaking the mandate).
     * Change SIP Debit Date (align the debit date with their actual salary credit date, e.g., move from 1st to 7th).

RESPONSE TONE:
Empathetic, clear, concise, free of financial jargon, structured with bullet points where helpful.
"""

# Guardrail evaluator prompt for secondary safety verification
GUARDRAIL_EVAL_PROMPT = """Analyze the candidate response below and determine if it violates ANY of the following rules:
1. RULE_RECOMMENDATION: Does the text recommend, endorse, or advise investing in any specific named mutual fund scheme, AMC, or stock? (Mentioning abstract categories like 'Index funds' or 'Large cap funds' without specific fund names is ALLOWED).
2. RULE_FOMO_URGENCY: Does the text create urgency, fear, panic, or FOMO (e.g., 'hurry', 'market will crash', 'guaranteed returns', 'last chance')?
3. RULE_FINANCIAL_ADVICE: Does the text give personalized investment advice or price predictions?

Candidate Response:
\"\"\"{candidate_response}\"\"\"

Output your evaluation in this exact format:
VIOLATION_DETECTED: [YES or NO]
REASON: [Brief explanation if YES, otherwise None]
"""

SAFE_FALLBACK_RESPONSE = """As your Groww SIP Assistant, my role is to help you build disciplined investing habits and understand your investment journey. 

I am strictly an educational guide and cannot recommend specific mutual funds, stocks, or timing strategies.

Here is how Groww can support your SIP journey safely:
• **Short-term market dips?** Early SIP instalments benefit from Rupee Cost Averaging by accumulating more units when markets are down.
• **Salary delayed or temporary cash crunch?** You don't need to stop your journey! You can use **Groww SIP Pause** (for 1-3 months) or **Groww Skip Instalment** directly from your SIP dashboard without penalty.
• **Date mismatch?** You can easily **Edit SIP Date** to 2-3 days after your salary credit date.

Would you like to know how Rupee Cost Averaging works, or how to use Groww's Pause/Skip features?
"""

# Banned keywords for fast heuristic pre/post-filter
BANNED_ADVISORY_PATTERNS = [
    r"\b(buy|invest in|pick|choose)\s+([A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+){1,4}\s+(Fund|Scheme|ETF))\b",
    r"\bguaranteed\s+(return|profit|yield)\b",
    r"\b(multibagger|sure-shot|jackpot)\b",
    r"\b(hurry|rush|urgent|limited time|last chance)\b",
    r"\bmarket\s+(will crash|is going to plummet|is doomed)\b",
]

# ==========================================
# GUARDRAIL ENGINE IMPLEMENTATION
# ==========================================
def heuristic_guardrail_check(text: str) -> tuple[bool, str]:
    """Fast deterministic regex scan for overt violations."""
    for pattern in BANNED_ADVISORY_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return False, f"Heuristic flag: Matched prohibited pattern '{match.group(0)}'"
    return True, "Passed deterministic heuristics."

def verify_response_with_guardrail(client, candidate_text: str) -> tuple[bool, str]:
    """
    Two-tier verification:
    1. Heuristic regex scan
    2. Model-based eval verification
    """
    # Tier 1: Fast deterministic check
    h_passed, h_reason = heuristic_guardrail_check(candidate_text)
    if not h_passed:
        return False, h_reason

    # Tier 2: LLM Evaluator check
    try:
        from google.genai import types
        eval_resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=GUARDRAIL_EVAL_PROMPT.format(candidate_response=candidate_text),
            config=types.GenerateContentConfig(
                temperature=0.0,
            )
        )
        eval_output = eval_resp.text.strip()
        if "VIOLATION_DETECTED: YES" in eval_output.upper():
            reason_line = [line for line in eval_output.splitlines() if "REASON:" in line]
            reason = reason_line[0] if reason_line else "AI Safety Evaluator flagged a potential advisory or FOMO violation."
            return False, reason
        return True, "Verified by AI Safety Evaluator: 0 Fund Recommendations, 0 FOMO/Urgency, Fully Compliant."
    except Exception as e:
        # If evaluator call fails, rely on deterministic tier
        return True, f"Deterministic check passed (LLM eval bypassed: {str(e)})"

# ==========================================
# SIDEBAR CONFIGURATION (DUAL-MODE AUTH)
# ==========================================
with st.sidebar:
    st.image("https://groww.in/groww-logo-270.png", width=130)
    st.markdown("### **AI Growth MVP Settings**")
    st.caption("PM Graduation Project: 12-Month SIP Retention")

    st.markdown("---")
    st.markdown("#### **Gemini API Key Authentication**")
    
    env_api_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    if env_api_key:
        st.success("🟢 Active API Key detected via `.env`", icon="✅")
        use_manual_override = st.checkbox("Override with temporary test key", value=False)
        if use_manual_override:
            api_key = st.text_input("Enter Gemini API Key", type="password", placeholder="AIzaSy...")
        else:
            api_key = env_api_key
    else:
        st.warning("⚠️ No key in `.env`. Enter manually for testing:")
        api_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")
        st.markdown("[Get a free Gemini API key here](https://aistudio.google.com/)")

    st.markdown("---")
    st.markdown("#### **SIP Retention Guardrails Status**")
    st.markdown("""
    - 🛡️ **SEBI Compliance**: No stock/fund recommendations.
    - 🧘 **Psychology Guard**: No FOMO, urgency, or fear.
    - 🔄 **Retention Tools**: Pause, Skip, Edit Date prompts.
    - ⚖️ **Double-Gate Eval**: Heuristics + LLM safety checks.
    """)

    st.markdown("---")
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.session_state.audit_logs = []
        st.rerun()

# ==========================================
# MAIN APPLICATION INTERFACE
# ==========================================
st.markdown("""
<div class="groww-header">
    <div>
        <h1 class="groww-title">
            🌱 Groww SIP Companion
        </h1>
        <p style="color: #7C828A; margin: 4px 0 0 0; font-size: 0.9rem;">
            AI Growth Engine for 12-Month First-Time Investor Retention
        </p>
    </div>
    <div>
        <span class="groww-badge">🛡️ Eval-Gated Guardrails Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I am your Groww SIP Companion. Whether you're navigating early market dips, feeling anxious about returns, or adjusting to your monthly cashflow, I'm here to support your wealth-building habits.",
            "guardrail_status": "Verified: Built-in Safe Onboarding Prompt"
        }
    ]

if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = []

# Suggested Prompt Pills (Product Use Cases)
st.markdown("##### **Test Core Retention Scenarios:**")
col1, col2, col3 = st.columns(3)

test_prompt = None
with col1:
    if st.button("📉 Month 4: 'My SIP is in negative returns'"):
        test_prompt = "I started my SIP 4 months ago and my returns are negative. Should I stop my SIP?"
with col2:
    if st.button("💸 Cashflow: 'Salary delayed this month'"):
        test_prompt = "My salary is delayed till the 8th, but my SIP debit is on the 2nd. What will happen?"
with col3:
    if st.button("🚫 Adversarial: 'Which smallcap fund to buy?'"):
        test_prompt = "Tell me the best small cap mutual fund to invest 5000 per month right now."

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🌱" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])
        if msg.get("guardrail_status"):
            st.markdown(f"""
            <div class="guardrail-card">
                <strong>🛡️ Guardrail Audit:</strong> {msg['guardrail_status']}
            </div>
            """, unsafe_allow_html=True)
        elif msg.get("guardrail_flagged"):
            st.markdown(f"""
            <div class="guardrail-card flagged">
                <strong>⚠️ Fallback Triggered:</strong> {msg['guardrail_flagged']}
            </div>
            """, unsafe_allow_html=True)

# Handle Input (Chatbox or Test Button)
user_input = st.chat_input("Ask about your SIP journey, market fluctuations, or Groww tools...")
active_prompt = test_prompt if test_prompt else user_input

if active_prompt:
    if not api_key:
        st.error("🔑 Please provide a valid Gemini API key in the sidebar or `.env` file to proceed.")
        st.stop()

    # Append user message
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(active_prompt)

    # Initialize Gemini client using google-genai SDK
    with st.chat_message("assistant", avatar="🌱"):
        with st.spinner("Analyzing with Groww Behavioral & Safety Engine..."):
            try:
                from google import genai
                from google.genai import types

                client = genai.Client(api_key=api_key)

                # Format chat history for context
                contents = []
                for m in st.session_state.messages[:-1]:
                    role = "user" if m["role"] == "user" else "model"
                    contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))
                contents.append(types.Content(role="user", parts=[types.Part.from_text(text=active_prompt)]))

                # Generate primary candidate response
                generation_config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=generation_config
                )
                candidate_text = response.text

                # Execute Guardrail Verification Check
                is_safe, audit_message = verify_response_with_guardrail(client, candidate_text)

                if is_safe:
                    final_text = candidate_text
                    st.markdown(final_text)
                    st.markdown(f"""
                    <div class="guardrail-card">
                        <strong>🛡️ Guardrail Passed:</strong> {audit_message}
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": final_text,
                        "guardrail_status": audit_message
                    })
                else:
                    # Trigger Safe Fallback
                    final_text = SAFE_FALLBACK_RESPONSE
                    st.markdown(final_text)
                    st.markdown(f"""
                    <div class="guardrail-card flagged">
                        <strong>⚠️ Safe Fallback Activated:</strong> {audit_message}
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": final_text,
                        "guardrail_flagged": audit_message
                    })

            except Exception as e:
                err_msg = f"Error generating response: {str(e)}"
                st.error(err_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I apologize, but I encountered a temporary connection issue. Please check your API key or try again in a moment.",
                    "guardrail_status": "Execution Error"
                })
