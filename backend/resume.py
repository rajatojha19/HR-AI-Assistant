def analyze_resume(model, resume_text):
    """
    Analyze a resume using Gemini AI and return structured HR feedback.
    """

    prompt = f"""
You are an experienced Senior HR Recruiter with over 15 years of hiring experience in the IT industry.

Analyze the following resume carefully.

Instructions:
- Evaluate the resume objectively.
- Do not make assumptions that are not supported by the resume.
- Use professional and constructive language.
- Keep the response concise and easy to read.
- If any information is missing, clearly mention it.

Return your response using the following format:

# 📊 Resume Score
Give a score out of 100 and briefly explain why.

# 👤 Candidate Summary
Summarize the candidate's profile in 3–5 lines.

# 💪 Strengths
List the candidate's key strengths as bullet points.

# ⚠ Areas for Improvement
Mention weaknesses or missing information as bullet points.

# 🛠 Suggested Skills
Recommend technical skills, tools, certifications, or technologies that would improve the resume.

# 📄 Resume Improvement Suggestions
Suggest practical improvements for formatting, projects, achievements, or content.

# 🎯 Interview Recommendation
Choose ONE of the following:

- Highly Recommended
- Recommended
- Needs Improvement
- Not Recommended

Explain your decision in 2–3 sentences.

Resume:
{resume_text}
"""

    try:

        response = model.generate_content(prompt)

    except Exception as e:

        raise RuntimeError(
            "Unable to analyze the uploaded resume."
        ) from e

    return response.text