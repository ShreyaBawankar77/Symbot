"""
SYMBOT - Step 3: Synonym-Aware FAQ Bot
Symbiosis Institute of Technology, Nagpur
Semantically similar queries map to same answer via synonym dictionary / keyword groups
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from step1_basic_faq import FAQ_DB
from step2_preprocessing import preprocess

# ── Synonym / Keyword groups ────────────────────────────────────────────────
# Each intent key maps to an exhaustive synonym cluster.
# All words in a cluster resolve to the SAME FAQ_DB entry.

SYNONYM_GROUPS = {
    "fees": [
        "fees", "fee", "tuition", "payment", "charges", "cost", "expense",
        "money", "amount", "price", "pay", "paying", "afford", "fund",
        "installment", "dues", "pending", "deposit",
    ],
    "timings": [
        "timings", "timing", "time", "hours", "open", "close", "schedule",
        "when", "working", "office hours", "college hours", "start", "end",
        "morning", "evening", "shift",
    ],
    "admissions": [
        "admission", "admissions", "apply", "application", "applying",
        "enroll", "enrollment", "join", "joining", "entrance", "jee", "cet",
        "cutoff", "merit", "registration", "form", "document", "eligibility",
        "criteria", "seat", "seats", "intake",
    ],
    "hostel": [
        "hostel", "accommodation", "stay", "room", "dorm", "dormitory",
        "pg", "paying guest", "boarding", "lodge", "lodging", "rent",
        "residential", "warden", "mess", "housing",
    ],
    "timetable": [
        "timetable", "timetables", "class", "classes", "lecture", "lectures",
        "period", "slot", "slots", "routine", "schedule", "period",
        "lab", "practical", "session", "daily", "weekly",
    ],
    "scholarships": [
        "scholarship", "scholarships", "merit", "financial aid", "waiver",
        "free", "discount", "stipend", "grant", "bursary", "fellowship",
        "sponsored", "freeship", "ebc", "obc",
    ],
    "courses": [
        "course", "courses", "branch", "branches", "department", "departments",
        "program", "programmes", "stream", "engineering", "btech", "mtech",
        "mba", "specialization", "subjects", "curriculum",
    ],
    "placement": [
        "placement", "placements", "job", "jobs", "recruit", "recruitment",
        "company", "companies", "campus", "hire", "hiring", "salary",
        "package", "ctc", "internship", "intern", "offer", "letter",
        "drive", "career",
    ],
    "library": [
        "library", "book", "books", "journal", "journals", "read", "reading",
        "borrow", "digital", "e-library", "delnet", "nptel", "resource",
        "reference", "periodical", "magazine",
    ],
    "exam": [
        "exam", "exams", "test", "tests", "assessment", "result", "results",
        "mark", "marks", "grade", "grades", "paper", "papers", "recheck",
        "revaluation", "backlog", "atkt", "supply", "semester", "end-sem",
        "mid-sem", "internal",
    ],
    "contact": [
        "contact", "phone", "email", "address", "reach", "call", "number",
        "location", "helpline", "enquiry", "inquiry", "website", "portal",
        "map", "direction",
    ],
    "canteen": [
        "canteen", "food", "cafeteria", "meal", "meals", "lunch", "dinner",
        "breakfast", "eat", "eating", "drink", "snack", "vendor", "tuck",
    ],
    "wifi": [
        "wifi", "internet", "network", "connectivity", "broadband", "online",
        "connection", "speed", "bandwidth", "lan", "hotspot",
    ],
    "principal": [
        "principal", "director", "hod", "head", "dean", "faculty", "professor",
        "staff", "teacher", "coordinator", "administration", "admin",
    ],
}

# Build a flat word → intent mapping for O(1) lookup
WORD_TO_INTENT: dict[str, str] = {}
for intent, synonyms in SYNONYM_GROUPS.items():
    for word in synonyms:
        WORD_TO_INTENT[word] = intent


def synonym_match(tokens: list[str]) -> str | None:
    """Return the first matched intent for a token list, else None."""
    for token in tokens:
        if token in WORD_TO_INTENT:
            return WORD_TO_INTENT[token]
    return None


def respond(raw_query: str) -> str:
    """Preprocess query → synonym-match → return FAQ answer."""
    tokens = preprocess(raw_query)
    intent = synonym_match(tokens)
    if intent and intent in FAQ_DB:
        return FAQ_DB[intent]["answer"]
    return FAQ_DB["default"]["answer"]


# ── REPL ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_queries = [
        "What is the tuition amount for first year?",        # → fees
        "How much money do I need to pay for admission?",    # → fees
        "Is there any financial aid available?",             # → scholarships
        "I want to know about the internship opportunities", # → placement
        "Tell me about career and hiring drive",             # → placement
        "What are the working hours of the college?",        # → timings
        "Can I get info on dormitory facility?",             # → hostel
        "How can I contact the administration?",             # → contact/principal
        "When is the end-sem exam scheduled?",               # → exam
    ]

    print("=" * 60)
    print("   SYMBOT — Step 3: Synonym-Aware FAQ Bot")
    print("=" * 60)

    for q in test_queries:
        tokens = preprocess(q)
        intent = synonym_match(tokens)
        ans    = respond(q)
        print(f"\n🔹 Query  : {q}")
        print(f"   Tokens : {tokens}")
        print(f"   Intent : {intent or 'unknown'}")
        print(f"   Answer : {ans[:80]}...")
        