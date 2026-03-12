"""
SYMBOT - Step 4: FAQ Retrieval with TF-IDF
Symbiosis Institute of Technology, Nagpur
Stores FAQs as documents, uses TF-IDF cosine similarity to pick best answer
"""

import math
import re
from collections import Counter

# ── Inline preprocessing (no external deps) ────────────────────────────────
STOP = {
    "i","me","my","we","our","you","your","he","him","she","her","it","its",
    "they","their","what","which","who","this","that","these","those","am","is",
    "are","was","were","be","been","have","has","had","do","does","did","will",
    "would","shall","should","may","might","can","could","a","an","the","and",
    "but","if","or","as","of","at","by","for","with","about","to","from","in",
    "on","how","when","where","why","please","tell","want","need","get","hi",
    "hello","hey","sir","madam",
}

def tokenize(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return [t for t in text.split() if t not in STOP and len(t) > 1]


# ── FAQ Corpus  (question → answer) ────────────────────────────────────────
FAQ_CORPUS = [
    ("What are the college timings and office hours?",
     "🕘 College: 9AM–5PM Mon–Sat | Library: 8AM–8PM | Admin: 10AM–4PM"),

    ("What is the fee structure and tuition payment schedule?",
     "💰 B.Tech: ₹1.8L–₹2.2L/yr | M.Tech: ₹1.5L–₹1.8L/yr | MBA: ₹2.5L/yr. Online/DD payment accepted."),

    ("How to apply for admission and what are eligibility criteria?",
     "🎓 B.Tech via MHT-CET/JEE Main | M.Tech via GATE | MBA via MAH-CET/CAT. Docs: 10th 12th marksheets, entrance scorecard, Aadhaar."),

    ("What hostel and accommodation facilities are available?",
     "🏠 Separate boys & girls hostels | Wi-Fi, mess, laundry | ₹60K–₹80K/yr. Contact: hostel@sitpune.edu.in"),

    ("How do I find the class timetable and exam schedule?",
     "📅 Timetable on ERP portal: erp.sitpune.edu.in | Exam schedule released 30 days before end-sem."),

    ("Are there scholarships or financial aid for students?",
     "🏆 Merit-based fee waiver, EBC/OBC/SC-ST govt scholarships, sports quota benefits. Contact: scholarship@sitpune.edu.in"),

    ("What engineering courses and programs are offered?",
     "📚 B.Tech: CS, IT, Mechanical, Civil, E&TC, AI&ML | M.Tech & MBA also offered | PhD programs available."),

    ("What is the placement record and which companies recruit?",
     "💼 Highest: ₹12 LPA | Average: ₹5.5 LPA | Recruiters: TCS, Infosys, Wipro, L&T, Cognizant."),

    ("What library resources and books are available?",
     "📖 20,000+ books, 5,000+ e-journals | NPTEL & DELNET access | Timings: 8AM–8PM | Digital library 24×7."),

    ("When are the mid-sem and end-sem exams and how is grading done?",
     "📝 Mid-sem: Week 7–8 | End-sem: Last 2 weeks | Results in 30 days | Revaluation within 7 days of result."),

    ("What is the contact address phone and email of the institute?",
     "📞 Address: Wathoda Layout, Nagpur 440008 | Email: admissions@sitpune.edu.in | Website: www.sitpune.edu.in"),

    ("What is available in the canteen and mess timings?",
     "🍽️ Canteen: 8AM–6PM (veg & non-veg) | Mess: Breakfast 7–9AM, Lunch 12–2PM, Dinner 7–9PM | ₹3,500/month."),

    ("What is the wifi and internet speed on campus?",
     "📶 Campus Wi-Fi (1 Gbps NKN) | Login with college credentials | IT helpdesk: it@sitpune.edu.in"),

    ("How can I meet the principal director or HOD faculty?",
     "👨‍💼 HOD meetings by appointment via dept office | Faculty list on college website | Grievance: grievance@sitpune.edu.in"),
]


# ── TF-IDF Engine ───────────────────────────────────────────────────────────
class TFIDF:
    def __init__(self, corpus: list[tuple[str, str]]):
        self.corpus    = corpus
        self.questions = [q for q, _ in corpus]
        self.answers   = [a for _, a in corpus]
        self.tokenized = [tokenize(q) for q in self.questions]
        self.vocab     = sorted({t for doc in self.tokenized for t in doc})
        self._build_matrix()

    def _tf(self, tokens: list[str]) -> dict[str, float]:
        count = Counter(tokens)
        total = len(tokens) or 1
        return {w: c / total for w, c in count.items()}

    def _build_matrix(self):
        N = len(self.tokenized)
        # IDF: log((N+1) / (df+1)) + 1
        df = Counter()
        for doc in self.tokenized:
            for w in set(doc):
                df[w] += 1
        self.idf = {w: math.log((N + 1) / (df[w] + 1)) + 1 for w in self.vocab}
        # TF-IDF vectors
        self.vectors = []
        for doc in self.tokenized:
            tf = self._tf(doc)
            vec = [tf.get(w, 0) * self.idf.get(w, 0) for w in self.vocab]
            self.vectors.append(vec)

    def _cosine(self, a: list[float], b: list[float]) -> float:
        dot  = sum(x * y for x, y in zip(a, b))
        norm = (math.sqrt(sum(x**2 for x in a)) *
                math.sqrt(sum(y**2 for y in b)))
        return dot / norm if norm else 0.0

    def query(self, raw_query: str, top_k: int = 3) -> list[tuple[float, str, str]]:
        tokens = tokenize(raw_query)
        tf = self._tf(tokens)
        qvec = [tf.get(w, 0) * self.idf.get(w, 0) for w in self.vocab]
        scores = [(self._cosine(qvec, dvec), self.questions[i], self.answers[i])
                  for i, dvec in enumerate(self.vectors)]
        scores.sort(reverse=True, key=lambda x: x[0])
        return scores[:top_k]

    def best_answer(self, raw_query: str, threshold: float = 0.05) -> str:
        results = self.query(raw_query, top_k=1)
        score, _, answer = results[0]
        if score >= threshold:
            return answer
        return "❓ I'm not sure about that. Please visit the admin office or call us directly."


# ── Singleton engine ────────────────────────────────────────────────────────
engine = TFIDF(FAQ_CORPUS)


# ── REPL ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_queries = [
        "I want to know tuition charges",
        "Where can I stay near campus?",
        "Is there any merit scholarship?",
        "When do exams happen?",
        "Do TCS and Infosys come for campus drive?",
        "What books are in the library?",
        "I need WiFi password",
        "Can I meet the department head?",
        "What food is available in college?",
    ]

    print("=" * 60)
    print("   SYMBOT — Step 4: TF-IDF Retrieval Engine")
    print("=" * 60)
    for q in test_queries:
        top3 = engine.query(q, top_k=3)
        print(f"\n🔹 Query : {q}")
        for rank, (score, matched_q, ans) in enumerate(top3, 1):
            print(f"   #{rank} [{score:.3f}] Matched: {matched_q[:55]}...")
        best = engine.best_answer(q)
        print(f"   ✅ Best Answer: {best[:80]}...")
        