# Study Buddy

A command-line study tutor powered by the Mistral API.

## Setup

1. Create a virtual environment and install the dependencies:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install mistralai python-dotenv
   ```

2. Copy `.env.example` to `.env` and add your Mistral API key:

   ```text
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

3. Start the tutor:

   ```powershell
   python study_buddy.py
   ```

## Commands

- `\\help` shows available commands.
- `\\clear` clears the conversation history.
- `\\check_usage` shows token usage.
- `\\exit` quits the tutor.

The real `.env` file is ignored by Git. Never commit API keys.
