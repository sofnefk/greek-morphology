# Greek verb lemmatisation: how well does spaCy handle irregular verbs?

## Research question
How accurately do spaCy's Greek models (`el_core_news_sm` and `el_core_news_lg`)
lemmatise verb forms, and does accuracy depend on verb type
(regular, stem change, suppletive)?

## Hypothesis
Accuracy is highest for regular verbs and lowest for suppletive verbs
(e.g. τρώω → έφαγα), because suppletive forms share no stem with the lemma.

## Method
- Hand-labelled test set in `data/test_set.csv`: sentence, target word,
  accepted lemma(s), verb type.
- Each model lemmatises the sentence; I compare the lemma of the target word
  to the accepted list.
- Two input conditions: original case vs lowercased.
- Extra metrics: how often the model returns the word unchanged, and how
  often it does not tag the word as a VERB.
- Run with `python evaluate.py`.

## Pilot results (10 rows, NOT conclusive)
| Model | Condition | Regular | Stem change | Suppletive |
|-------|-----------|---------|-------------|------------|
| sm | keep case | 1/3 | 0/3 | 1/4 |
| sm | lowercase | 2/3 | 0/3 | 1/4 |
| lg | keep case | 2/3 | 0/3 | 1/4 |
| lg | lowercase | 2/3 | 0/3 | 1/4 |

Observations:
- Stem-change verbs were 0/3 in every run, always returned unchanged.
- `lg` tagged every target as VERB; `sm` often did not (NOUN, ADJ, X).
- `lg` gave identical results with and without lowercasing; `sm` did better
  lowercased. Targets that were sentence-initial are confounded with case.
- `είπε → λέγω` counts as correct only because I accepted `λέγω` as a
  valid variant lemma of `λέω`.

## Limitations
- Only 10 rows: one flipped row moves a category by 25-33 points.
- Only verbs, labelled by me.
- Short sentences with little context.
- Case and sentence position are confounded in the pilot.

## Next steps
- Grow the test set to 50+ rows (same verbs across persons/tenses,
  targets at sentence start and middle).
- Interactive results app (Streamlit).
- Compare with Ancient Greek tools.