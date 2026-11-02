import unicodedata
import spacy

# Load the Greek model (the one you just downloaded)
nlp = spacy.load("el_core_news_sm")


def analyse(text):
    """Return (word, lemma, part of speech, morph features) for each word."""
    # NFC = store accented letters as ONE character (see Lecture 2, Greek slide).
    # Skipping this can silently break matching and counting.
    text = unicodedata.normalize("NFC", text)
    doc = nlp(text)

    rows = []
    for token in doc:
        if token.is_punct:
            continue
        rows.append((token.text, token.lemma_, token.pos_, str(token.morph)))
    return rows


sentences = [
    "Γράψαμε ένα γράμμα χθες.",           # γράφω -> γράψαμε (stem change)
    "Έφαγα ψωμί.",                          # τρώω -> έφαγα (suppletion)
    "Τα παιδιά παίζουν στον δρόμο.",        # regular verb
    "Οι δρόμοι είναι γεμάτοι.",             # δρόμοι: nom. or voc.? (Lecture 3)
]

for sentence in sentences:
    print(f"\n{sentence}")
    print(f"{'WORD':<12}{'LEMMA':<12}{'POS':<8}FEATURES")
    for word, lemma, pos, morph in analyse(sentence):
        print(f"{word:<12}{lemma:<12}{pos:<8}{morph}")