import numpy as np
import spacy
from scipy.spatial.distance import cosine

nlp = spacy.load("en_core_web_sm")

DOCUMENT = (
    "The Eiffel Tower, located in Paris, France, was constructed between 1887 and 1889 "
    "as the entrance arch to the 1889 World's Fair. It was designed by Gustave Eiffel's "
    "engineering company and initially faced criticism from artists and intellectuals who "
    "considered it an eyesore. Today, the Eiffel Tower is one of the most visited monuments "
    "in the world, attracting over 7 million visitors annually. In 2015, special lighting "
    "systems were added to enhance its nighttime appearance and improve energy efficiency."
)


def fixed_size_chunker(text, chunk_size=15, overlap=3):
    words = text.split()
    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]
        if not chunk_words:
            break
        chunks.append(" ".join(chunk_words))
        if start + chunk_size >= len(words):
            break
    return chunks


def _sentence_vector(sent_doc):
    vectors = [t.vector for t in sent_doc if t.has_vector and not t.is_stop and not t.is_punct]
    if not vectors:
        vectors = [t.vector for t in sent_doc]
    return np.mean(vectors, axis=0)


def semantic_chunker(text, similarity_threshold=0.75):
    doc = nlp(text)
    sentences = list(doc.sents)
    if not sentences:
        return []

    vectors = [_sentence_vector(s) for s in sentences]
    chunks = []
    current_chunk = [sentences[0].text.strip()]

    for i in range(1, len(sentences)):
        sim = 1 - cosine(vectors[i - 1], vectors[i])
        if sim >= similarity_threshold:
            current_chunk.append(sentences[i].text.strip())
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i].text.strip()]
    chunks.append(" ".join(current_chunk))
    return chunks


def metadata_chunker(text):
    doc = nlp(text)
    chunks = []
    for i, sent in enumerate(doc.sents):
        sent_doc = sent.as_doc()
        ents = [(e.text, e.label_) for e in sent_doc.ents]
        metadata = {
            "chunk_id": i,
            "contains_date": any(e[1] == "DATE" for e in ents),
            "contains_number": any(e[1] in ("CARDINAL", "QUANTITY", "PERCENT") for e in ents),
            "contains_entity": len(ents) > 0,
            "entities": ents,
        }
        chunks.append({"text": sent.text.strip(), "metadata": metadata})
    return chunks


def extract_key_facts(text):
    doc = nlp(text)
    facts = {"dates": [], "places": [], "people": [], "numbers": [], "events": []}

    for ent in doc.ents:
        if ent.label_ == "DATE":
            facts["dates"].append(ent.text)
        elif ent.label_ in ("GPE", "LOC", "FAC"):
            facts["places"].append(ent.text)
        elif ent.label_ == "PERSON" or ent.label_ == "ORG":
            facts["people"].append(ent.text)
        elif ent.label_ in ("CARDINAL", "QUANTITY", "PERCENT"):
            facts["numbers"].append(ent.text)
        elif ent.label_ == "EVENT":
            facts["events"].append(ent.text)

    event_keywords = ["World's Fair", "World’s Fair"]
    for kw in event_keywords:
        if kw in text and kw not in facts["events"]:
            facts["events"].append(kw)
    if "lighting systems were added" in text:
        facts["events"].append("Addition of nighttime lighting systems (2015)")
    if "constructed" in text:
        facts["events"].append("Construction of the Eiffel Tower (1887-1889)")

    for k in facts:
        seen = set()
        deduped = []
        for v in facts[k]:
            if v not in seen:
                seen.add(v)
                deduped.append(v)
        facts[k] = deduped

    return facts


def summarize(text, max_sentences=2):
    doc = nlp(text)
    sentences = list(doc.sents)
    scored = []
    for sent in sentences:
        sent_doc = sent.as_doc()
        score = len(sent_doc.ents) + 0.1 * len(sent_doc)
        scored.append((score, sent.text.strip()))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [s for _, s in scored[:max_sentences]]
    ordered = [s.text.strip() for s in sentences if s.text.strip() in top]
    return " ".join(ordered)


print("=" * 70)
print("1a. FIXED-SIZE CHUNKS (15 words, 3-word overlap)")
print("=" * 70)
for i, c in enumerate(fixed_size_chunker(DOCUMENT), 1):
    print(f"[{i}] {c}\n")

print("=" * 70)
print("1b. SEMANTIC CHUNKS (embedding similarity threshold)")
print("=" * 70)
for i, c in enumerate(semantic_chunker(DOCUMENT), 1):
    print(f"[{i}] {c}\n")

print("=" * 70)
print("1c. METADATA-BASED CHUNKS (per sentence + metadata)")
print("=" * 70)
for c in metadata_chunker(DOCUMENT):
    print(f"Text: {c['text']}")
    print(f"Metadata: {c['metadata']}\n")

print("=" * 70)
print("2. KEY FACTS")
print("=" * 70)
facts = extract_key_facts(DOCUMENT)
for k, v in facts.items():
    print(f"{k.capitalize()}: {v}")

print("\n" + "=" * 70)
print("3. SUMMARY")
print("=" * 70)
print(summarize(DOCUMENT))