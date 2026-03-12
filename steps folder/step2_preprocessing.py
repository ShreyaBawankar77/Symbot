"""
SYMBOT - Step 2: Preprocessing Student Queries
Symbiosis Institute of Technology, Nagpur
Lowercasing, tokenization, stopword removal, punctuation handling, spelling normalization
"""

import re
import string
from difflib import get_close_matches

# ── Stopwords (light English set, no NLTK needed) ──────────────────────────
STOP_WORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "he", "him", "his", "she", "her", "hers", "it", "its",
    "they", "them", "their", "theirs", "what", "which", "who", "whom", "this",
    "that", "these", "those", "am", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "a", "an", "the", "and",
    "but", "if", "or", "because", "as", "until", "of", "at", "by", "for", "with",
    "about", "into", "through", "to", "from", "in", "on", "up", "out", "so",
    "than", "too", "very", "just", "how", "when", "where", "why", "please", "tell",
    "me", "know", "want", "need", "get", "give", "let", "hi", "hello", "hey",
    "sir", "mam", "madam", "dear", "bot", "symbot",
}

# ── Common typo corrections (domain-specific) ──────────────────────────────
SPELLING_CORRECTIONS = {
    "fess": "fees", "fee": "fees", "feees": "fees",
    "addmission": "admission", "addmissions": "admissions", "admmission": "admission",
    "hostle": "hostel", "hostil": "hostel",
    "exem": "exam", "exams": "exam", "eaxm": "exam",
    "timetble": "timetable", "time table": "timetable", "time-table": "timetable",
    "scolarship": "scholarship", "scholrship": "scholarship",
    "placment": "placement", "placements": "placement",
    "libraray": "library", "libary": "library",
    "timeing": "timing", "tiiming": "timing",
    "cource": "course", "cources": "courses", "coarse": "course",
    "cannteen": "canteen", "cantine": "canteen",
    "wifii": "wifi", "wi fi": "wifi", "wi-fi": "wifi",
    "principel": "principal", "principall": "principal",
    "recuiter": "recruiter", "recuitment": "recruitment",
}

VOCAB = list(SPELLING_CORRECTIONS.keys()) + list(SPELLING_CORRECTIONS.values())


def lowercase(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()


def remove_punctuation(text: str) -> str:
    """Remove punctuation characters."""
    # Keep apostrophes inside words (e.g., "what's" → "whats")
    text = re.sub(r"[^\w\s]", " ", text)
    return text


def tokenize(text: str) -> list[str]:
    """Simple whitespace tokenizer."""
    return text.split()


def remove_stopwords(tokens: list[str]) -> list[str]:
    """Filter out stopwords from token list."""
    return [t for t in tokens if t not in STOP_WORDS]


def correct_spelling(tokens: list[str]) -> list[str]:
    """Apply domain-specific spelling corrections."""
    corrected = []
    for token in tokens:
        # Direct lookup
        if token in SPELLING_CORRECTIONS:
            corrected.append(SPELLING_CORRECTIONS[token])
        else:
            # Fuzzy closest match (cutoff 0.82 to avoid false positives)
            matches = get_close_matches(token, VOCAB, n=1, cutoff=0.82)
            if matches:
                match = matches[0]
                corrected.append(SPELLING_CORRECTIONS.get(match, match))
            else:
                corrected.append(token)
    return corrected


def normalize(tokens: list[str]) -> list[str]:
    """Remove very short tokens (length <= 1) and digits-only tokens."""
    return [t for t in tokens if len(t) > 1 and not t.isdigit()]


def preprocess(raw_text: str, verbose: bool = False) -> list[str]:
    """Full preprocessing pipeline → returns clean token list."""
    step_lower  = lowercase(raw_text)
    step_nopunc = remove_punctuation(step_lower)
    step_tokens = tokenize(step_nopunc)
    step_nostop = remove_stopwords(step_tokens)
    step_spell  = correct_spelling(step_nostop)
    step_final  = normalize(step_spell)

    if verbose:
        print(f"  Original  : {raw_text}")
        print(f"  Lowercase : {step_lower}")
        print(f"  No Punct  : {step_nopunc}")
        print(f"  Tokens    : {step_tokens}")
        print(f"  No Stop   : {step_nostop}")
        print(f"  Spelling  : {step_spell}")
        print(f"  Final     : {step_final}")

    return step_final


def preprocess_to_string(raw_text: str) -> str:
    """Preprocess and return as joined string (useful for matching)."""
    return " ".join(preprocess(raw_text))


# ── Demo ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_queries = [
        "Hello! Can you tell me about the fess structure??",
        "What are the addmission requirements for B.Tech?",
        "Hi sir, I want to know about hostle facilities.",
        "please tell me the timetble for this semester",
        "I need info on scolarship for SC students!",
        "What's the wifii speed in campus???",
    ]

    print("=" * 60)
    print("   SYMBOT — Step 2: Preprocessing Pipeline Demo")
    print("=" * 60)
    for q in test_queries:
        print(f"\n{'─'*55}")
        tokens = preprocess(q, verbose=True)
        print(f"  Joined    : '{' '.join(tokens)}'")
    print("\n" + "=" * 60)