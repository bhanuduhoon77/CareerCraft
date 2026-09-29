import json
from backend.database import SessionLocal
from backend.models.job import Job


# =========================================================
# JOB DATA
# =========================================================

JOBS = [

    # =====================================================
    # 1. JAVA BACKEND DEVELOPER
    # =====================================================

    {
        "title": "Java Backend Developer",
        "company": "Tech Solutions",
        "location": "Noida, India",
        "description": (
            "Develop and maintain backend applications using Java, "
            "Spring Boot and REST APIs."
        ),
        "required_skills": [
            "Java",
            "Spring Boot",
            "REST API",
            "SQL",
            "MySQL"
        ],
        "apply_url": "https://www.linkedin.com/jobs/search/?keywords=Java%20Backend%20Developer",
        "source": "LinkedIn",
        "career_id": 1
    },

    {
        "title": "Java Backend Engineer",
        "company": "Software Technologies",
        "location": "Bangalore, India",
        "description": (
            "Build scalable backend services and APIs using Java "
            "and Spring Boot."
        ),
        "required_skills": [
            "Java",
            "Spring Boot",
            "REST API",
            "SQL",
            "Git"
        ],
        "apply_url": "https://www.naukri.com/java-backend-developer-jobs",
        "source": "Naukri",
        "career_id": 1
    },


    # =====================================================
    # 2. PYTHON BACKEND DEVELOPER
    # =====================================================

    {
        "title": "Python Backend Developer",
        "company": "Python Technologies",
        "location": "Noida, India",
        "description": (
            "Develop backend services and REST APIs using Python "
            "and FastAPI."
        ),
        "required_skills": [
            "Python",
            "FastAPI",
            "REST API",
            "SQL",
            "MySQL"
        ],
        "apply_url": "https://www.linkedin.com/jobs/search/?keywords=Python%20Backend%20Developer",
        "source": "LinkedIn",
        "career_id": 2
    },

    {
        "title": "Python Backend Engineer",
        "company": "Cloud Software",
        "location": "Bangalore, India",
        "description": (
            "Design and develop scalable backend applications "
            "using Python, FastAPI and databases."
        ),
        "required_skills": [
            "Python",
            "FastAPI",
            "REST API",
            "SQL",
            "Git"
        ],
        "apply_url": "https://www.naukri.com/python-backend-developer-jobs",
        "source": "Naukri",
        "career_id": 2
    },

    {
        "title": "Python API Developer",
        "company": "Backend Labs",
        "location": "Remote",
        "description": (
            "Build production-ready APIs and backend services "
            "using Python and FastAPI."
        ),
        "required_skills": [
            "Python",
            "FastAPI",
            "REST API",
            "SQL",
            "Docker"
        ],
        "apply_url": "https://www.linkedin.com/jobs/search/?keywords=Python%20API%20Developer",
        "source": "LinkedIn",
        "career_id": 2
    },


    # =====================================================
    # 3. AI/ML ENGINEER
    # =====================================================

    {
        "title": "Machine Learning Engineer",
        "company": "AI Technologies",
        "location": "Bangalore, India",
        "description": (
            "Develop machine learning models and data pipelines "
            "for real-world AI applications."
        ),
        "required_skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn"
        ],
        "apply_url": "https://www.linkedin.com/jobs/search/?keywords=Machine%20Learning%20Engineer",
        "source": "LinkedIn",
        "career_id": 3
    },

    {
        "title": "AI/ML Engineer",
        "company": "Intelligent Systems",
        "location": "Hyderabad, India",
        "description": (
            "Build and deploy machine learning solutions "
            "using Python and modern ML frameworks."
        ),
        "required_skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "NumPy",
            "Pandas"
        ],
        "apply_url": "https://www.naukri.com/machine-learning-engineer-jobs",
        "source": "Naukri",
        "career_id": 3
    },


    # =====================================================
    # 4. GENERATIVE AI DEVELOPER
    # =====================================================

    {
        "title": "Generative AI Developer",
        "company": "GenAI Labs",
        "location": "Bangalore, India",
        "description": (
            "Develop AI-powered applications using LLMs, "
            "LangChain and Retrieval Augmented Generation."
        ),
        "required_skills": [
            "Python",
            "Generative AI",
            "LangChain",
            "RAG",
            "LLM"
        ],
        "apply_url": "https://www.linkedin.com/jobs/search/?keywords=Generative%20AI%20Developer",
        "source": "LinkedIn",
        "career_id": 4
    },

    {
        "title": "GenAI Engineer",
        "company": "AI Innovations",
        "location": "Pune, India",
        "description": (
            "Build LLM-powered applications and RAG pipelines "
            "for enterprise use cases."
        ),
        "required_skills": [
            "Python",
            "Generative AI",
            "LangChain",
            "Vector Database",
            "RAG"
        ],
        "apply_url": "https://www.naukri.com/generative-ai-jobs",
        "source": "Naukri",
        "career_id": 4
    },


    # =====================================================
    # 5. DATA ANALYST
    # =====================================================

    {
        "title": "Data Analyst",
        "company": "Analytics Solutions",
        "location": "Noida, India",
        "description": (
            "Analyze business data, create reports and dashboards, "
            "and generate actionable insights."
        ),
        "required_skills": [
            "SQL",
            "Excel",
            "Python",
            "Pandas",
            "Data Analysis"
        ],
        "apply_url": "https://www.linkedin.com/jobs/search/?keywords=Data%20Analyst",
        "source": "LinkedIn",
        "career_id": 5
    },

    {
        "title": "Junior Data Analyst",
        "company": "Business Analytics",
        "location": "Delhi, India",
        "description": (
            "Work with structured datasets, perform data analysis "
            "and prepare business reports."
        ),
        "required_skills": [
            "SQL",
            "Excel",
            "Python",
            "Pandas",
            "Data Visualization"
        ],
        "apply_url": "https://www.naukri.com/data-analyst-jobs",
        "source": "Naukri",
        "career_id": 5
    },

    {
        "title": "Business Data Analyst",
        "company": "Data Insights Pvt Ltd",
        "location": "Gurgaon, India",
        "description": (
            "Analyze business performance data and communicate "
            "insights through reports and dashboards."
        ),
        "required_skills": [
            "SQL",
            "Excel",
            "Power BI",
            "Python",
            "Data Analysis"
        ],
        "apply_url": "https://www.linkedin.com/jobs/search/?keywords=Business%20Data%20Analyst",
        "source": "LinkedIn",
        "career_id": 5
    },


    # =====================================================
    # 6. AI BACKEND ENGINEER
    # =====================================================

    {
        "title": "AI Backend Engineer",
        "company": "AI Systems",
        "location": "Bangalore, India",
        "description": (
            "Develop backend services for AI applications using "
            "Python, FastAPI and AI technologies."
        ),
        "required_skills": [
            "Python",
            "FastAPI",
            "REST API",
            "AI",
            "SQL"
        ],
        "apply_url": "https://www.linkedin.com/jobs/search/?keywords=AI%20Backend%20Engineer",
        "source": "LinkedIn",
        "career_id": 6
    },

    {
        "title": "Machine Learning Backend Engineer",
        "company": "Intelligent Labs",
        "location": "Hyderabad, India",
        "description": (
            "Build backend infrastructure and APIs for "
            "machine learning and AI applications."
        ),
        "required_skills": [
            "Python",
            "FastAPI",
            "Machine Learning",
            "REST API",
            "SQL"
        ],
        "apply_url": "https://www.naukri.com/ai-engineer-jobs",
        "source": "Naukri",
        "career_id": 6
    }
]


