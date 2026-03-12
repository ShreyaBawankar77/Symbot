"""
SYMBOT - Step 1: Basic FAQ Responder
Symbiosis Institute of Technology, Nagpur
Rule-based chatbot answering 10-15 fixed institute FAQs using if-else / pattern matching
"""

import re

# ── Institute FAQ Database ──────────────────────────────────────────────────
FAQ_DB = {
    "timings": {
        "patterns": ["timing", "time", "hours", "open", "close", "schedule", "when"],
        "answer": (
            "🕘 Symbiosis Institute of Technology (SIT Nagpur) timings:\n"
            "  • College Hours  : 9:00 AM – 5:00 PM (Mon–Sat)\n"
            "  • Library        : 8:00 AM – 8:00 PM\n"
            "  • Admin Office   : 10:00 AM – 4:00 PM\n"
            "  • Saturday       : Half-day (till 1:00 PM)"
        ),
    },
    "fees": {
        "patterns": ["fee", "fees", "cost", "tuition", "payment", "charges", "expense", "pay"],
        "answer": (
            "💰 Fee Structure at SIT Nagpur:\n"
            "  • B.Tech (per year)  : ₹1,80,000 – ₹2,20,000 (branch-wise)\n"
            "  • M.Tech (per year)  : ₹1,50,000 – ₹1,80,000\n"
            "  • MBA (per year)     : ₹2,50,000\n"
            "  • Payment modes      : Online / DD / Demand Draft\n"
            "  • Last date          : Contact admissions office"
        ),
    },
    "contact": {
        "patterns": ["contact", "phone", "email", "address", "reach", "call", "number", "location"],
        "answer": (
            "📞 Contact SIT Nagpur:\n"
            "  • Address   : Survey No. 13/2, Maheshwari Colony, Wathoda Layout,\n"
            "                Nagpur, Maharashtra – 440008\n"
            "  • Phone     : +91-712-XXXXXXX\n"
            "  • Email     : admissions@sitpune.edu.in\n"
            "  • Website   : www.sitpune.edu.in"
        ),
    },
    "admissions": {
        "patterns": ["admission", "apply", "application", "enroll", "joining", "entrance", "jee", "cutoff"],
        "answer": (
            "🎓 Admissions at SIT Nagpur:\n"
            "  • B.Tech : via MHT-CET / JEE Main (CAP rounds)\n"
            "  • M.Tech : via GATE score\n"
            "  • MBA    : via MAH-MBA CET / CAT / MAT\n"
            "  • Documents: 10th & 12th marksheets, entrance scorecard,\n"
            "               Aadhaar, passport photo, category certificate (if any)"
        ),
    },
    "hostel": {
        "patterns": ["hostel", "accommodation", "stay", "room", "dorm", "pg", "boarding"],
        "answer": (
            "🏠 Hostel Facilities at SIT Nagpur:\n"
            "  • Separate hostels for boys and girls\n"
            "  • Amenities: Wi-Fi, mess, laundry, 24×7 security\n"
            "  • Hostel Fee (per year): ₹60,000 – ₹80,000\n"
            "  • Contact Hostel Warden: hostel@sitpune.edu.in"
        ),
    },
    "timetable": {
        "patterns": ["timetable", "class", "lecture", "period", "slot", "exam date", "syllabus"],
        "answer": (
            "📅 Timetable & Academics:\n"
            "  • Timetable is uploaded on the college ERP portal\n"
            "  • Login at: erp.sitpune.edu.in\n"
            "  • Exam schedule is shared 30 days before end-sem\n"
            "  • Lab sessions: As per departmental schedule"
        ),
    },
    "scholarships": {
        "patterns": ["scholarship", "merit", "financial aid", "waiver", "free", "discount", "stipend"],
        "answer": (
            "🏆 Scholarships at SIT Nagpur:\n"
            "  • Merit-based fee waiver for top 5 rankers\n"
            "  • Government: EBC, OBC, SC/ST scholarships available\n"
            "  • Sports quota: Extra benefits for state/national players\n"
            "  • Contact: scholarship@sitpune.edu.in"
        ),
    },
    "courses": {
        "patterns": ["course", "branch", "department", "program", "stream", "engineering", "btech", "mtech"],
        "answer": (
            "📚 Courses Offered at SIT Nagpur:\n"
            "  B.Tech: CS, IT, Mechanical, Civil, E&TC, AI&ML\n"
            "  M.Tech: CS, Mechanical, E&TC, Structural\n"
            "  MBA   : General, Marketing, Finance, HR\n"
            "  Also offers PhD programs"
        ),
    },
    "placement": {
        "patterns": ["placement", "job", "recruit", "company", "campus", "hire", "salary", "package"],
        "answer": (
            "💼 Placement at SIT Nagpur:\n"
            "  • Highest CTC    : ₹12 LPA\n"
            "  • Average CTC    : ₹5.5 LPA\n"
            "  • Top Recruiters : TCS, Infosys, Wipro, Cognizant, L&T\n"
            "  • Placement Cell : placement@sitpune.edu.in"
        ),
    },
    "library": {
        "patterns": ["library", "book", "journal", "read", "borrow", "digital", "e-library"],
        "answer": (
            "📖 Library at SIT Nagpur:\n"
            "  • 20,000+ books and 5,000+ e-journals\n"
            "  • NPTEL & DELNET access available\n"
            "  • Timings: 8:00 AM – 8:00 PM\n"
            "  • Digital Library: Open 24×7 via college portal"
        ),
    },
    "exam": {
        "patterns": ["exam", "test", "assessment", "result", "mark", "grade", "paper", "recheck"],
        "answer": (
            "📝 Examination Details:\n"
            "  • Mid-sem  : 7th–8th week of each semester\n"
            "  • End-sem  : Last 2 weeks of semester\n"
            "  • Results  : Published within 30 days on ERP portal\n"
            "  • Revaluation requests: Within 7 days of result\n"
            "  • ATKT policy as per Savitribai Phule Pune University norms"
        ),
    },
    "principal": {
        "patterns": ["principal", "director", "hod", "dean", "professor", "faculty", "staff"],
        "answer": (
            "👨‍💼 Administration at SIT Nagpur:\n"
            "  • Director     : Contact admin office for current details\n"
            "  • HOD meetings : By appointment via department office\n"
            "  • Faculty list : Available on college website\n"
            "  • Grievance    : grievance@sitpune.edu.in"
        ),
    },
    "canteen": {
        "patterns": ["canteen", "food", "cafeteria", "mess", "eat", "meal", "lunch"],
        "answer": (
            "🍽️ Canteen & Mess:\n"
            "  • Main Canteen : 8:00 AM – 6:00 PM (veg & non-veg)\n"
            "  • Mess (hostel): Breakfast 7–9 AM, Lunch 12–2 PM, Dinner 7–9 PM\n"
            "  • Monthly mess charges: ~₹3,500"
        ),
    },
    "wifi": {
        "patterns": ["wifi", "internet", "network", "connectivity", "broadband", "online"],
        "answer": (
            "📶 Internet Facility:\n"
            "  • Campus-wide Wi-Fi (NKN connected)\n"
            "  • Speed: 1 Gbps leased line\n"
            "  • Login with your college credentials\n"
            "  • IT helpdesk: it@sitpune.edu.in"
        ),
    },
    "default": {
        "patterns": [],
        "answer": (
            "🤖 Hi! I'm SymBot — your assistant for SIT Nagpur.\n"
            "I can answer questions about:\n"
            "  timings, fees, admissions, hostel, timetable,\n"
            "  scholarships, courses, placements, library,\n"
            "  exams, faculty, canteen, wifi\n\n"
            "Please rephrase or type a keyword!"
        ),
    },
}


def match_faq(user_input: str) -> str:
    """Pattern-match the user query against FAQ keys and return best answer."""
    query = user_input.lower().strip()
    query = re.sub(r"[^\w\s]", " ", query)   # remove punctuation

    for key, data in FAQ_DB.items():
        if key == "default":
            continue
        for pattern in data["patterns"]:
            if pattern in query:
                return data["answer"]

    return FAQ_DB["default"]["answer"]


# ── REPL ────────────────────────────────────────────────────────────────────
def run_bot():
    print("=" * 60)
    print("   SYMBOT — Symbiosis Institute of Technology, Nagpur")
    print("   Step 1: Basic FAQ Responder (Rule-Based)")
    print("=" * 60)
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "bye"):
            print("SymBot: Goodbye! 👋")
            break
        response = match_faq(user_input)
        print(f"\nSymBot:\n{response}\n")


if __name__ == "__main__":
    run_bot()