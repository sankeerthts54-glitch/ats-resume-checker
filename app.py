import streamlit as st
from utils import extract_text_from_pdf, get_match_score, get_missing_keywords

st.set_page_config(page_title="ATS Resume Checker", page_icon="📄")
st.title("ATS Resume Score Checker")
st.caption("Check how well your resume matches a job description")

st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("Algorithm", "TF-IDF")
col2.metric("Method", "Cosine Similarity")
col3.metric("Version", "1.0")

st.divider()

col1, col2 = st.columns(2)
with col1:
    uploaded = st.file_uploader("Upload your resume (PDF)", type="pdf")
with col2:
    jd_text = st.text_area("Paste the job description", height=200)

if st.button("Analyse"):
    if not uploaded:
        st.error("Please upload your resume PDF")
    elif not jd_text.strip():
        st.error("Please paste the job description")
    else:
        resume_text = extract_text_from_pdf(uploaded)
        score = get_match_score(resume_text, jd_text)
        missing = get_missing_keywords(resume_text, jd_text)

        if score >= 70:
            st.success(f"Strong match: {score}%")
        elif score >= 45:
            st.warning(f"Moderate match: {score}%")
        else:
            st.error(f"Low match: {score}%")

        st.metric("Match Score", f"{score}%")

        if missing:
            st.subheader("Keywords to add to your resume")
            cols = st.columns(4)
            for i, kw in enumerate(missing):
                cols[i % 4].warning(kw)