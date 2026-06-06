import os

from google import genai


def summarize_institution(profile: dict) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")

    client = genai.Client(api_key=api_key)

    prompt = f"""You are an institutional intelligence analyst. Write a professional 3-5 paragraph institution intelligence summary based on the verified profile data below.

The summary must cover:
- Institution overview (name, state, website, establishment history)
- Academic strengths and institutional maturity
- Engineering program presence
- Management/MBA program presence
- Doctoral/PhD program presence
- Leadership information (vice chancellor)
- Confidence assessment based on the confidence score

Write in clear, professional prose suitable for an executive briefing. Do not invent facts beyond what is provided. If data is missing, note the limitation briefly.

Institution Profile:
- Name: {profile.get('name')}
- State: {profile.get('state')}
- Website: {profile.get('website')}
- Established Year: {profile.get('established_year')}
- Age (years): {profile.get('age')}
- Engineering Programs: {profile.get('engineering')}
- MBA/Management Programs: {profile.get('mba')}
- PhD/Doctoral Programs: {profile.get('phd')}
- Vice Chancellor: {profile.get('vice_chancellor')}
- Address: {profile.get('address')}
- Confidence Score: {profile.get('confidence')}/100
- Eligible: {profile.get('eligible')}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text.strip()
