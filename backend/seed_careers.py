from backend.database import SessionLocal
from backend.models.career import Career, CareerSkill
from backend.models.skill import Skill

# Order matters: career ids must be 1..6 to match seed_jobs.py
CAREERS = [
    ("Java Backend Developer", "Build scalable backend services using Java and Spring Boot.", "Backend",
     [("Java", "high"), ("Spring Boot", "high"), ("REST API", "high"),
      ("SQL", "medium"), ("MySQL", "medium"), ("Git", "low")]),
    ("Python Backend Developer", "Build APIs and backend systems using Python and FastAPI.", "Backend",
     [("Python", "high"), ("FastAPI", "high"), ("REST API", "high"),
      ("SQL", "medium"), ("MySQL", "medium"), ("Git", "low"), ("Docker", "low")]),
    ("Machine Learning Engineer", "Design, train and deploy machine learning models.", "AI/ML",
     [("Python", "high"), ("Machine Learning", "high"), ("Scikit-learn", "high"),
      ("Pandas", "medium"), ("NumPy", "medium"), ("Deep Learning", "medium")]),
    ("Generative AI Developer", "Build applications using LLMs, RAG and vector databases.", "AI/ML",
     [("Python", "high"), ("Generative AI", "high"), ("LLM", "high"),
      ("LangChain", "medium"), ("RAG", "medium"), ("Vector Database", "medium")]),
    ("Data Analyst", "Analyze data and build dashboards to support decisions.", "Data",
     [("SQL", "high"), ("Excel", "high"), ("Data Analysis", "high"),
      ("Python", "medium"), ("Pandas", "medium"),
      ("Data Visualization", "medium"), ("Power BI", "low")]),
    ("AI Backend Engineer", "Build backend services that serve AI and ML features.", "AI/ML",
     [("Python", "high"), ("FastAPI", "high"), ("REST API", "medium"),
      ("AI", "medium"), ("Machine Learning", "medium"), ("SQL", "low")]),
]


def seed_careers():
    db = SessionLocal()

    try:
        if db.query(Career).count() > 0:
            print("Careers already exist. Skipping.")
            return

        skill_ids = {}

        for title, description, category, skills in CAREERS:
            for name, _ in skills:
                if name not in skill_ids:
                    skill = Skill(name=name, category="Technical")
                    db.add(skill)
                    db.flush()
                    skill_ids[name] = skill.id

        for title, description, category, skills in CAREERS:
            career = Career(title=title, description=description, category=category)
            db.add(career)
            db.flush()

            for name, importance in skills:
                db.add(CareerSkill(
                    career_id=career.id,
                    skill_id=skill_ids[name],
                    importance=importance,
                    required_proficiency=50
                ))

        db.commit()
        print("Careers and skills seeded successfully!")

    except Exception as e:
        db.rollback()
        print("Error while seeding careers:")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_careers()