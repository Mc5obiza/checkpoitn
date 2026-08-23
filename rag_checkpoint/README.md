# Gutenberg RAG Checkpoint

A minimal retrieval-augmented generation (RAG) pipeline for asking questions about the Project Gutenberg novel *Les morts qui parlent* by Eugène-Melchior de Vogüé. The source text is downloaded from Gutenberg when the application starts, split into overlapping chunks, embedded with `sentence-transformers/all-MiniLM-L6-v2`, indexed in Chroma, and passed to an OpenRouter-compatible chat model through LangChain.

## Project files

- `ingest.py` downloads the source text and creates 100-character chunks with 20-character overlap.
- `index.py` embeds the chunks and builds the Chroma vector store.
- `retrieve_generate.py` retrieves the top five chunks and generates an answer.
- `EVALUATION.md` records the evaluation scope, metrics, limitations, and qualitative findings.

## Setup

Python 3.10 or newer is recommended.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For local checks and future tests:

```powershell
pip install -r requirements-dev.txt
```

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openrouter_api_key
```

The code uses `https://openrouter.ai/api/v1` as the OpenAI-compatible base URL. The key is required even though the variable keeps the `OPENAI_API_KEY` name.

## Run

```powershell
python .\retrieve_generate.py
```

The current entry point runs the example query `what is this book`. To ask another question, change the query passed to `generate()` in `retrieve_generate.py`. The `k_top` argument controls how many chunks are retrieved and defaults to five.

## Reproducibility notes

The Gutenberg text is fetched on every run, so network access is required. The embedding model is downloaded on first use and may be cached locally. The current vector store is created in memory and is not persisted between processes. Generation output depends on the model selected by the OpenRouter account, model defaults, and remote availability.

Questions should be phrased with the source language in mind: the dataset is French, while the default example is English. The prompt asks the model to answer from context, but it does not yet require citations, a target language, or an explicit refusal when the retrieved context is insufficient.

## Limitations

There is currently no committed labeled question set, automated evaluation script, persisted index, or test suite. The evaluation report therefore distinguishes implementation facts and qualitative observations from quantitative metrics that still need to be measured on a fixed benchmark.
