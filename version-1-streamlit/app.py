import streamlit as st
from utils.section_splitter import split_sections
from utils.pdf_reader import read_pdf
from utils.docx_reader import read_docx
from agents.formatting_agent import check_formatting
from utils.scoring import calculate_score
from utils.role_matcher import calculate_role_match
from agents.content_agent import extract_bullets, analyze_bullets_with_ai

st.set_page_config(page_title="Resume Reviewer AI", layout="wide")

st.title("🚀 Resume Reviewer AI")
st.caption("AI powered resume feedback for placements and job applications.")

st.divider()

# ------------------------------
# Role + Upload
# ------------------------------

col1, col2 = st.columns([2,1])

with col1:
    role = st.selectbox(
        "🎯 Target Role",
        ["Software Engineer", "AI/ML Engineer", "Data Analyst"]
    )

with col2:
    uploaded_file = st.file_uploader(
        "📂 Upload Resume",
        type=["pdf","docx"]
    )

st.divider()

# ------------------------------
# Analyze Resume Button
# ------------------------------

analyze = st.button("⚡ Analyze Resume")

if analyze and uploaded_file is not None:

    if uploaded_file.name.endswith(".pdf"):
        resume_text = read_pdf(uploaded_file)
    else:
        resume_text = read_docx(uploaded_file)

    sections = split_sections(resume_text)

    format_result = check_formatting(sections)
    score = calculate_score(format_result)

    match_percentage, matched_skills, missing_skills = calculate_role_match(
        resume_text, role
    )

    # Save results to session state
    st.session_state.resume_text = resume_text
    st.session_state.sections = sections
    st.session_state.format_result = format_result
    st.session_state.score = score
    st.session_state.match_percentage = match_percentage
    st.session_state.matched_skills = matched_skills
    st.session_state.missing_skills = missing_skills

# ------------------------------
# Display Results if Available
# ------------------------------

if "score" in st.session_state:

    score = st.session_state.score
    match_percentage = st.session_state.match_percentage
    matched_skills = st.session_state.matched_skills
    missing_skills = st.session_state.missing_skills
    sections = st.session_state.sections
    format_result = st.session_state.format_result

    # Dashboard metrics
    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Resume Score", f"{score}/100")

    with m2:
        st.metric("Role Match", f"{match_percentage}%")

    with m3:
        st.metric("Detected Skills", len(matched_skills))

    st.divider()

    # Tabs
    tab1, tab2, tab3 = st.tabs(
        ["📊 Formatting", "🎯 Role Match", "📄 Resume Sections"]
    )

    with tab1:

        if format_result["issues"]:
            for issue in format_result["issues"]:
                st.error(issue)

        if format_result["warnings"]:
            for warn in format_result["warnings"]:
                st.warning(warn)

        if not format_result["issues"] and not format_result["warnings"]:
            st.success("No formatting issues detected.")

    with tab2:

        st.write("### Matched Skills")
        st.write(", ".join(matched_skills) if matched_skills else "None")

        st.write("### Missing Skills")
        st.write(", ".join(missing_skills) if missing_skills else "None")

    with tab3:

        for name, content in sections.items():
            with st.expander(name.capitalize()):

                if content.strip():
                    lines = [line.strip() for line in content.split("\n") if line.strip()]
                    for line in lines:
                        st.markdown(f"- {line}")
                else:
                    st.write("No content detected.")

    st.divider()

    # ------------------------------
    # AI Suggestions Button
    # ------------------------------

    st.subheader("🤖 AI Suggestions")

    ai_button = st.button("Generate AI Suggestions")

    if ai_button:

        combined_text = (
            st.session_state.sections["projects"]
            + "\n"
            + st.session_state.sections["experience"]
        )

        bullets = extract_bullets(combined_text)

        with st.spinner("AI analyzing your resume bullets..."):

            ai_feedback = analyze_bullets_with_ai(bullets)

        if bullets:
            if ai_feedback:
                st.markdown(ai_feedback)
            else:
                st.warning("AI did not return feedback.")
        else:
            st.warning("No bullet-style content detected.")

    st.divider()

    with st.expander("View Extracted Resume Text"):
        st.text_area("Resume Content", st.session_state.resume_text, height=300)