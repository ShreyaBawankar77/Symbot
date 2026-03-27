"""
SYMBOT - Main Chatbot (All 6 Steps Combined)
Symbiosis Institute of Technology, Nagpur
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Fix: Add the steps folder to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "steps")))

# Now import each step directly by filename (no package prefix needed)
from step2_preprocessing        import preprocess
from step3_synonym_aware        import synonym_match, FAQ_DB
from step4_tfidf_retrieval      import engine as tfidf_engine
from step5_intent_classification import classifier, INTENT_RESPONSES
from step6_entity_recognition   import extract_entities, enrich_response

BOT_NAME = "SymBot"
COLLEGE  = "Symbiosis Institute of Technology, Nagpur"
CONFIDENCE_THRESHOLD = 0.25


def greet() -> str:
    return (
        f"{'=' * 55}\n"
        f"  Welcome to {BOT_NAME}!\n"
        f"  {COLLEGE}\n"
        f"{'=' * 55}\n"
        f"I can help you with:\n"
        f"  - Admissions and Courses\n"
        f"  - Fees and Scholarships\n"
        f"  - Hostel and Canteen\n"
        f"  - Exams and Timetable\n"
        f"  - Placements and Library\n"
        f"  - Campus Facilities\n\n"
        f"Type 'exit' to quit  |  Type 'help' to see all topics\n"
    )


def respond(user_query: str) -> str:
    """
    Full pipeline:
    Step 2 -> Preprocess query
    Step 6 -> Extract entities
    Step 3 -> Synonym match  (fast path)
    Step 4 -> TF-IDF retrieval
    Step 5 -> Naive Bayes intent classification
    """

    # Empty input check
    if not user_query.strip():
        return "Please type something! I am here to help."

    # Special commands
    q_lower = user_query.lower().strip()
    if q_lower in ("help", "topics", "menu"):
        return (
            "Topics I can help with:\n"
            "  admissions, fees, timings, hostel, timetable,\n"
            "  scholarships, courses, placement, library,\n"
            "  exams, contact, canteen, wifi, faculty"
        )

    # ── Step 2: Preprocess ────────────────────────────────────
    tokens = preprocess(user_query)

    # ── Step 6: Extract entities ──────────────────────────────
    ents = extract_entities(user_query)

    # ── Step 3: Synonym match ─────────────────────────────────
    intent_from_synonym = synonym_match(tokens)
    if intent_from_synonym and intent_from_synonym in FAQ_DB:
        base = FAQ_DB[intent_from_synonym]["answer"]
        return enrich_response(base, ents)

    # ── Step 4: TF-IDF retrieval ──────────────────────────────
    tfidf_results = tfidf_engine.query(user_query, top_k=1)
    tfidf_score, _, tfidf_answer = tfidf_results[0]
    if tfidf_score >= 0.08:
        return enrich_response(tfidf_answer, ents)

    # ── Step 5: Naive Bayes intent classification ─────────────
    nb_intent, nb_answer, nb_conf = classifier.respond(user_query)
    if nb_conf >= CONFIDENCE_THRESHOLD:
        return enrich_response(nb_answer, ents)

    # ── Fallback ──────────────────────────────────────────────
    return (
        "I am not sure I understood that.\n"
        "Try keywords like: fees, admission, hostel, exam,\n"
        "placement, scholarship, timetable, canteen, wifi.\n"
        "Or visit: www.sitpune.edu.in"
    )


def main():
    print(greet())

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{BOT_NAME}: Goodbye! Visit us at SIT Nagpur.")
            break

        if user_input.lower() in ("exit", "quit", "bye", "goodbye"):
            print(f"\n{BOT_NAME}: Goodbye! Best of luck at SIT Nagpur.")
            break

        if not user_input:
            continue

        response = respond(user_input)
        print(f"\n{BOT_NAME}:\n{response}\n")


if __name__ == "__main__":
    main()