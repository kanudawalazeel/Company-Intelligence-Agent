# app/streamlit_app.py
#
# PURPOSE: This is the face of our project.
# It creates a web interface where users interact with our AI agent.
# Everything the user sees and clicks is defined here.

import sys
import os

# This line ensures Python can find our src/ folder
# when Streamlit runs the app from the app/ directory
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
))

import streamlit as st
from src.tools.search_tool import search_company
from src.agents.analyst import generate_report
from src.tools.pdf_export import export_to_pdf

# ─────────────────────────────────────────────
# PAGE CONFIGURATION
# This must be the FIRST Streamlit command called.
# It sets the browser tab title, icon, and layout.
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Company Intelligence Agent",
    page_icon="🏢",
    layout="wide",            # Use full browser width
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CUSTOM STYLING
# Streamlit allows injecting CSS with st.markdown.
# This makes our app look polished and professional.
# ─────────────────────────────────────────────
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0f1117;
    }

    /* Section card style */
    .report-card {
        background-color: #1e2130;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        border-left: 4px solid #4f8ef7;
    }

    /* Section heading */
    .section-title {
        color: #4f8ef7;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }

    /* Section content */
    .section-content {
        color: #d1d5db;
        font-size: 15px;
        line-height: 1.8;
    }

    /* Main title */
    .main-title {
        text-align: center;
        color: #ffffff;
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    /* Subtitle */
    .sub-title {
        text-align: center;
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 32px;
    }

    /* Hide Streamlit default footer */
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HEADER SECTION
# This is the title displayed at the top of the page.
# ─────────────────────────────────────────────
st.markdown(
    '<div class="main-title">🏢 Company Intelligence Agent</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">Enter any company name to generate an AI-powered intelligence report</div>',
    unsafe_allow_html=True
)

st.divider()

# ─────────────────────────────────────────────
# INPUT SECTION
# Two columns: left has the text input and button,
# right shows example companies for reference.
# ─────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    # Text input box where user types the company name
    company_name = st.text_input(
        label="Company Name",
        placeholder="e.g. Adani Realty, Sobha Limited, Prestige Group...",
        label_visibility="collapsed"
    )

    # The button that starts the research process
    generate_btn = st.button(
        "🔍 Generate Intelligence Report",
        type="primary",
        use_container_width=True
    )

with col2:
    # Show example companies as clickable hints
    st.markdown("**💡 Try these examples:**")
    st.markdown("Adani Realty • Sobha Limited")
    st.markdown("Prestige Group • Brigade Group")
    st.markdown("Puravankara • DLF Limited")


# ─────────────────────────────────────────────
# MAIN LOGIC
# This block runs ONLY when the button is clicked
# AND the company name field is not empty.
# ─────────────────────────────────────────────
if generate_btn:

    # Validation: check if user actually typed something
    if not company_name.strip():
        st.warning("⚠️ Please enter a company name before generating.")
        st.stop()  # Stop execution here, don't run anything below

    # ── STEP 1: WEB SEARCH ──────────────────────
    # Show a status message while searching
    with st.status(
        f"🔍 Researching **{company_name}**...",
        expanded=True
    ) as status:

        st.write("📡 Searching the web for company information...")

        # Call our search_tool.py function
        research_data = search_company(company_name)

        st.write("✅ Web search complete.")
        st.write("🧠 Sending data to AI for analysis...")

        # ── STEP 2: AI ANALYSIS ─────────────────
        # Call our analyst.py function
        report = generate_report(company_name, research_data)

        st.write("✅ Report generated successfully!")

        # Update the status box to show completion
        status.update(
            label="✅ Intelligence Report Ready",
            state="complete",
            expanded=False
        )

    # ── STEP 3: ERROR CHECK ─────────────────────
    # If the report's overview starts with "Error:", something went wrong
    if report.get("overview", "").startswith("Error:"):
        st.error(f"❌ Report generation failed: {report['overview']}")
        st.info("💡 Try again in a few seconds, or check your API keys in .env")
        st.stop()

    # ── STEP 4: DISPLAY REPORT ──────────────────
    st.divider()
    st.markdown(f"## 📊 Intelligence Report: {company_name}")
    st.caption("Generated using real-time web research + AI analysis")

    # Section 1: Company Overview
    st.markdown(f"""
    <div class="report-card">
        <div class="section-title">📌 1. Company Overview</div>
        <div class="section-content">{report.get('overview', 'Not available')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Section 2: Key Business Information
    st.markdown(f"""
    <div class="report-card">
        <div class="section-title">💼 2. Key Business Information</div>
        <div class="section-content">{report.get('business_info', 'Not available')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Section 3: Business Challenges
    st.markdown(f"""
    <div class="report-card">
        <div class="section-title">⚠️ 3. Potential Business Challenges</div>
        <div class="section-content">{report.get('challenges', 'Not available')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Section 4: AI Opportunities
    st.markdown(f"""
    <div class="report-card">
        <div class="section-title">🤖 4. AI Opportunities</div>
        <div class="section-content">{report.get('ai_opportunities', 'Not available')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Section 5: Personalized CEO Pitch
    st.markdown(f"""
    <div class="report-card">
        <div class="section-title">🎯 5. Personalized CEO Pitch</div>
        <div class="section-content">{report.get('pitch', 'Not available')}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── STEP 5: SAVE REPORT ─────────────────────
    # Save the report as a text file in outputs/
    # This shows the recruiter you think about data persistence
    st.divider()

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Create a clean filename from company name
    safe_name = company_name.strip().replace(" ", "_").lower()
    output_path = os.path.join(output_dir, f"{safe_name}_report.txt")

    # Build the text content to save
    report_text = f"""
COMPANY INTELLIGENCE REPORT
============================
Company: {company_name}
Generated by: AI Research Agent

1. OVERVIEW
{report.get('overview', '')}

2. KEY BUSINESS INFORMATION
{report.get('business_info', '')}

3. BUSINESS CHALLENGES
{report.get('challenges', '')}

4. AI OPPORTUNITIES
{report.get('ai_opportunities', '')}

5. CEO PITCH
{report.get('pitch', '')}
""".strip()

    # Write the file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    # ── STEP 5: DOWNLOAD OPTIONS ────────────────
    st.divider()
    st.markdown("### 📥 Download Report")

    dl_col1, dl_col2 = st.columns(2)

    # ── PDF Download ──
    with dl_col1:
        with st.spinner("Preparing PDF..."):
            pdf_path = export_to_pdf(report, company_name)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download PDF Report",
                data=f,
                file_name=f"{safe_name}_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )

    # ── TXT Download ──
    with dl_col2:
        st.download_button(
            label="📝 Download TXT Report",
            data=report_text,
            file_name=f"{safe_name}_report.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.success(f"✅ Reports saved to outputs/ folder")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()
st.markdown(
    '<div style="text-align:center; color:#4b5563; font-size:13px;">'
    'Built with LangChain • Groq LLaMA 3.3 • Tavily Search • Streamlit'
    '</div>',
    unsafe_allow_html=True
)