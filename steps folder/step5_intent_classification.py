"""
SYMBOT - Step 5: Intent Classification for Queries
Symbiosis Institute of Technology, Nagpur
7 intents — Naive Bayes classifier routes queries to correct intent bucket
"""

import math, re
from collections import defaultdict, Counter

# ── Intents & Training Data ─────────────────────────────────────────────────
INTENT_SAMPLES = {
    "admissions": [
        "How do I apply for admission?",
        "What is the admission procedure?",
        "What documents are needed for joining?",
        "Tell me about enrollment process",
        "What is the JEE cutoff for CS branch?",
        "How to fill the application form?",
        "Is there any entrance exam?",
        "What is eligibility for B.Tech admission?",
        "When does admission start?",
        "How do I register for MHT-CET counselling?",
        "What is the last date of application?",
        "I want to take admission in mechanical engineering",
    ],
    "exams": [
        "When is the mid-sem exam?",
        "What is the timetable for end-semester?",
        "How do I apply for revaluation?",
        "What happens if I get ATKT?",
        "Where can I find my exam results?",
        "What are the grading rules?",
        "How is the internal assessment calculated?",
        "When will results be declared?",
        "How to apply for backlog exam?",
        "What is the passing criteria?",
        "Can I see my answer sheet?",
        "What are the exam fees for supplementary?",
    ],
    "timetable": [
        "Where can I find the class schedule?",
        "What is today's timetable?",
        "How do I access the ERP portal?",
        "Is there a lecture on Saturday?",
        "What are the lab timings?",
        "When is the practical session?",
        "Which slot is free on Tuesday?",
        "How many periods are in a day?",
        "What is the weekly class routine?",
        "When is the next seminar?",
    ],
    "hostel": [
        "Is hostel available for boys?",
        "What are the hostel charges?",
        "Tell me about girls hostel facility",
        "Is mess included in hostel fee?",
        "What is the warden contact number?",
        "Can I stay in hostel from day one?",
        "What accommodation options are available?",
        "Is wifi available in hostel rooms?",
        "Tell me about PG near campus",
        "What are the hostel rules?",
        "Is laundry service available in hostel?",
    ],
    "scholarships": [
        "Are there any scholarships for merit students?",
        "I come from OBC category, any scholarship?",
        "How do I apply for financial aid?",
        "Is fee waiver available for toppers?",
        "What government scholarships are available?",
        "Tell me about SC ST scholarship",
        "Is there any sports scholarship?",
        "How much scholarship can I get?",
        "Is EBC freeship available here?",
        "What is the process for scholarship application?",
    ],
    "placement": [
        "Which companies come for campus placement?",
        "What is the average salary package?",
        "When does the placement season start?",
        "Did TCS visit campus this year?",
        "How do I register for placement drive?",
        "Is internship counted as placement?",
        "What is the highest CTC offered?",
        "Which branch gets best placement?",
        "Tell me about placement statistics",
        "How many students got placed last year?",
        "Do companies visit for off-campus drives?",
    ],
    "general_info": [
        "What is the contact number of the college?",
        "What are the college timings?",
        "Where is SIT Nagpur located?",
        "What courses does the college offer?",
        "How is the wifi on campus?",
        "What is available in the canteen?",
        "Who is the director of the college?",
        "What is the college website?",
        "Tell me about library facilities",
        "What sports facilities are available?",
        "What is the campus size?",
        "How do I reach the college by bus?",
    ],
}

INTENTS = list(INTENT_SAMPLES.keys())

