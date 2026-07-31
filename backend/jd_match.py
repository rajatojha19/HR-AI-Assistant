import json

def match_resume_with_jd(model, resume_text, jd_text):

    """Compare a resume with a job description
    and return a structured ATS evaluation."""

    prompt = f"""
You are an experienced Technical HR Recruiter and Applicant Tracking System (ATS).

Compare the candidate's resume with the job description.

Rules:
- Analyze only the information provided.
- Do not make assumptions.
- Return ONLY valid JSON.
- Do not include markdown or explanations.
- The match score must be between 0 and 100.

Return JSON in exactly this format:

{{
    "match_score": 0,
    "reasoning": "",
    "matching_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "recommendation": ""
}}

Guidelines:

match_score:
Give an ATS compatibility score out of 100.

reasoning:
Explain briefly why the score was given.

matching_skills:
List technical skills found in both the resume and job description.

missing_skills:
List important skills present in the job description but missing from the resume.

strengths:
Mention strengths that increase the candidate's suitability.

weaknesses:
Mention weaknesses or missing qualifications.

suggestions:
Provide practical improvements to increase ATS compatibility.

recommendation:
Choose exactly one:
"Highly Recommended"
"Recommended"
"Needs Improvement"
"Not Recommended"

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    try:

        response = model.generate_content(prompt)

    except Exception as e:

        raise RuntimeError(
            "Unable to analyze the resume against the job description."
        ) from e

    text = response.text.strip()

    # Remove markdown if Gemini wraps JSON in ```json
    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError as e:

        return {
        "match_score": 0,
        "reasoning": "Gemini returned an invalid JSON response.",
        "matching_skills": [],
        "missing_skills": [],
        "strengths": [],
        "weaknesses": [],
        "suggestions": [],
        "recommendation": "Unable to Analyze"
        }