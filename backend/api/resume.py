import os
import uuid
import json

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException
)

from sqlalchemy.orm import Session

from pypdf import PdfReader

from backend.database import get_db
from backend.models.resume import Resume
from backend.models.user import User
from backend.utils.security import get_current_user
from backend.services.gemini_service import analyze_resume
from backend.models.resume_analysis import ResumeAnalysis


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


UPLOAD_DIR = "uploads/resumes"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==========================================
# UPLOAD RESUME
# ==========================================

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_content = await file.read()

    unique_filename = (
        f"{uuid.uuid4()}_{file.filename}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    try:

        reader = PdfReader(file_path)

        extracted_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

    except Exception as e:

        os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=f"Could not read PDF: {str(e)}"
        )

    resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_path,
        extracted_text=extracted_text
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "status": "success",
        "message": "Resume uploaded successfully",
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "text_length": len(extracted_text)
    }


# ==========================================
# ANALYZE RESUME USING GENAI
# ==========================================

@router.post("/analyze")
def analyze_uploaded_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Get latest resume
    resume = (
        db.query(Resume)
        .filter(
            Resume.user_id == current_user.id
        )
        .order_by(Resume.id.desc())
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="No resume uploaded"
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Resume text is empty"
        )

    # ==============================
    # SEND RESUME TO GEMINI
    # ==============================

    try:

        print(">>> Sending resume to Gemini...")

        ai_response = analyze_resume(
            resume.extracted_text
        )

        print(">>> Gemini response received!")

    except Exception as e:

        print(">>> GEMINI ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )

    # ==============================
    # PARSE GEMINI JSON
    # ==============================

    try:

        cleaned_response = ai_response.strip()

        if cleaned_response.startswith("```"):
            cleaned_response = (
                cleaned_response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        analysis = json.loads(
            cleaned_response
        )

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail="Gemini returned invalid JSON"
        )

    # ==============================
    # SAVE AI ANALYSIS TO DATABASE
    # ==============================

    resume_analysis = ResumeAnalysis(

        resume_id=resume.id,

        user_id=current_user.id,

        name=analysis.get("name"),

        education=analysis.get("education", []),

        skills=analysis.get("skills", []),

        experience=analysis.get("experience", []),

        projects=analysis.get("projects", []),

        certifications=analysis.get(
            "certifications", []
        ),

        career_preferences=analysis.get(
            "career_preferences", []
        ),

        strengths=analysis.get(
            "strengths", []
        ),

        missing_skills=analysis.get(
            "missing_skills", []
        )
    )

    db.add(resume_analysis)

    db.commit()

    db.refresh(resume_analysis)

    # ==============================
    # RETURN RESPONSE
    # ==============================

    return {

        "status": "success",

        "message": "Resume analyzed and saved successfully",

        "resume_id": resume.id,

        "analysis_id": resume_analysis.id,

        "analysis": analysis
    }