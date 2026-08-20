# AI Terminal

A small command-line chat client that uses the OpenRouter free model through the OpenAI-compatible API.

## Requirements

- Python 3.9 or newer
- An OpenRouter API key

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies:

   ```powershell
   pip install -r requirement.txt
   ```

3. Create `.env` from `.env.example` and set your key:

   ```env
   OPENAI_API_KEY=your_openrouter_api_key
   ```

## Run

```powershell
python main.py
```

## Commands

- `\help` shows available commands.
- `\clear` clears the conversation and the terminal.
- `\check_usage` shows the tokens reported by the response stream.
- `\exit` closes the application.
