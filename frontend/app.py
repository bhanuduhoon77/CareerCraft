import streamlit as st
import requests


# =========================================================
# CONFIG
# =========================================================

API_BASE_URL = "http://127.0.0.1:8000"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CareerCraft",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

if "resume_analyzed" not in st.session_state:
    st.session_state.resume_analyzed = False

if "selected_career_id" not in st.session_state:
    st.session_state.selected_career_id = None

if "selected_career" not in st.session_state:
    st.session_state.selected_career = None

if "assessment" not in st.session_state:
    st.session_state.assessment = None

if "assessment_answers" not in st.session_state:
    st.session_state.assessment_answers = {}

if "assessment_result" not in st.session_state:
    st.session_state.assessment_result = None


token = st.session_state.access_token


# =========================================================
# API HEADERS
# =========================================================

def get_headers():

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }


# =========================================================
# LOGIN
# =========================================================

def login_user(email, password):

    try:

        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={
                "email": email,
                "password": password
            },
            timeout=10
        )

        if response.status_code != 200:

            try:
                error = response.json()
            except Exception:
                error = response.text

            return False, error

        data = response.json()

        access_token = data.get("access_token")

        if not access_token:
            return False, "Backend did not return access token."

        st.session_state.access_token = access_token

        user_response = requests.get(
            f"{API_BASE_URL}/auth/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            },
            timeout=10
        )

        if user_response.status_code == 200:

            user_data = user_response.json()

            st.session_state.user = user_data.get(
                "user",
                {}
            )

        return True, "Login successful"

    except requests.exceptions.RequestException as e:

        return False, f"Could not connect to backend: {e}"


# =========================================================
# REGISTER
# =========================================================

def register_user(name, email, password):

    try:

        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={
                "name": name,
                "email": email,
                "password": password
            },
            timeout=10
        )

        if response.status_code in [200, 201]:

            return True, response.json()

        try:
            error = response.json()
        except Exception:
            error = response.text

        return False, error

    except requests.exceptions.RequestException as e:

        return False, f"Could not connect to backend: {e}"


# =========================================================
# CURRENT USER
# =========================================================

