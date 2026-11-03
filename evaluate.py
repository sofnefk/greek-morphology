import csv
import unicodedata
from collections import defaultdict

import spacy

MODELS = ["el_core_news_sm", "el_core_news_lg"]
TEST_FILE = "data/test_set.csv"
VERBOSE = False  # set True to print every row


def nfc(s):
    """Unicode NFC only. Keeps case."""
    return unicodedata.normalize("NFC", s).strip()


def norm(s):
    """NFC + lowercase. Always used for comparing strings."""
    return nfc(s).lower()


CONDITIONS = {"keep_case": nfc, "lowercase": norm}


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

    for cond_name, prep in CONDITIONS.items():
        correct = defaultdict(int)
        unchanged = defaultdict(int)
        not_verb = defaultdict(int)
        total = defaultdict(int)

        for row in test_set:
            doc = nlp(prep(row["sentence"]))
            predicted, pos = None, None
            for token in doc:
                if norm(token.text) == norm(row["target"]):
                    predicted, pos = norm(token.lemma_), token.pos_
                    break

            if predicted is None:
                print(f"WARNING: '{row['target']}' not found in its sentence")
                continue

            kind = row["type"]
            total[kind] += 1
            ok = predicted in row["accepted"]
            correct[kind] += ok
            unchanged[kind] += predicted == norm(row["target"])
            not_verb[kind] += pos != "VERB"
            if VERBOSE:
                print(f"{'OK ' if ok else 'ERR'} {row['target']:<12} -> {predicted:<12} {pos}")

        print(f"\n===== {model_name} | {cond_name} =====")
        for kind in total:
            n = total[kind]
            print(
                f"{kind:<12} correct {correct[kind]}/{n} ({100*correct[kind]/n:.0f}%)"
                f" | unchanged {unchanged[kind]}/{n}"
                f" | not VERB {not_verb[kind]}/{n}"
            )