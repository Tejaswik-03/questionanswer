from fastapi import FastAPI, Query
import requests
from difflib import SequenceMatcher
import re
from typing import List, Dict, Optional

app = FastAPI(
    title="Member Question Answering API",
    description="Ask natural-language questions about members based on the public /messages API.",
    version="1.1.0",
)

API_URL = "https://november7-730026606190.europe-west1.run.app/messages"


# ---------- Helpers ----------

def fetch_items() -> List[Dict]:
    """
    Fetch the first page of messages. The API returns:
    { "total": <int>, "items": [ { "message": "...", "user_name": "...", "timestamp": "...", ... }, ... ] }
    """
    try:
        r = requests.get(API_URL, timeout=15)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and "items" in data and isinstance(data["items"], list):
            return [it for it in data["items"] if isinstance(it, dict) and "message" in it]
    except Exception as e:
        print("Error fetching items:", e)
    return []


def extract_name(question: str) -> Optional[str]:
    """
    Very simple name extractor: grabs 'First' or 'First Last' (capitalized words).
    Works for names like 'Layla', 'Vikram Desai', 'Amira', etc.
    """
    m = re.search(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\b", question)
    return m.group(1) if m else None


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def best_match(question: str, items: List[Dict], name: Optional[str]) -> Optional[Dict]:
    """
    Pick the item whose 'message' is most similar to the question.
    If a name is detected, give a small bonus when the item's user_name/message matches that name.
    """
    best = None
    best_score = 0.0
    q = question.strip()

    for it in items:
        msg = it.get("message", "")
        if not msg:
            continue
        score = similarity(q, msg)

        # small bonus if the name matches either the user_name or message text
        if name:
            uname = (it.get("user_name") or "").lower()
            if name.lower() in uname or name.lower() in msg.lower():
                score += 0.10  # bonus for name alignment

        if score > best_score:
            best_score = score
            best = it

    # threshold to avoid returning irrelevant text; tweak as needed
    if best and best_score >= 0.25:
        return best
    return None


# ---------- API ----------

@app.get("/ask")
def ask(question: str = Query(..., description="Ask a natural-language question about members.")):
    items = fetch_items()
    if not items:
        return {"answer": "Could not fetch data from the API."}

    name = extract_name(question)

    # If a name is present, try to pre-filter to items likely about that person.
    candidates = items
    if name:
        narrowed = [
            it for it in items
            if name.lower() in (it.get("user_name") or "").lower()
               or name.lower() in (it.get("message") or "").lower()
        ]
        if narrowed:
            candidates = narrowed

    winner = best_match(question, candidates, name)

    if winner:
        return {"answer": winner.get("message", "").strip()}

    return {"answer": "I couldn’t find a clear answer."}