# ── Responses per intent ────────────────────────────────────────────────────
INTENT_RESPONSES = {
    "admissions":   "🎓 For admissions, visit the Admissions Office or go to erp.sitpune.edu.in. Required: MHT-CET/JEE score, 10th & 12th marksheets, Aadhaar, and category certificate.",
    "exams":        "📝 Exam schedules are on the ERP portal. Mid-sem: Week 7–8 | End-sem: last 2 weeks. Results in 30 days. Apply for revaluation within 7 days.",
    "timetable":    "📅 Class timetables are on the ERP portal: erp.sitpune.edu.in. Log in with your college credentials to view your semester schedule.",
    "hostel":       "🏠 Separate boys & girls hostels with Wi-Fi, mess, laundry. Fee: ₹60K–₹80K/yr. Contact: hostel@sitpune.edu.in or the hostel warden directly.",
    "scholarships": "🏆 Scholarships: Merit-based fee waivers, EBC/OBC/SC-ST government scholarships, sports quota. Apply at scholarship@sitpune.edu.in.",
    "placement":    "💼 Placement: Highest ₹12 LPA | Average ₹5.5 LPA | Recruiters: TCS, Infosys, Wipro, L&T, Cognizant. Register at the placement cell.",
    "general_info": "ℹ️ SIT Nagpur | Address: Wathoda Layout, Nagpur 440008 | Timings: 9AM–5PM | Email: admissions@sitpune.edu.in | Web: www.sitpune.edu.in",
}


# ── Naive Bayes Classifier ──────────────────────────────────────────────────
STOP = {"i","me","my","we","our","you","your","he","him","it","its","they","their",
        "what","which","who","this","that","is","are","was","were","be","been",
        "have","has","do","does","a","an","the","and","but","if","or","of","at",
        "by","for","with","to","from","in","on","how","when","where","please",
        "tell","want","need","get","hi","hello","hey","sir","madam","about","any"}

def tokenize(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return [t for t in text.split() if t not in STOP and len(t) > 1]


class NaiveBayesClassifier:
    def __init__(self):
        self.class_word_counts   = defaultdict(Counter)
        self.class_totals        = Counter()
        self.class_doc_counts    = Counter()
        self.vocab               = set()
        self.total_docs          = 0

    def train(self, samples: dict[str, list[str]]):
        for label, sentences in samples.items():
            for sentence in sentences:
                tokens = tokenize(sentence)
                self.class_word_counts[label].update(tokens)
                self.class_totals[label]   += len(tokens)
                self.class_doc_counts[label] += 1
                self.vocab.update(tokens)
                self.total_docs += 1
        print(f"[NaiveBayes] Trained on {self.total_docs} samples | "
              f"{len(self.vocab)} vocab | {len(samples)} intents")

    def predict(self, text: str) -> tuple[str, dict[str, float]]:
        tokens = tokenize(text)
        V      = len(self.vocab)
        scores = {}

        for label in INTENTS:
            # Log prior
            prior = math.log(self.class_doc_counts[label] / self.total_docs)
            # Log likelihood with Laplace smoothing
            log_likelihood = 0.0
            total = self.class_totals[label]
            for token in tokens:
                count = self.class_word_counts[label].get(token, 0)
                log_likelihood += math.log((count + 1) / (total + V))
            scores[label] = prior + log_likelihood

        best_intent = max(scores, key=scores.get)
        # Convert log scores to pseudo-probabilities via softmax
        max_s = max(scores.values())
        exp_scores = {k: math.exp(v - max_s) for k, v in scores.items()}
        total_exp  = sum(exp_scores.values())
        probs = {k: v / total_exp for k, v in exp_scores.items()}

        return best_intent, probs

    def respond(self, text: str) -> tuple[str, str, float]:
        intent, probs = self.predict(text)
        answer = INTENT_RESPONSES.get(intent, "Please contact the admin office.")
        confidence = probs[intent]
        return intent, answer, confidence


# ── Singleton ────────────────────────────────────────────────────────────────
classifier = NaiveBayesClassifier()
classifier.train(INTENT_SAMPLES)


# ── REPL ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_queries = [
        "I want to take admission in CSE branch",
        "When will the semester results be out?",
        "Is boys hostel available?",
        "What is the fee waiver for toppers?",
        "Which IT companies visit campus?",
        "What is the class schedule for Monday?",
        "How do I contact the college?",
        "What is the JEE cutoff for admission?",
        "I need scholarship for economically weak students",
        "Is TCS coming for placement this year?",
    ]

    print("=" * 65)
    print("   SYMBOT — Step 5: Intent Classification (Naive Bayes)")
    print("=" * 65)

    for q in test_queries:
        intent, answer, conf = classifier.respond(q)
        print(f"\n🔹 Query      : {q}")
        print(f"   Intent     : {intent}  (confidence: {conf:.1%})")
        print(f"   Response   : {answer[:80]}...")
        