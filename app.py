import os
import streamlit as st

st.set_page_config(page_title="Groww SIP Retention Companion", page_icon="🌱", layout="wide")

st.title("🌱 Groww 12-Month SIP Retention Companion")
st.caption("AI-Native Growth MVP for First-Time Indian Mutual Fund Investors")

# Quick Test Buttons directly at the top
st.markdown("### ⚡ Quick Retention Test Scenarios")
c1, c2, c3 = st.columns(3)

test_query = None
if c1.button("💸 Salary delayed by 10 days"):
    test_query = "Is mahine salary 10 din late hai, meri SIP bounce na ho iske liye Groww mein kya karu?"
if c2.button("📉 Month 4: Portfolio in red"):
    test_query = "Portfolio negative show ho raha hai, kya mujhe SIP cancel kar deni chahiye?"
if c3.button("❓ Which is best fund?"):
    test_query = "Mujhe batao sabse best small cap fund kaunsa hai SIP ke liye?"

def get_retention_reply(user_query: str) -> dict:
    q = user_query.lower()
    if any(k in q for k in ["best fund", "which fund", "recommend", "small cap", "kaha lagau", "kisme"]):
        return {
            "source": "🛡️ SEBI Compliance Guardrail",
            "reply": (
                "Main kisi specific mutual fund ya stock ki recommendation nahi de sakta, "
                "kyunki Groww unbiased investing ko promote karta hai.\n\n"
                "**Smart Approach:** Apne horizon aur risk profile ke according invest karein aur "
                "existing SIP ko continue rakhein taaki Rupee-Cost Averaging ka advantage mile."
            )
        }
    if any(k in q for k in ["salary", "late", "paise nahi", "bounce", "delay", "tangi"]):
        return {
            "source": "⚡ Groww Retention Action Engine",
            "reply": (
                "Salary delay ki wajah se SIP cancel karne ki bilkul zaroorat nahi hai! Groww par ye options use karein:\n\n"
                "1. **Skip Instalment:** Is mahine ki instalment skip karein, mandate intact rahega aur koi bank bounce charge nahi lagega.\n"
                "2. **Edit SIP Date:** SIP date ko salary credit date ke 2-3 din baad (e.g. 7th ya 10th) set kar lein.\n"
                "3. **Pause SIP:** 1-3 months ke liye temporary pause karein."
            )
        }
    return {
        "source": "🧠 Panic De-escalation Engine",
        "reply": (
            "Pehle 3-6 months mein returns flat ya negative dikhna normal hai. "
            "Down market mein aapki SIP **zyada units** acquire karti hai (Rupee-Cost Averaging). "
            "Jab market bounce karega, toh yahi units strong wealth create karengi."
        )
    }

# Chat session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! Main aapka Groww SIP Companion hoon. Salary mismatch ya portfolio doubts ke liye upar diye buttons dabayein ya yahan type karein.", "source": "System"}
    ]

# If quick button clicked
if test_query:
    st.session_state.messages.append({"role": "user", "content": test_query, "source": "User"})
    ans = get_retention_reply(test_query)
    st.session_state.messages.append({"role": "assistant", "content": ans["reply"], "source": ans["source"]})

# Show chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "source" in m:
            st.caption(f"Audit: {m['source']}")

# Input bar
user_text = st.chat_input("Type your question here...")
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text, "source": "User"})
    ans = get_retention_reply(user_text)
    st.session_state.messages.append({"role": "assistant", "content": ans["reply"], "source": ans["source"]})
    st.rerun()