def get_current_user():

    try:

        response = requests.get(
            f"{API_BASE_URL}/auth/me",
            headers=get_headers(),
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            user = data.get(
                "user",
                {}
            )

            st.session_state.user = user

            return user

        return None

    except requests.exceptions.RequestException:

        return None


# =========================================================
# GET ROADMAP
# =========================================================

def get_roadmap():

    try:

        response = requests.get(
            f"{API_BASE_URL}/roadmap/current",
            headers=get_headers(),
            timeout=10
        )

        if response.status_code == 200:

            return response.json()

        if response.status_code == 404:

            return None

        st.error(
            f"Roadmap API Error: {response.status_code}"
        )

        try:
            st.json(response.json())
        except Exception:
            st.code(response.text)

        return None

    except requests.exceptions.RequestException as e:

        st.error(
            f"Could not connect to backend: {e}"
        )

        return None


# =========================================================
# CAREER RECOMMENDATIONS
# =========================================================

def get_career_recommendations():

    try:

        response = requests.get(
            f"{API_BASE_URL}/career/recommend",
            headers=get_headers(),
            timeout=30
        )

        if response.status_code == 200:

            return True, response.json()

        try:
            error = response.json()
        except Exception:
            error = response.text

        return False, error

    except requests.exceptions.RequestException as e:

        return False, f"Could not connect to backend: {e}"


# =========================================================
# JOB RECOMMENDATIONS
# =========================================================

def get_job_recommendations():

    try:

        response = requests.get(
            f"{API_BASE_URL}/jobs/recommend",
            headers=get_headers(),
            timeout=30
        )

        if response.status_code == 200:

            return True, response.json()

        try:
            error = response.json()
        except Exception:
            error = response.text

        return False, error

    except requests.exceptions.RequestException as e:

        return False, f"Could not connect to backend: {e}"


# =========================================================
# UPLOAD RESUME
# =========================================================

def upload_resume(uploaded_file):

    try:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        response = requests.post(
            f"{API_BASE_URL}/resume/upload",
            headers={
                "Authorization": f"Bearer {token}"
            },
            files=files,
            timeout=60
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.resume_uploaded = True
            st.session_state.resume_analyzed = False

            return True, data

        try:
            error = response.json()
        except Exception:
            error = response.text

        return False, error

    except requests.exceptions.RequestException as e:

        return False, f"Could not connect to backend: {e}"


# =========================================================
# ANALYZE RESUME
# =========================================================

def analyze_resume():

    try:

        response = requests.post(
            f"{API_BASE_URL}/resume/analyze",
            headers=get_headers(),
            timeout=120
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.resume_analyzed = True

            return True, data

        try:
            error = response.json()
        except Exception:
            error = response.text

        return False, error

    except requests.exceptions.RequestException as e:

        return False, f"Could not connect to backend: {e}"


# =========================================================
# GENERATE ROADMAP
# =========================================================

def generate_roadmap(career_id):

    try:

        response = requests.post(
            f"{API_BASE_URL}/roadmap/generate/{career_id}",
            headers=get_headers(),
            timeout=120
        )

        if response.status_code == 200:

            return True, response.json()

        try:
            error = response.json()
        except Exception:
            error = response.text

        return False, error

    except requests.exceptions.RequestException as e:

        return False, f"Could not connect to backend: {e}"


# =========================================================
# CREATE ASSESSMENT
# =========================================================

def create_assessment(roadmap_item_id):

    try:

        response = requests.post(
            f"{API_BASE_URL}/assessment/create/{roadmap_item_id}",
            headers=get_headers(),
            timeout=120
        )

        if response.status_code == 200:

            data = response.json()

            return True, data

        try:
            error = response.json()
        except Exception:
            error = response.text

        return False, error

    except requests.exceptions.RequestException as e:

        return False, f"Could not connect to backend: {e}"


# =========================================================
# SUBMIT ASSESSMENT
# =========================================================

def submit_assessment(assessment_id, answers):

    try:

        response = requests.post(
            f"{API_BASE_URL}/assessment/submit/{assessment_id}",
            headers=get_headers(),
            json={
                "answers": answers
            },
            timeout=60
        )

        if response.status_code == 200:

            return True, response.json()

        try:
            error = response.json()
        except Exception:
            error = response.text

        return False, error

    except requests.exceptions.RequestException as e:

        return False, f"Could not connect to backend: {e}"


# =========================================================
# LOGIN / REGISTER SCREEN
# =========================================================

if not token:

    st.title("🎯 CareerCraft")

    st.write(
        "Your AI-powered career recommendation and placement platform."
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )


    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        st.subheader("Welcome Back 👋")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            type="primary",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "Please enter email and password."
                )

            else:

                success, result = login_user(
                    email,
                    password
                )

                if success:

                    st.success(
                        "Login successful! 🎉"
                    )

                    st.rerun()

                else:

                    st.error(
                        f"Login failed: {result}"
                    )


    # =====================================================
    # REGISTER
    # =====================================================

    with register_tab:

        st.subheader(
            "Create Your CareerCraft Account 🚀"
        )

        name = st.text_input(
            "Name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True
        ):

            if not name or not email or not password:

                st.warning(
                    "Please fill all fields."
                )

            else:

                success, result = register_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success(
                        "Account created successfully! 🎉"
                    )

                    st.info(
                        "Now login using your email and password."
                    )

                else:

                    st.error(
                        f"Registration failed: {result}"
                    )

    st.stop()


# =========================================================
# AUTH CHECK
# =========================================================

current_user = get_current_user()

if current_user is None:

    st.session_state.access_token = None
    st.session_state.user = None

    st.error(
        "Session expired. Please login again."
    )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎯 CareerCraft")

    st.caption(
        "AI Career & Placement Platform"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🎯 Career",
            "🗺️ Roadmap",
            "🧠 Assessment",
            "💼 Jobs",
            "📄 Resume Analysis",
            "👤 Profile"
        ]
    )

    st.divider()

    st.write(
        f"👤 {current_user.get('name', 'User')}"
    )

    if st.session_state.selected_career:

        st.caption(
            f"Selected Career: "
            f"{st.session_state.selected_career}"
        )

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.access_token = None
        st.session_state.user = None
        st.session_state.resume_uploaded = False
        st.session_state.resume_analyzed = False
        st.session_state.selected_career_id = None
        st.session_state.selected_career = None
        st.session_state.assessment = None
        st.session_state.assessment_answers = {}
        st.session_state.assessment_result = None

        st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.title("Dashboard")

    st.write(
        "Your career journey at a glance."
    )

    st.success(
        f"Welcome, {current_user.get('name', 'User')} 👋"
    )

    st.divider()

    roadmap_data = get_roadmap()


    if not roadmap_data:

        st.warning(
            "No roadmap found for your account."
        )

        st.info(
            "Create your personalized roadmap using your resume."
        )

        st.subheader(
            "🚀 Create Your Roadmap"
        )

        if st.session_state.selected_career:

            st.write(
                f"Selected Career: "
                f"**{st.session_state.selected_career}**"
            )

        else:

            st.write(
                "First select a career from the "
                "🎯 Career Recommendation page."
            )

        st.divider()

        # =================================================
        # STEP 1
        # =================================================

        st.markdown(
            "### Step 1️⃣ — Upload Your Resume"
        )

        uploaded_file = st.file_uploader(
            "Upload your resume PDF",
            type=["pdf"],
            key="dashboard_resume_upload"
        )

        if uploaded_file:

            if st.button(
                "📤 Upload Resume",
                type="primary",
                use_container_width=True
            ):

                with st.spinner(
                    "Uploading resume..."
                ):

                    success, result = upload_resume(
                        uploaded_file
                    )

                if success:

                    st.success(
                        "Resume uploaded successfully! ✅"
                    )

                else:

                    st.error(
                        "Resume upload failed."
                    )

                    st.json(result)


        # =================================================
        # STEP 2
        # =================================================

        st.markdown(
            "### Step 2️⃣ — Analyze Resume with AI"
        )

        if st.session_state.resume_uploaded:

            if st.button(
                "🤖 Analyze Resume",
                type="primary",
                use_container_width=True
            ):

                with st.spinner(
                    "Gemini is analyzing your resume..."
                ):

                    success, result = analyze_resume()

                if success:

                    st.success(
                        "Resume analyzed successfully! 🎉"
                    )

                    analysis = result.get(
                        "analysis",
                        {}
                    )

                    skills = analysis.get(
                        "skills",
                        []
                    )

                    if skills:

                        st.write(
                            "**Detected Skills:**"
                        )

                        st.write(
                            ", ".join(
                                str(skill)
                                for skill in skills
                            )
                        )

                    missing_skills = analysis.get(
                        "missing_skills",
                        []
                    )

                    if missing_skills:

                        st.write(
                            "**Missing Skills:**"
                        )

                        st.write(
                            ", ".join(
                                str(skill)
                                for skill in missing_skills
                            )
                        )

                else:

                    st.error(
                        "Resume analysis failed."
                    )

                    st.json(result)

        else:

            st.info(
                "Upload your resume first."
            )


        # =================================================
        # STEP 3
        # =================================================

        st.markdown(
            "### Step 3️⃣ — Select Your Career"
        )

        st.info(
            "Go to 🎯 Career and select the career "
            "you want to pursue."
        )

        if st.session_state.selected_career:

            st.success(
                f"Selected Career: "
                f"{st.session_state.selected_career}"
            )


        # =================================================
        # STEP 4
        # =================================================

        st.markdown(
            "### Step 4️⃣ — Generate Personalized Roadmap"
        )

        selected_career_id = (
            st.session_state.selected_career_id
        )

        if not selected_career_id:

            st.warning(
                "Please select a career first."
            )

        elif not st.session_state.resume_analyzed:

            st.warning(
                "Analyze your resume first."
            )

        else:

            if st.button(
                "🗺️ Generate Roadmap",
                type="primary",
                use_container_width=True
            ):

                with st.spinner(
                    "Creating your personalized roadmap..."
                ):

                    success, result = generate_roadmap(
                        career_id=selected_career_id
                    )

                if success:

                    st.success(
                        "Roadmap created successfully! 🎉"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Could not generate roadmap."
                    )

                    st.json(result)


    else:

        roadmap = roadmap_data.get(
            "roadmap",
            {}
        )

        items = roadmap_data.get(
            "items",
            []
        )

        progress = roadmap.get(
            "progress",
            0
        )

        completed_items = [
            item
            for item in items
            if item.get("status") == "completed"
        ]

        col1, col2, col3, col4 = st.columns(4)

        career_title = roadmap.get(
            "title",
            "Not available"
        ).replace(
            " Career Roadmap",
            ""
        )

        with col1:

            st.metric(
                "Career",
                career_title
            )

        with col2:

            st.metric(
                "Roadmap Progress",
                f"{progress}%"
            )

        with col3:

            st.metric(
                "Completed Items",
                len(completed_items)
            )

        with col4:

            st.metric(
                "Total Items",
                len(items)
            )

        st.divider()

        st.subheader(
            "🎯 Selected Career"
        )

        with st.container(border=True):

            st.markdown(
                f"### {career_title}"
            )

            st.write(
                roadmap.get(
                    "description",
                    "Personalized career recommendation."
                )
            )

            st.progress(
                progress / 100
            )

            st.caption(
                f"Roadmap completion: {progress}%"
            )

        st.divider()

        st.subheader(
            "🗺️ Your Roadmap"
        )

        for index, item in enumerate(
            items,
            start=1
        ):

            status = item.get(
                "status",
                "pending"
            )

            title = item.get(
                "title",
                "Untitled"
            )

            description = item.get(
                "description",
                ""
            )

            score = item.get(
                "score",
                0
            )

            if status == "completed":

                st.success(
                    f"✅ {index}. {title}"
                )

            else:

                st.warning(
                    f"⏳ {index}. {title}"
                )

            st.write(description)

            st.caption(
                f"Status: {status} • Score: {score}%"
            )

            st.divider()


# =========================================================
# ROADMAP PAGE
# =========================================================

elif page == "🗺️ Roadmap":

    st.title(
        "🗺️ Career Roadmap"
    )

    roadmap_data = get_roadmap()

    if roadmap_data:

        roadmap = roadmap_data.get(
            "roadmap",
            {}
        )

        items = roadmap_data.get(
            "items",
            []
        )

        progress = roadmap.get(
            "progress",
            0
        )

        st.subheader(
            roadmap.get(
                "title",
                "Your Roadmap"
            )
        )

        st.progress(
            progress / 100
        )

        st.write(
            f"Overall Progress: **{progress}%**"
        )

        st.divider()

        for index, item in enumerate(
            items,
            start=1
        ):

            status = item.get(
                "status",
                "pending"
            )

            if status == "completed":

                st.success(
                    f"✅ {index}. "
                    f"{item.get('title')}"
                )

            else:

                st.warning(
                    f"⏳ {index}. "
                    f"{item.get('title')}"
                )

            st.write(
                item.get(
                    "description",
                    ""
                )
            )

            st.caption(
                f"Status: {status} "
                f"• Score: {item.get('score', 0)}%"
            )

            st.divider()

    else:

        st.warning(
            "No roadmap found."
        )


# =========================================================
# CAREER RECOMMENDATION
# =========================================================

elif page == "🎯 Career":

    st.title(
        "🎯 Career Recommendation"
    )

    st.write(
        "AI-powered career recommendations "
        "based on your analyzed resume."
    )

    st.divider()

    success, result = get_career_recommendations()

    if success:

        skills = result.get(
            "skills",
            []
        )

        recommendations = result.get(
            "recommendations",
            []
        )

        st.subheader(
            "🧠 Skills Detected From Your Resume"
        )

        if skills:

            st.write(
                ", ".join(
                    str(skill)
                    for skill in skills
                )
            )

        else:

            st.warning(
                "No skills found."
            )

        st.divider()

        st.subheader(
            "🎯 Recommended Careers"
        )

        if recommendations:

            for index, recommendation in enumerate(
                recommendations,
                start=1
            ):

                career_id = recommendation.get(
                    "career_id"
                )

                career = recommendation.get(
                    "career",
                    "Unknown Career"
                )

                match_score = recommendation.get(
                    "match_score",
                    0
                )

                matched_skills = recommendation.get(
                    "matched_skills",
                    []
                )

                missing_skills = recommendation.get(
                    "missing_skills",
                    []
                )

                with st.container(border=True):

                    st.markdown(
                        f"### {index}. {career}"
                    )

                    st.metric(
                        "Career Match",
                        f"{match_score}%"
                    )

                    st.progress(
                        min(
                            max(
                                match_score / 100,
                                0
                            ),
                            1
                        )
                    )

                    if matched_skills:

                        st.write(
                            "✅ **Matched Skills:**"
                        )

                        st.write(
                            ", ".join(
                                str(skill)
                                for skill in matched_skills
                            )
                        )

                    else:

                        st.write(
                            "✅ **Matched Skills:** None"
                        )

                    if missing_skills:

                        st.write(
                            "❌ **Missing Skills:**"
                        )

                        st.write(
                            ", ".join(
                                str(skill)
                                for skill in missing_skills
                            )
                        )

                    else:

                        st.write(
                            "❌ **Missing Skills:** None"
                        )

                    if (
                        st.session_state.selected_career_id
                        == career_id
                    ):

                        st.success(
                            "⭐ Currently Selected"
                        )

                    else:

                        if st.button(
                            f"Select {career}",
                            key=f"select_career_{career_id}",
                            use_container_width=True
                        ):

                            st.session_state.selected_career_id = (
                                career_id
                            )

                            st.session_state.selected_career = (
                                career
                            )

                            st.success(
                                f"{career} selected successfully!"
                            )

                            st.rerun()

        else:

            st.warning(
                "No career recommendations available."
            )

    else:

        if isinstance(result, dict):

            detail = result.get(
                "detail",
                "Unable to get career recommendations."
            )

            st.warning(
                detail
            )

        else:

            st.error(
                "Career recommendation failed."
            )

            st.write(result)


# =========================================================
# ASSESSMENT
# =========================================================

elif page == "🧠 Assessment":

    st.title(
        "🧠 Skill Assessments"
    )

    st.write(
        "Test your knowledge of roadmap skills using "
        "AI-generated multiple-choice questions."
    )

    st.divider()

    roadmap_data = get_roadmap()

    if not roadmap_data:

        st.warning(
            "Please create your career roadmap first."
        )

    else:

        items = roadmap_data.get(
            "items",
            []
        )

        if not items:

            st.warning(
                "No roadmap items available."
            )

        else:

            st.subheader(
                "📚 Select a Skill"
            )

            item_options = {}

            for item in items:

                item_id = item.get("id")

                title = item.get(
                    "title",
                    "Unknown Skill"
                )

                status = item.get(
                    "status",
                    "pending"
                )

                item_options[
                    f"{title} ({status})"
                ] = item_id

            selected_item_label = st.selectbox(
                "Choose a roadmap skill",
                list(item_options.keys())
            )

            selected_item_id = item_options[
                selected_item_label
            ]

            st.divider()

            if st.session_state.assessment is None:

                st.info(
                    "Click below to generate a 5-question "
                    "AI assessment."
                )

                if st.button(
                    "🤖 Generate Assessment",
                    type="primary",
                    use_container_width=True
                ):

                    with st.spinner(
                        "Gemini is generating your assessment..."
                    ):

                        success, result = create_assessment(
                            selected_item_id
                        )

                    if success:

                        st.session_state.assessment = result

                        st.session_state.assessment_answers = {}

                        st.session_state.assessment_result = None

                        st.success(
                            "Assessment generated successfully! 🎉"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Could not create assessment."
                        )

                        st.json(result)

            else:

                assessment = st.session_state.assessment

                assessment_id = assessment.get(
                    "assessment_id"
                )

                topic = assessment.get(
                    "topic",
                    "Skill Assessment"
                )

                questions = assessment.get(
                    "questions",
                    []
                )

                st.subheader(
                    f"📝 Assessment: {topic}"
                )

                st.caption(
                    f"Total Questions: {len(questions)}"
                )

                st.divider()

                for index, question in enumerate(
                    questions
                ):

                    question_text = question.get(
                        "question",
                        ""
                    )

                    options = question.get(
                        "options",
                        []
                    )

                    st.markdown(
                        f"### Question {index + 1}"
                    )

                    st.write(
                        question_text
                    )

                    answer = st.radio(
                        "Select your answer:",
                        options,
                        key=f"assessment_q_{assessment_id}_{index}",
                        index=None
                    )

                    st.session_state.assessment_answers[
                        index
                    ] = answer

                    st.divider()

                if st.button(
                    "✅ Submit Assessment",
                    type="primary",
                    use_container_width=True
                ):

                    answers = []

                    unanswered = False

                    for index in range(
                        len(questions)
                    ):

                        answer = (
                            st.session_state.assessment_answers
                            .get(index)
                        )

                        if answer is None:

                            unanswered = True

                        answers.append(
                            answer if answer is not None else ""
                        )

                    if unanswered:

                        st.warning(
                            "Please answer all questions before submitting."
                        )

                    else:

                        with st.spinner(
                            "Evaluating your answers..."
                        ):

                            success, result = submit_assessment(
                                assessment_id,
                                answers
                            )

                        if success:

                            st.session_state.assessment_result = result

                            st.success(
                                "Assessment submitted successfully! 🎉"
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Assessment submission failed."
                            )

                            st.json(result)

                if st.session_state.assessment_result:

                    result = (
                        st.session_state.assessment_result
                    )

                    st.divider()

                    st.subheader(
                        "📊 Assessment Result"
                    )

                    score = result.get(
                        "score",
                        0
                    )

                    correct_answers = result.get(
                        "correct_answers",
                        0
                    )

                    total_questions = result.get(
                        "total_questions",
                        len(questions)
                    )

                    roadmap_item_status = result.get(
                        "roadmap_item_status",
                        "pending"
                    )

                    roadmap_progress = result.get(
                        "roadmap_progress",
                        0
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Score",
                            f"{score}%"
                        )

                    with col2:

                        st.metric(
                            "Correct Answers",
                            f"{correct_answers}/{total_questions}"
                        )

                    with col3:

                        st.metric(
                            "Roadmap Progress",
                            f"{roadmap_progress}%"
                        )

                    if score >= 60:

                        st.success(
                            "🎉 Skill completed! "
                            "You scored 60% or above."
                        )

                    else:

                        st.warning(
                            "Keep practicing! "
                            "You need 60% or above to complete this skill."
                        )

                    st.write(
                        f"**Skill Status:** "
                        f"{roadmap_item_status}"
                    )

                    st.divider()

                    if st.button(
                        "🔄 Take Another Assessment",
                        use_container_width=True
                    ):

                        st.session_state.assessment = None

                        st.session_state.assessment_answers = {}

                        st.session_state.assessment_result = None

                        st.rerun()


# =========================================================
# JOBS
# =========================================================

elif page == "💼 Jobs":

    st.title(
        "💼 Recommended Jobs"
    )

    st.write(
        "Find jobs that match your skills and selected career."
    )

    st.divider()

    # =====================================================
    # SELECTED CAREER CHECK
    # =====================================================

    selected_career_id = (
        st.session_state.selected_career_id
    )

    selected_career = (
        st.session_state.selected_career
    )

    if not selected_career_id:

        st.warning(
            "Please select a career first."
        )

        st.info(
            "Go to 🎯 Career and select a career."
        )

    else:

        st.success(
            f"🎯 Showing jobs for: **{selected_career}**"
        )

        st.divider()

        # =================================================
        # GET JOBS
        # =================================================

        with st.spinner(
            "Finding jobs matching your profile..."
        ):

            success, result = get_job_recommendations()

        if success:

            # -------------------------------------------------
            # HANDLE RESPONSE
            # -------------------------------------------------

            jobs = result.get(
                "jobs",
                []
            )

            # -------------------------------------------------
            # CAREER FROM BACKEND
            # -------------------------------------------------

            backend_career = result.get(
                "career",
                selected_career
            )

            st.subheader(
                f"🎯 Jobs for {backend_career}"
            )

            # -------------------------------------------------
            # JOB COUNT
            # -------------------------------------------------

            st.metric(
                "Matching Jobs Found",
                len(jobs)
            )

            st.divider()

            # -------------------------------------------------
            # NO JOBS
            # -------------------------------------------------

            if not jobs:

                st.warning(
                    "No jobs found for this career."
                )

                st.info(
                    "Try another career or add more skills "
                    "to your profile."
                )

            # -------------------------------------------------
            # SHOW JOBS
            # -------------------------------------------------

            else:

                for index, job in enumerate(
                    jobs,
                    start=1
                ):

                    title = job.get(
                        "title",
                        "Unknown Job"
                    )

                    company = job.get(
                        "company",
                        "Unknown Company"
                    )

                    location = job.get(
                        "location",
                        "Location not specified"
                    )

                    description = job.get(
                        "description",
                        "No description available."
                    )

                    match_score = job.get(
                        "match_percentage",
                        job.get(
                            "match_score",
                            0
                        )
                    )

                    matched_skills = job.get(
                        "matched_skills",
                        []
                    )

                    missing_skills = job.get(
                        "missing_skills",
                        []
                    )

                    apply_url = job.get(
                        "apply_url",
                        ""
                    )

                    source = job.get(
                        "source",
                        ""
                    )

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"## 💼 {index}. {title}"
                        )

                        st.write(
                            f"**🏢 Company:** {company}"
                        )

                        st.write(
                            f"**📍 Location:** {location}"
                        )

                        if source:

                            st.caption(
                                f"Source: {source}"
                            )

                        st.divider()

                        # =================================
                        # MATCH SCORE
                        # =================================

                        col1, col2 = st.columns(2)

                        with col1:

                            st.metric(
                                "🎯 Skill Match",
                                f"{match_score}%"
                            )

                        with col2:

                            if match_score >= 80:

                                st.success(
                                    "🔥 Excellent Match"
                                )

                            elif match_score >= 60:

                                st.info(
                                    "👍 Good Match"
                                )

                            else:

                                st.warning(
                                    "📚 Skills Needed"
                                )

                        st.progress(
                            min(
                                max(
                                    float(match_score) / 100,
                                    0
                                ),
                                1
                            )
                        )

                        # =================================
                        # DESCRIPTION
                        # =================================

                        st.markdown(
                            "### 📄 Job Description"
                        )

                        st.write(
                            description
                        )

                        # =================================
                        # MATCHED SKILLS
                        # =================================

                        if matched_skills:

                            st.markdown(
                                "### ✅ Matched Skills"
                            )

                            st.write(
                                ", ".join(
                                    str(skill)
                                    for skill in matched_skills
                                )
                            )

                        # =================================
                        # MISSING SKILLS
                        # =================================

                        if missing_skills:

                            st.markdown(
                                "### ❌ Missing Skills"
                            )

                            st.write(
                                ", ".join(
                                    str(skill)
                                    for skill in missing_skills
                                )
                            )

                        # =================================
                        # APPLY BUTTON
                        # =================================

                        if apply_url:

                            st.link_button(
                                "🚀 Apply for this Job",
                                apply_url,
                                use_container_width=True
                            )

                        st.divider()

        else:

            st.error(
                "Could not load recommended jobs."
            )

            if isinstance(result, dict):

                st.json(
                    result
                )

            else:

                st.write(
                    result
                )


