from backend.database import SessionLocal
from backend.services.recommendation_service import recommend_careers
from backend.models.resume_analysis import ResumeAnalysis


db = SessionLocal()

try:

    # Get latest resume analysis
    resume_analysis = (
        db.query(ResumeAnalysis)
        .order_by(ResumeAnalysis.id.desc())
        .first()
    )

    if not resume_analysis:
        print("❌ No resume analysis found.")
        exit()

    # Get skills extracted by Gemini
    user_skills = resume_analysis.skills

    if not user_skills:
        print("❌ No skills found in resume analysis.")
        exit()

    print(">>> Skills extracted from resume:")
    print(user_skills)

    print("\n>>> Testing Career Recommendation...")

    results = recommend_careers(
        user_skills,
        db
    )

    print("\n========== CAREER RECOMMENDATIONS ==========\n")

    for result in results:

        print(
            f"{result['career']} "
            f"-> {result['match_score']}%"
        )

        print(
            "Matched:",
            result["matched_skills"]
        )

        print(
            "Missing:",
            result["missing_skills"]
        )

        print("-----------------------------------")

finally:

    db.close()