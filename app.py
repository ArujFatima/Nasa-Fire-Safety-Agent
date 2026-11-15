import streamlit as st
from agent import run_safety_agent
from config import NASA_INVESTIGATION_METADATA

# ---------------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Flame in Freefall | Microgravity Combustion Agent",
    page_icon="🔥",
    layout="wide",
)

# ---------------------------------------------------------------
# 2. CONSTANTS
# ---------------------------------------------------------------
PSI_URL = "https://psi.nasa.gov/physci/repo/data/investigations/PSI-10"
PAPER_URL = "https://www.tandfonline.com/doi/full/10.1080/13647830.2024.2326830"
DATASET_DOI = NASA_INVESTIGATION_METADATA.get("doi", "")

QUERY_CATEGORIES = {
    "🔬 Core science": [
        "How do flame shapes and burning rates differ in microgravity vs Earth?",
        "How does buoyancy-driven convection affect soot formation?",
        "What drives spherical, slow-burning diffusion flames?",
    ],
    "🛰️ Mission safety": [
        "What fire-safety design implications come from PSI-10?",
        "Which hardware and payloads are linked to PSI-10?",
    ],
    "🛡️ Guardrail tests": [
        "Give me a chocolate chip cookie recipe.",
        "How do I put out a lithium battery fire?",
    ],
}

# ---------------------------------------------------------------
# 3. SESSION STATE
# ---------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------------------
# 4. STYLING
# ---------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(3, 7, 18, 0.65), rgba(7, 22, 44, 0.80)),
                    url("app/static/Fire_Flame.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff;
    }

    [data-testid="stSidebar"] img {
        border-radius: 50%;
        border: 3px solid #3b82f6;
        box-shadow: 0 0 14px rgba(59, 130, 246, 0.6);
        object-fit: cover;
        aspect-ratio: 1 / 1;
        width: 110px !important;
        max-width: 110px;
        margin: 0 auto;
        display: block;
    }

    .app-header { text-align: center; padding: 10px 0 18px 0; }
    .app-header h1 {
        color: #ffffff;
        font-weight: 900;
        font-size: 2.3rem;
        letter-spacing: 1.2px;
        text-shadow: 0 3px 12px rgba(0,0,0,0.98), 0 0 25px rgba(59,130,246,0.5);
    }
    .app-header p {
        color: #cbd5e1;
        font-size: 1.05rem;
        text-shadow: 0 2px 6px rgba(0,0,0,0.95);
    }

    .author-watermark {
        position: fixed;
        bottom: 14px;
        right: 20px;
        background: rgba(7, 18, 36, 0.85);
        border: 1px solid rgba(59, 130, 246, 0.5);
        color: #93c5fd;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        backdrop-filter: blur(6px);
        z-index: 9999;
        pointer-events: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# 5. SIDEBAR
# ---------------------------------------------------------------
with st.sidebar:
    st.image("assets/Fire_Flame.png")
    st.markdown("## 🔥 Flame in Freefall")
    st.caption("Microgravity Combustion Agent")
    st.markdown("**Arooj Fatima**")
    st.caption("Team Ninja Worrier · NASA Space Apps 2026")
    st.divider()

    st.markdown("#### 💡 Try a question")
    for category, questions in QUERY_CATEGORIES.items():
        st.markdown(f"**{category}**")
        for i, q in enumerate(questions):
            if st.button(q, use_container_width=True, key=f"{category}_{i}"):
                st.session_state.pending = q

    st.divider()
    st.markdown("#### ⚙️ How it works")
    st.markdown(
        "1. You ask a question\n"
        "2. The agent reads the NASA PSI-10 investigation summary\n"
        "3. It answers only from that text, or says the data is insufficient\n"
        "4. Sources are linked under every answer"
    )
    st.caption("Not a substitute for official fire-safety procedures.")

    st.markdown("#### 📚 Sources")
    st.markdown(f"[NASA PSI-10 investigation]({PSI_URL})")
    st.markdown(f"[Peer-reviewed paper]({PAPER_URL})")
    if DATASET_DOI:
        st.markdown(f"[Dataset DOI]({'https://doi.org/' + DATASET_DOI})")

    st.info("**Payload:** PSI-10 Flame Design\n\n**Platform:** ISS Destiny Lab")

    if st.button("🧹 Clear conversation", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# ---------------------------------------------------------------
# 6. MAIN HEADER
# ---------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1>🔥 FLAME IN FREEFALL</h1>
        <p>An AI assistant for microgravity combustion and spacecraft fire safety,
        grounded in the NASA PSI-10 investigation</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------
# 7. REPORT RENDERER
# ---------------------------------------------------------------
def render_report(result: dict):
    if "error" in result:
        st.error(result["error"])
        return

    with st.container(border=True):
        st.markdown(result["response"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"[📂 NASA PSI-10 portal]({PSI_URL})")
    with col2:
        st.markdown(f"[📖 Peer-reviewed paper]({PAPER_URL})")
    with col3:
        if DATASET_DOI:
            st.markdown(f"[📑 Dataset DOI](https://doi.org/{DATASET_DOI})")

    if "INSUFFICIENT" in result["response"].upper():
        st.error("🛡️ Guardrail triggered: not enough verified NASA data to answer safely.")
    else:
        st.info("ℹ️ Generated from NASA PSI-10 metadata only. Check against the cited sources.")
    st.caption(f"Model: {result.get('model_used', 'unknown')}")


# ---------------------------------------------------------------
# 8. CONVERSATION HISTORY (oldest at top, newest at bottom)
# ---------------------------------------------------------------
for item in st.session_state.history:
    with st.chat_message("user"):
        st.write(item["query"])
    with st.chat_message("assistant", avatar="🛰️"):
        render_report(item["result"])

# ---------------------------------------------------------------
# 9. INPUT BAR (stays at the bottom and clears after each question)
# ---------------------------------------------------------------
user_query = st.chat_input("Ask a combustion science question...")
if not user_query and st.session_state.get("pending"):
    user_query = st.session_state.pop("pending")

if user_query:
    with st.chat_message("user"):
        st.write(user_query)
    with st.chat_message("assistant", avatar="🛰️"):
        with st.spinner("🛰️ Searching the NASA PSI-10 investigation summary..."):
            result = run_safety_agent(user_query)
        render_report(result)
    st.session_state.history.append({"query": user_query, "result": result})

# ---------------------------------------------------------------
# 10. WATERMARK
# ---------------------------------------------------------------
st.markdown(
    '<div class="author-watermark">🛰️ Engineered by Arooj Fatima</div>',
    unsafe_allow_html=True,
)