# RAG Evaluation Report

## 1. Scope and dataset

This checkpoint evaluates a retrieval-augmented generation pipeline over *Les morts qui parlent* by Eugène-Melchior de Vogüé. The corpus is Project Gutenberg ebook `#79438`, released August 23, 2026, and identified as French text originally published in Paris in 1911. `ingest.py` downloads the plain-text edition from `https://gutenberg.org/cache/epub/79438/pg79438.txt` at runtime.

The ingestion path applies `RecursiveCharacterTextSplitter` with a 100-character chunk size and 20-character overlap. Each chunk is embedded with `sentence-transformers/all-MiniLM-L6-v2` and inserted into a Chroma collection named `gmc`. At query time, the retriever returns the five nearest chunks by default. The generation prompt places those chunks under `CONTEXT` and asks the chat model to answer from them. No metadata, page identifiers, source citations, or persistent index are currently attached to chunks.

## 2. Metrics and current status

No labeled evaluation questions, reference answers, retrieval annotations, or model-run logs are committed in the repository. Consequently, numeric scores would be fabricated if reported as completed results. The table below defines the required metrics and records the current status.

| Area | Metric | Definition | Current result |
| --- | --- | --- | --- |
| Retrieval | Recall@k | Fraction of questions where at least one relevant chunk appears in the top `k` results | Not measured; no relevance labels |
| Retrieval | MRR@k | Mean reciprocal rank of the first relevant chunk | Not measured; no relevance labels |
| Retrieval | Context precision | Relevant retrieved chunks divided by all retrieved chunks | Not measured; no relevance labels |
| Generation | Exact match / token F1 | Comparison with a short reference answer where applicable | Not measured; no reference set |
| Generation | Faithfulness | Claims supported by retrieved context divided by verifiable claims | Not measured; requires claim annotations or judge protocol |
| Generation | Answer relevance | Whether the response directly answers the question | Not measured; requires human or judge labels |
| Operations | Latency | Time for ingestion, retrieval, and generation separately | Not measured; remote model and cold-start costs vary |

A defensible benchmark should contain at least 20 questions covering factual lookup, character and event questions, summaries, and unanswerable questions. Each question should have a reference answer and one or more relevant chunk identifiers. Results should be reported separately for `k=1`, `k=3`, and `k=5`, with the model name, temperature, prompt, and corpus revision fixed.

## 3. Qualitative failure cases

The current implementation has several predictable failure modes:

- **Very small chunks:** 100 characters can separate a question's evidence across several results. A retrieved chunk may contain a pronoun or sentence fragment without the surrounding context needed to resolve it.
- **Language mismatch:** The corpus is French, but the example question is English and the prompt does not request a response language. Cross-language retrieval and generation may work inconsistently depending on the model.
- **Unsupported questions:** The prompt says to answer from context but does not explicitly instruct the model to say that the answer is unavailable. The model may produce a plausible answer from general knowledge.
- **No source grounding in output:** Answers contain no chunk references, so a user cannot quickly verify which passage supports a claim.
- **Runtime instability:** The source is fetched remotely and the embedding model is loaded on demand. Network failures, source revisions, and cold model startup affect repeatability.

These are qualitative risk findings from code inspection and the pipeline design, not claims about a statistically sampled run.

## 4. Hallucinations and retrieval mitigation

Without retrieval, a language model can answer questions about the novel using memorized associations, patterns from other books, or fluent invention. Retrieval mitigates this by placing corpus passages directly in the model's context. For questions whose answer is explicitly present in one of the top five chunks, this narrows the evidence available to the generator and can improve factual specificity. The overlap also gives a neighboring chunk a chance to preserve a boundary sentence.

Retrieval is a mitigation, not a guarantee. It cannot correct a missed passage, an overly small or ambiguous chunk, a poor embedding match, or a model that ignores context. The absence of a refusal instruction and citations leaves residual hallucination risk, especially for questions outside the book. The next practical improvements are larger semantically coherent chunks with metadata, an explicit “answer only from context; otherwise say insufficient information” rule, citations, and an annotated benchmark with faithfulness review.

## 5. Conclusion

The checkpoint demonstrates the core RAG path end to end, but it does not yet provide a completed quantitative evaluation. The correct current conclusion is that retrieval is structurally present and should reduce unsupported generation when relevant passages are retrieved; the magnitude of that benefit remains unknown until the proposed benchmark and metric collection are implemented.