# =========================================================
# SEED JOBS
# =========================================================

def seed_jobs():

    db = SessionLocal()

    try:

        # -------------------------------------------------
        # Remove old jobs
        # -------------------------------------------------

        deleted_count = db.query(Job).delete()

        print(
            f"Deleted old jobs: {deleted_count}"
        )


        # -------------------------------------------------
        # Insert new jobs
        # -------------------------------------------------

        for job_data in JOBS:

            job = Job(
                title=job_data["title"],
                company=job_data["company"],
                location=job_data["location"],
                description=job_data["description"],
                required_skills=json.dumps(job_data["required_skills"]),
                apply_url=job_data["apply_url"],
                source=job_data["source"],
                career_id=job_data["career_id"]
            )

            db.add(job)


        db.commit()


        print(
            f"Successfully inserted {len(JOBS)} jobs."
        )


        # -------------------------------------------------
        # Show inserted jobs
        # -------------------------------------------------

        jobs = db.query(Job).order_by(
            Job.career_id,
            Job.id
        ).all()


        print("\nInserted Jobs:")
        print("-" * 80)


        for job in jobs:

            print(
                f"ID: {job.id} | "
                f"Career ID: {job.career_id} | "
                f"{job.title} | "
                f"{job.company}"
            )


    except Exception as e:

        db.rollback()

        print(
            "Error while seeding jobs:"
        )

        print(e)


    finally:

        db.close()


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    seed_jobs()