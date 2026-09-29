def calculate_job_match(
    user_skills: list,
    required_skills: str
):

    if not user_skills or not required_skills:
        return 0, []

    user_skills_normalized = {
        skill.strip().lower()
        for skill in user_skills
    }

    required_skills_list = [
        skill.strip()
        for skill in required_skills.split(",")
        if skill.strip()
    ]

    if not required_skills_list:
        return 0, []

    matched_skills = []

    for skill in required_skills_list:

        if skill.lower() in user_skills_normalized:
            matched_skills.append(skill)

    match_percentage = (
        len(matched_skills) /
        len(required_skills_list)
    ) * 100

    return round(match_percentage, 2), matched_skills