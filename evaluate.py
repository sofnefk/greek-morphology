import unicodedata
from collections import defaultdict

import spacy

MODELS = ["el_core_news_sm", "el_core_news_lg"]


def nfc(s):
    return unicodedata.normalize("NFC", s).lower()


# (sentence, target word, set of ACCEPTED lemmas, type)
TEST_SET = [
    ("Τα παιδιά παίζουν έξω.",    "παίζουν",   {"παίζω"},             "regular"),
    ("Τρέχουμε κάθε πρωί.",       "τρέχουμε",  {"τρέχω"},             "regular"),
    ("Διαβάζεις πολύ.",           "διαβάζεις", {"διαβάζω"},           "regular"),
    ("Έγραψα ένα μήνυμα.",        "έγραψα",    {"γράφω"},             "stem_change"),
    ("Πήρα το βιβλίο.",           "πήρα",      {"παίρνω", "πάρω"},    "stem_change"),
    ("Βρήκα τα κλειδιά.",         "βρήκα",     {"βρίσκω"},            "stem_change"),
    ("Εγώ έφαγα ψωμί.",           "έφαγα",     {"τρώω", "τρώγω"},     "suppletive"),
    ("Μου είπε την αλήθεια.",     "είπε",      {"λέω", "λέγω"},       "suppletive"),
    ("Είδα μια ταινία χθες.",     "είδα",      {"βλέπω"},             "suppletive"),
    ("Ήρθε στο σπίτι μας.",       "ήρθε",      {"έρχομαι"},           "suppletive"),
]

for model_name in MODELS:
    try:
        nlp = spacy.load(model_name)
    except OSError:
        print(f"\n!! {model_name} not installed, skipping")
        continue

    print(f"\n===== {model_name} =====")
    correct = defaultdict(int)
    total = defaultdict(int)

    for sentence, target, accepted, kind in TEST_SET:
        doc = nlp(nfc(sentence))
        predicted, pos = None, None
        for token in doc:
            if nfc(token.text) == nfc(target):
                predicted, pos = nfc(token.lemma_), token.pos_
                break

        total[kind] += 1
        ok = predicted in {nfc(a) for a in accepted}
        if ok:
            correct[kind] += 1
        print(f"{'OK ' if ok else 'ERR'} {target:<10} model={predicted:<10} pos={pos}")

    print("--- accuracy ---")
    for kind in total:
        pct = 100 * correct[kind] / total[kind]
        print(f"{kind:<12} {correct[kind]}/{total[kind]} ({pct:.0f}%)")