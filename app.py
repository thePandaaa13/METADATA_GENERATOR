import streamlit as st
import pandas as pd
from pathlib import Path

from main import run_pipeline
from src.export.excel_export import export_to_excel
from src.config import SAMPLE_ASSETS_DIR

# ---------------- Page setup ----------------
st.set_page_config(
    page_title="Content Metadata Builder",
    page_icon="💊",
    layout="wide",
)

# ---------------- Custom styling ----------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0;
    }
    .sub-header {
        color: #6b7280;
        font-size: 1rem;
        margin-top: 0;
    }
    div[data-testid="stMetric"] {
        background-color: #f8f9fb;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 15px;
    }
    .status-pass {
        background-color: #d1fae5;
        color: #065f46;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .status-review {
        background-color: #fef3c7;
        color: #92400e;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown('<p class="main-header">💊 Content Metadata Builder Agent</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Automated metadata generation, compliance checks & performance enrichment for pharma marketing assets</p>', unsafe_allow_html=True)
st.divider()

# ---------------- Session state (so results persist across reruns) ----------------
if "results" not in st.session_state:
    st.session_state.results = None
if "excel_path" not in st.session_state:
    st.session_state.excel_path = None

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("📁 Upload Assets")
    uploaded_files = st.file_uploader(
    "Add new content files",
    type=["txt", "pdf", "docx", "pptx"],   # ← ye add karein
    accept_multiple_files=True,
    )

    if uploaded_files:
        for file in uploaded_files:
            save_path = SAMPLE_ASSETS_DIR / file.name
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
        st.success(f"{len(uploaded_files)} file(s) added to processing queue.")

    st.divider()
    existing_count = len(list(SAMPLE_ASSETS_DIR.glob("*.txt")))
    st.caption(f"📦 {existing_count} asset(s) ready in queue")

    st.divider()
    run_clicked = st.button("🚀 Generate Metadata Catalogue", type="primary", use_container_width=True)

# ---------------- Run pipeline ----------------
if run_clicked:
    with st.spinner("Processing assets — reading content, calling LLM, checking compliance..."):
        results = run_pipeline()
        excel_path = export_to_excel(results)
        st.session_state.results = results
        st.session_state.excel_path = excel_path
    st.success("Catalogue generated successfully!")

# ---------------- Results display ----------------
if st.session_state.results:
    results = st.session_state.results
    df = pd.DataFrame([r.model_dump() for r in results])

    # ---- Summary metrics ----
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Assets", len(df))
    col2.metric("Avg Confidence", f"{df['confidence_score'].mean():.0%}")
    pass_count = (df["compliance_status"] == "pass").sum()
    col3.metric("Compliance Pass Rate", f"{pass_count}/{len(df)}")
    col4.metric("Avg Engagement Score", f"{df['avg_engagement_score'].mean():.2f}")

    st.divider()

    # ---- Download button ----
    with open(st.session_state.excel_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Excel Catalogue",
            data=f,
            file_name="content_metadata_catalogue.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
        )

    st.divider()

    # ---- Per-asset cards ----
    st.subheader("📋 Generated Metadata")

    for r in results:
        with st.expander(f"**{r.title}**  —  {r.product} ({r.country})"):
            left, right = st.columns([2, 1])

            with left:
                st.write("**Summary:**", r.summary)
                st.write("**Keywords:**", ", ".join(r.keywords))
                st.write("**Therapeutic Area:**", r.therapeutic_area)
                st.write("**Approved Indication:**", r.approved_indication)

            with right:
                status_class = "status-pass" if r.compliance_status == "pass" else "status-review"
                status_label = "✅ Pass" if r.compliance_status == "pass" else "⚠️ Needs Review"
                st.markdown(f'<span class="{status_class}">{status_label}</span>', unsafe_allow_html=True)
                st.write("")
                st.write("**MLR Status:**", r.mlr_status)
                st.write("**Confidence:**", f"{r.confidence_score:.0%}")
                st.write("**Engagement Score:**", r.avg_engagement_score)
                st.write("**Activated:**", f"{r.times_activated}x")

            if r.compliance_notes:
                st.warning(" | ".join(r.compliance_notes))

    st.divider()

    # ---- Full table view ----
    st.subheader("📊 Full Catalogue Table")
    st.dataframe(df, use_container_width=True, height=400)

else:
    st.info("👈 Upload files (optional) and click **Generate Metadata Catalogue** to get started.")