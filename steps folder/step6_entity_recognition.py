"""
SYMBOT - Step 6: Entity Recognition
Symbiosis Institute of Technology, Nagpur
Extracts dates, course codes, department names, roll numbers, and key entities from queries
"""

import re
from dataclasses import dataclass, field

@dataclass
class Entities:
    dates:        list[str] = field(default_factory=list)
    course_codes: list[str] = field(default_factory=list)
    departments:  list[str] = field(default_factory=list)
    roll_numbers: list[str] = field(default_factory=list)
    semesters:    list[str] = field(default_factory=list)
    years:        list[str] = field(default_factory=list)
    amounts:      list[str] = field(default_factory=list)
    emails:       list[str] = field(default_factory=list)
    phone_numbers:list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v}

    def summary(self) -> str:
        parts = []
        if self.dates:         parts.append(f"📅 Dates: {', '.join(self.dates)}")
        if self.course_codes:  parts.append(f"📘 Course Codes: {', '.join(self.course_codes)}")
        if self.departments:   parts.append(f"🏛️ Departments: {', '.join(self.departments)}")
        if self.roll_numbers:  parts.append(f"🆔 Roll Numbers: {', '.join(self.roll_numbers)}")
        if self.semesters:     parts.append(f"📆 Semesters: {', '.join(self.semesters)}")
        if self.years:         parts.append(f"📅 Years: {', '.join(self.years)}")
        if self.amounts:       parts.append(f"💰 Amounts: {', '.join(self.amounts)}")
        if self.emails:        parts.append(f"📧 Emails: {', '.join(self.emails)}")
        if self.phone_numbers: parts.append(f"📞 Phones: {', '.join(self.phone_numbers)}")
        return "\n".join(parts) if parts else "No entities found."


# ── Entity Patterns ─────────────────────────────────────────────────────────

DATE_PATTERNS = [
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",           # 12/05/2024 or 12-05-24
    r"\b\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s\d{2,4}\b",
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s\d{1,2},?\s\d{4}\b",
    r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    r"\b(?:today|tomorrow|yesterday|next week|last week|this month)\b",
    r"\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s\d{4}\b",
]

# Course codes like CS201, IT302, ME101, CS-501, BTCS301
COURSE_CODE_PATTERN = r"\b(?:CS|IT|ME|CE|ET|EC|AI|ML|MB|BT|EE|CH|MCA)\s?[-]?\s?\d{3,4}\b"

DEPARTMENT_KEYWORDS = {
    "computer science":    "CS", "computer engineering":  "CS",
    "information technology": "IT",
    "mechanical":          "ME", "mechanical engineering": "ME",
    "civil":               "CE", "civil engineering":      "CE",
    "electronics":         "EC", "e&tc":                   "EC",
    "electrical":          "EE", "electrical engineering": "EE",
    "ai":                  "AI", "artificial intelligence": "AI",
    "machine learning":    "ML", "data science":            "ML",
    "mba":                 "MBA", "management":             "MBA",
    "chemical":            "CH", "chemical engineering":   "CH",
}

# Roll numbers like 2021BTCS045, SIT2022IT023
ROLL_NUMBER_PATTERN = r"\b(?:SIT)?20\d{2}(?:BT|MT|MBA)?(?:CS|IT|ME|CE|EC|AI|ML|EE|CH)\d{3}\b"

SEMESTER_PATTERN = r"\b(?:sem(?:ester)?[-\s]?[1-8]|[1-8](?:st|nd|rd|th)\s?sem(?:ester)?)\b"

YEAR_PATTERN = r"\b20[12]\d\b"

AMOUNT_PATTERN = r"(?:₹|rs\.?|inr)\s?\d[\d,]*(?:\.\d{2})?|\b\d[\d,]+\s?(?:lakh|lakhs|lac|k|thousand|rupees)\b"

EMAIL_PATTERN = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}\b"

PHONE_PATTERN = r"\b(?:\+91[\s-]?)?[6-9]\d{9}\b|\b0\d{2,4}[\s-]\d{6,8}\b"


def extract_entities(text: str) -> Entities:
    ents = Entities()
    t = text.lower()

    # Dates
    for pat in DATE_PATTERNS:
        ents.dates.extend(re.findall(pat, t, re.IGNORECASE))
    ents.dates = list(dict.fromkeys(ents.dates))  # deduplicate preserving order

    # Course codes
    ents.course_codes = list(set(re.findall(COURSE_CODE_PATTERN, text, re.IGNORECASE)))

    # Departments
    found_depts = []
    for keyword, code in DEPARTMENT_KEYWORDS.items():
        if keyword in t and code not in found_depts:
            found_depts.append(code)
    ents.departments = found_depts

    # Roll numbers
    ents.roll_numbers = list(set(re.findall(ROLL_NUMBER_PATTERN, text, re.IGNORECASE)))

    # Semesters
    ents.semesters = list(set(re.findall(SEMESTER_PATTERN, t, re.IGNORECASE)))

    # Years
    ents.years = list(set(re.findall(YEAR_PATTERN, text)))

    # Amounts
    ents.amounts = list(set(re.findall(AMOUNT_PATTERN, t, re.IGNORECASE)))

    # Emails
    ents.emails = list(set(re.findall(EMAIL_PATTERN, text)))

    # Phone numbers
    ents.phone_numbers = list(set(re.findall(PHONE_PATTERN, text)))

    return ents


def enrich_response(base_response: str, ents: Entities) -> str:
    """Append extracted entity context to a base response."""
    entity_summary = ents.summary()
    if entity_summary == "No entities found.":
        return base_response
    return (
        f"{base_response}\n\n"
        f"📌 Detected in your query:\n{entity_summary}"
    )


# ── REPL ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_queries = [
        "I have exam for CS301 on 15/11/2024, what should I do?",
        "My roll number is 2022BTCS045 and I need scholarship info",
        "Fee for mechanical engineering in 3rd semester 2023?",
        "Contact admissions@sitpune.edu.in for joining form before January 2025",
        "The course code for AI is AI501 in 5th sem, when is the paper?",
        "I want ₹50,000 scholarship for SIT Nagpur civil branch",
        "Reach us at +919876543210 or visit on Monday",
        "How much is the fee for MBA program in 2024?",
    ]

    print("=" * 60)
    print("   SYMBOT — Step 6: Entity Recognition")
    print("=" * 60)

    for q in test_queries:
        ents = extract_entities(q)
        print(f"\n🔹 Query   : {q}")
        print(f"   Entities:\n   {ents.summary().replace(chr(10), chr(10)+'   ')}")
        