# =========================================================
# RESUME ANALYSIS
# =========================================================

elif page == "📄 Resume Analysis":

    st.title(
        "📄 Resume Analysis"
    )

    st.write(
        "Upload and analyze your resume using Gemini AI."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Choose your resume PDF",
        type=["pdf"],
        key="resume_page_upload"
    )

    if uploaded_file:

        if st.button(
            "📤 Upload Resume",
            type="primary"
        ):

            with st.spinner(
                "Uploading resume..."
            ):

                success, result = upload_resume(
                    uploaded_file
                )

            if success:

                st.success(
                    "Resume uploaded successfully! ✅"
                )

            else:

                st.error(
                    "Upload failed."
                )

                st.json(result)

    if st.session_state.resume_uploaded:

        st.divider()

        if st.button(
            "🤖 Analyze Resume",
            type="primary"
        ):

            with st.spinner(
                "Gemini is analyzing your resume..."
            ):

                success, result = analyze_resume()

            if success:

                st.success(
                    "Resume analyzed successfully! 🎉"
                )

                analysis = result.get(
                    "analysis",
                    {}
                )

                st.subheader(
                    "Resume Analysis"
                )

                st.json(
                    analysis
                )

            else:

                st.error(
                    "Analysis failed."
                )

                st.json(result)


# =========================================================
# PROFILE
# =========================================================

elif page == "👤 Profile":

    st.title(
        "👤 Profile"
    )

    st.subheader(
        "Your Profile"
    )

    st.write(
        f"**Name:** "
        f"{current_user.get('name', 'N/A')}"
    )

    st.write(
        f"**Email:** "
        f"{current_user.get('email', 'N/A')}"
    )

    st.write(
        f"**User ID:** "
        f"{current_user.get('id', 'N/A')}"
    )

    if st.session_state.selected_career:

        st.divider()

        st.subheader(
            "🎯 Selected Career"
        )

        st.write(
            st.session_state.selected_career
        )