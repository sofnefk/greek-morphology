import csv
import unicodedata
from collections import defaultdict

import spacy

MODELS = ["el_core_news_sm", "el_core_news_lg"]
TEST_FILE = "data/test_set.csv"


def nfc(s):
    """Unicode NFC only. Keeps case. This is what the model sees."""
    return unicodedata.normalize("NFC", s).strip()


def norm(s):
    """NFC + lowercase. ONLY for comparing strings, never for model input."""
    return nfc(s).lower()


def load_test_set(path):
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            row["accepted"] = {norm(x) for x in row["accepted_lemmas"].split("|")}
            rows.append(row)
    return rows


test_set = load_test_set(TEST_FILE)
print(f"Loaded {len(test_set)} test rows")

for model_name in MODELS:
    try:
        nlp = spacy.load(model_name)
    except OSError:
        print(f"\n!! {model_name} not installed, skipping")
        continue

    print(f"\n===== {model_name} =====")
    correct = defaultdict(int)
    unchanged = defaultdict(int)
    total = defaultdict(int)

    for row in test_set:
        doc = nlp(nfc(row["sentence"]))
        predicted, pos = None, None
        for token in doc:
            if norm(token.text) == norm(row["target"]):
                predicted, pos = norm(token.lemma_), token.pos_
                break

        if predicted is None:
            print(f"WARNING: target '{row['target']}' not found in its sentence")
            continue

        kind = row["type"]
        total[kind] += 1
        ok = predicted in row["accepted"]
        same = predicted == norm(row["target"])
        if ok:
            correct[kind] += 1
        if same:
            unchanged[kind] += 1
        print(f"{'OK ' if ok else 'ERR'} {row['target']:<12} model={predicted:<12} pos={pos}")

    print("--- accuracy | returned unchanged ---")
    for kind in total:
        pct = 100 * correct[kind] / total[kind]
        print(f"{kind:<12} {correct[kind]}/{total[kind]} ({pct:.0f}%) | unchanged: {unchanged[kind]}/{total[kind]}")