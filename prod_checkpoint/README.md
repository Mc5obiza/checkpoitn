# FastAPI Checkpoint

A FastAPI learning assistant that provides chat, quiz-generation, and text-summarization endpoints through OpenRouter's OpenAI-compatible API.

## Requirements

- Python 3.10+
- An OpenRouter API key

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your_openrouter_api_key
   ```

## Run the API

```powershell
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive documentation is available at `/docs`.

## Test

```powershell
pytest
```

## Endpoints

- `GET /health` - Check API status.
- `POST /chat` - Send a message to the learning assistant.
- `POST /quizz` - Generate multiple-choice questions.
- `POST /summarize` - Summarize text into concise bullet points.

Example quiz request:

```json
{
  "subject": "FastAPI",
  "number": 5
}
```

Example summary request:

```json
{
  "text": "FastAPI is a modern Python web framework for building APIs.",
  "max_bullets": 3
}
```
