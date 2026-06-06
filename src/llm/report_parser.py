import re


def _parse_bool(value: str | None) -> bool:
    if not value:
        return False
    return value.strip().lower() in {"true", "1", "yes"}


def _section_content(content: str, heading: str) -> str:
    pattern = rf"## {re.escape(heading)}\s*\n([\s\S]*?)(?=\n## |\Z)"
    match = re.search(pattern, content)
    if not match:
        return ""
    return match.group(1).strip()


def _field(content: str, label: str) -> str | None:
    match = re.search(rf"- {re.escape(label)}:\s*(.+)", content)
    if not match:
        return None
    return match.group(1).strip()


def parse_report_locally(report_content: str, institution_name: str) -> dict:
    name = institution_name
    for line in report_content.splitlines():
        if line.startswith("# "):
            name = line[2:].strip()
            break

    state = _field(report_content, "State")
    website = _field(report_content, "Website")
    established_year = _field(report_content, "Established Year")
    age = _field(report_content, "Age")
    engineering = _parse_bool(_field(report_content, "Engineering"))
    mba = _parse_bool(_field(report_content, "MBA"))
    phd = _parse_bool(_field(report_content, "PhD"))
    eligible = _parse_bool(_field(report_content, "Eligible"))

    leadership = _section_content(report_content, "Leadership")
    address = _section_content(report_content, "Address")

    confidence = 0
    confidence_match = re.search(r"## Confidence Score\s*\n\s*(\d+)/100", report_content)
    if confidence_match:
        confidence = int(confidence_match.group(1))

    year_int = int(established_year) if established_year and established_year.isdigit() else None
    age_int = int(age) if age and age.isdigit() else None

    overview = (
        f"{name} is a higher education institution located in {state or 'an unspecified state'}. "
        f"{'It was established in ' + str(year_int) + ' and has operated for ' + str(age_int) + ' years.' if year_int and age_int else ''} "
        f"{'Official website: ' + website + '.' if website else ''}"
    ).strip()

    verified_programs = []
    if engineering:
        verified_programs.append("engineering")
    if mba:
        verified_programs.append("MBA/management")
    if phd:
        verified_programs.append("doctoral (PhD)")

    academic_strengths = (
        f"The institution demonstrates verified presence across "
        f"{', '.join(verified_programs) if verified_programs else 'limited verified programs'}. "
        f"{'With ' + str(age_int) + ' years of operation, it shows institutional maturity.' if age_int and age_int >= 50 else 'Institutional maturity should be reviewed against age criteria.'}"
    )

    engineering_analysis = (
        "Engineering programs are verified on the institution website."
        if engineering
        else "Engineering programs were not verified from the available report data."
    )

    management_analysis = (
        "MBA or management programs are verified on the institution website."
        if mba
        else "MBA or management programs were not verified from the available report data."
    )

    doctoral_analysis = (
        "Doctoral (PhD) programs are verified on the institution website."
        if phd
        else "Doctoral programs were not verified from the available report data."
    )

    leadership_analysis = (
        f"Leadership information identified: {leadership}."
        if leadership
        else "Leadership information was not available in the report."
    )

    confidence_assessment = (
        f"The institution received a confidence score of {confidence}/100 based on data completeness "
        f"including website, establishment year, program verification, leadership, and address fields."
    )

    eligibility_note = "meets" if eligible else "does not meet"
    executive_summary = (
        f"{name} {eligibility_note} qualification criteria with a confidence score of {confidence}/100. "
        f"Verified programs include "
        f"{', '.join(verified_programs) if verified_programs else 'none confirmed'}. "
        f"{'Vice Chancellor / leadership: ' + leadership + '.' if leadership else ''}"
    ).strip()

    return {
        "name": name,
        "state": state,
        "website": website,
        "established_year": year_int,
        "age": age_int,
        "engineering": engineering,
        "mba": mba,
        "phd": phd,
        "eligible": eligible,
        "vice_chancellor": leadership or None,
        "address": address or None,
        "confidence": confidence,
        "overview": overview,
        "academic_strengths": academic_strengths,
        "engineering_analysis": engineering_analysis,
        "management_analysis": management_analysis,
        "doctoral_analysis": doctoral_analysis,
        "leadership_analysis": leadership_analysis,
        "confidence_assessment": confidence_assessment,
        "executive_summary": executive_summary,
        "generated_by": "local_parser",
    }
