import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="George Adjaidoo",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stMetricLabel"] {
    font-size:18px;
}

[data-testid="stMetricValue"] {
    font-size:26px;
}

h1 {
    font-size:45px !important;
}

h2 {
    font-size:28px !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.title("🚀 George Adjaidoo")

st.subheader(
    "Senior Data Engineer | Microsoft Fabric | Databricks | Azure | SQL"
)

st.markdown("""
📧 gadjaidoo@gmail.com  
📞 301-452-2385  
🔗 LinkedIn: linkedin.com/in/george-a-7861428b
""")

st.divider()

# =====================================================
# METRICS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Experience", "16+ Years")
col2.metric("Current Role", "Sr Software Engineer")
col3.metric("Education", "MS IT 2026")
col4.metric("Focus", "Data Engineering")

st.divider()

# =====================================================
# SUMMARY
# =====================================================

st.header("Professional Summary")

st.write("""
Senior Data Engineer with 16+ years of experience designing,
developing, and optimizing enterprise-scale data platforms,
cloud-native ETL frameworks, and analytics solutions.

Expertise includes Microsoft Fabric, Azure Data Factory,
Databricks, Snowflake, SQL Server, Terraform, and Python.

Proven success delivering scalable data architectures,
automation solutions, cloud migrations, and enterprise
analytics platforms across healthcare, financial services,
consulting, and government sectors.
""")

# =====================================================
# EXPERIENCE
# =====================================================

st.header("Professional Experience")

with st.expander(
    "Johns Hopkins - Senior Software Engineer (2021 - Present)",
    expanded=True
):
    st.write("""
    • Microsoft Fabric Architecture

    • Databricks Development

    • Azure Data Factory Pipelines

    • Terraform Automation

    • Python Development

    • Real-Time Analytics Solutions

    • Data Platform Modernization
    """)

with st.expander("Unisys - Data Integration Engineer"):
    st.write("""
    • ETL Development

    • Power BI Dashboards

    • Azure Data Factory Automation
    """)

with st.expander("Ernst & Young - Manager, Data Modeler"):
    st.write("""
    • Global Tax Platform

    • Azure DevOps

    • SAFe PI Planning
    """)

with st.expander("United Health Group - SQL / ETL Developer"):
    st.write("""
    • SSIS Development

    • SQL Server Automation

    • Power BI Reporting
    """)

with st.expander("Government Contracts (SEC / OCC / DOE)"):
    st.write("""
    • Data Modeling

    • ETL Development

    • Tableau

    • Power BI

    • SAS
    """)

# =====================================================
# SKILLS
# =====================================================

st.header("Technical Skills")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Cloud & Data Platforms")

    st.write("""
    • Microsoft Fabric  
    • Azure  
    • Databricks  
    • Snowflake  
    • Hadoop
    """)

    st.subheader("Databases")

    st.write("""
    • SQL Server  
    • T-SQL  
    • SAS
    """)

with col2:

    st.subheader("Programming")

    st.write("""
    • Python  
    • PowerShell  
    • Bash  
    • C#  
    • Java
    """)

    st.subheader("Analytics")

    st.write("""
    • Power BI  
    • Tableau  
    • SSRS
    """)

# =====================================================
# EDUCATION
# =====================================================

st.header("Education")

st.markdown("""
### Master of Science – Information Technology
University of Denver  
Expected Graduation: Fall 2026

### B.Sc. Accounting
University of Maryland

### Professional Certificate in Data Engineering
Purdue University
""")

# =====================================================
# CERTIFICATIONS
# =====================================================

st.header("Certifications")

st.write("""
• Microsoft Certified Professional

• Databricks Certified

• Querying with Transact-SQL
""")

# =====================================================
# PROJECTS
# =====================================================

st.header("Featured Projects")

st.subheader("💰 Loan Payoff Analysis Application")

st.write("""
Interactive Streamlit application featuring:

• Target payoff analysis

• Payment optimization

• Interactive sliders

• Balance forecasting

• Interest savings analysis

• CSV export
""")

st.subheader("📊 Microsoft Fabric Data Engineering")

st.write("""
Enterprise data engineering solutions utilizing:

• Microsoft Fabric

• Azure Data Factory

• Databricks

• Lakehouse Architecture

• Metadata Driven ETL
""")

# =====================================================
# RESUME DOWNLOAD
# =====================================================

st.divider()

st.header("Resume Download")

resume_file = Path(__file__).parent / "George_Adjaidoo_Resume.pdf"

with open(resume_file, "rb") as pdf_file:
    st.download_button(
        "📄 Download PDF Resume",
        pdf_file,
        file_name="George_Adjaidoo_Resume.pdf",
        mime="application/pdf"
    )

st.success("Thank you for visiting my profile.")