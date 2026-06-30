import streamlit as st
from pathlib import Path
st.set_page_config(
    page_title="George Adjaidoo",
    page_icon="🚀",
    layout="wide"
)

# ==================================================
# Styling
# ==================================================

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

# ==================================================
# Sidebar
# ==================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "About",
        "Experience",
        "Projects",
        "Skills",
        "Education",
        "Resume"
    ]
)

# ==================================================
# HOME
# ==================================================

if page == "Home":

    st.title("🚀 George Adjaidoo")

    st.subheader(
        "Senior Data Engineer | Microsoft Fabric | Databricks | Azure"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Experience", "16+ Years")
    col2.metric("Certifications", "3+")
    col3.metric("Degree", "MS IT")
    col4.metric("Focus", "Data Engineering")

    st.markdown("---")

    st.write("""
    Senior Data Engineer with 16+ years of experience designing,
    developing, and optimizing enterprise-scale data platforms,
    cloud-native ETL frameworks, and analytics solutions.

    Expertise includes Microsoft Fabric, Azure Data Factory,
    Databricks, Snowflake, SQL Server, Terraform, and Python.
    """)

# ==================================================
# ABOUT
# ==================================================

elif page == "About":

    st.title("About Me")

    st.write("""
    Senior Data Engineer with extensive experience building
    enterprise data solutions across healthcare, financial
    services, consulting, and government sectors.

    Passionate about:

    • Microsoft Fabric

    • Data Engineering

    • Cloud Architecture

    • Automation

    • Analytics

    • Streamlit Applications
    """)

# ==================================================
# EXPERIENCE
# ==================================================

elif page == "Experience":

    st.title("Professional Experience")

    with st.expander("Johns Hopkins - Senior Software Engineer (2021-Present)", expanded=True):
        st.write("""
        • Designed ETL architecture using Databricks,
          Azure Data Factory, and Microsoft Fabric

        • Automated cloud migrations using
          Terraform, PowerShell, and Python

        • Built real-time analytics and reporting
          solutions

        • Engineered scalable ETL frameworks
        """)

    with st.expander("Unisys - Data Integration Engineer"):
        st.write("""
        • Built ETL integrations

        • Developed Power BI dashboards

        • Automated workflows with Azure Data Factory
        """)

    with st.expander("Ernst & Young - Manager, Data Modeler"):
        st.write("""
        • Developed Global Tax Platform data models

        • Managed Azure DevOps

        • Participated in SAFe PI Planning
        """)

    with st.expander("United Health Group - SQL/ETL Developer"):
        st.write("""
        • SSIS Development

        • SQL Server Automation

        • Power BI Reporting
        """)

# ==================================================
# PROJECTS
# ==================================================

elif page == "Projects":

    st.title("Projects")

    st.subheader("💰 Loan Payoff Analysis App")

    st.write("""
    Streamlit application featuring:

    • Target payoff analysis

    • Payment optimization

    • Interactive sliders

    • Scenario modeling

    • Loan progress tracking

    • CSV export
    """)

    st.subheader("📊 Microsoft Fabric Data Platform")

    st.write("""
    Enterprise-scale data engineering solutions utilizing:

    • Microsoft Fabric

    • Databricks

    • Azure Data Factory

    • Lakehouse Architecture

    • Metadata Driven ETL
    """)

# ==================================================
# SKILLS
# ==================================================

elif page == "Skills":

    st.title("Skills")

    st.subheader("Cloud & Data Platforms")

    st.write(
        "Microsoft Fabric • Azure • Databricks • Snowflake"
    )

    st.subheader("Databases")

    st.write(
        "SQL Server • T-SQL • SAS"
    )

    st.subheader("Programming")

    st.write(
        "Python • PowerShell • Bash • C# • Java"
    )

    st.subheader("Analytics")

    st.write(
        "Power BI • Tableau • SSRS"
    )

# ==================================================
# EDUCATION
# ==================================================

elif page == "Education":

    st.title("Education")

    st.subheader(
        "Master of Science - Information Technology"
    )

    st.write(
        "University of Denver (Expected Fall 2026)"
    )

    st.subheader(
        "B.Sc. Accounting"
    )

    st.write(
        "University of Maryland"
    )

    st.subheader(
        "Professional Certificate in Data Engineering"
    )

    st.write(
        "Purdue University"
    )

# ==================================================
# RESUME
# ==================================================

# elif page == "Resume":

#     st.title("Resume")

#     st.info(
#         "Upload your PDF resume to the repository and enable download here."
#     )

#     st.download_button(
#         label="Download Resume",
#         data=b"Upload your PDF resume first",
#         file_name="George_Adjaidoo_Resume.pdf",
#         mime="application/pdf"
#     )
# elif page == "Resume":

#     st.title("Resume")

#     with open("George_Adjaidoo_Resume.pdf", "rb") as pdf_file:
#         st.download_button(
#             label="📄 Download Resume",
#             data=pdf_file,
#             file_name="George_Adjaidoo_Resume.pdf",
#             mime="application/pdf"
#         )


elif page == "Resume":

    st.title("Resume")

    resume_file = Path("George_Adjaidoo_Resume.pdf")

    if resume_file.exists():

        with open(resume_file, "rb") as pdf_file:
            st.download_button(
                label="📄 Download Resume",
                data=pdf_file,
                file_name="George_Adjaidoo_Resume.pdf",
                mime="application/pdf"
            )

    else:
        st.warning(
            "Resume PDF not found. Upload George_Adjaidoo_Resume.pdf to the repository."
        )