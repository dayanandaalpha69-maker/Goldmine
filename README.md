# Goldmine

Goldmine is a lightweight terminal-based AI chat application built using Python, LangChain, and Groq. It loads the API key from a local `.env` file, initializes a chat model, and allows users to ask questions interactively from the command line.

Note: The `llama-3.1-8b-instant` model has been decommissioned. This project now uses a configurable replacement model; by default it attempts to use `gpt-oss-20b`. If you do not have access to that model, set `GROQ_MODEL` in your `.env` to a model available to your account.

## Features
- Terminal-based conversational AI
- LangChain integration
- Groq-powered language model
- Reads configuration from `.env`
- Interactive chat loop
- Secure secret handling using `.gitignore`

## Tech Stack
- Python
- LangChain
- Groq
- VS Code
- GitHub

## Project Structure
- `app.py` — main chatbot logic
- `.env` — stores local environment variables, including the API key
- `.gitignore` — prevents sensitive files from being committed
- `README.md` — project documentation

## Prerequisites
Before you run the app, make sure you have:
- Python 3.10 or newer
- A valid Groq API key
- A project virtual environment configured

## Installation
1. Open the project folder in VS Code
2. Create and activate a virtual environment
3. Install the required dependency:

```bash
pip install langchain-groq
```

4. Create a `.env` file in the project root
5. Add your Groq key:

```env
GROQ_API_KEY=your_api_key_here
# Optional: override the default model
GROQ_MODEL=gpt-oss-20b
```

## Run the App

```bash
python app.py
```

Then type your question in the terminal, for example:

```
What is the capital of India?
```

To exit the app, type:

```
exit
```

## VS Code Environment Setup
If VS Code does not load variables from `.env` automatically, enable:

```json
"python.terminal.useEnvFile": true
```

This ensures terminal sessions can read the values from the `.env` file.

## Security
Do not commit your `.env` file to GitHub. Keep your API key local and safe.

The project includes `.gitignore` entries such as:

```
.env
.venv/
__pycache__/
*.pyc
```

## GitHub Repository
https://github.com/dayanandaalpha69-maker/Goldmine.git

## Notes
This project was built and verified as a working AI chat application using Groq. It is intended for learning, experimentation, and quick chatbot development in a local environment.

---

## Examples
Run a quick question from the command line (non-interactive):

```bash
echo "What is the capital of India?" | python app.py
```

Override model selection in `.env`:

```env
# Preferred model
GROQ_MODEL=gpt-4o
# Comma-separated fallbacks
GROQ_FALLBACK_MODELS=gpt-oss-20b,gpt-4o
```

## Badges
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-SEE_REPO-lightgrey)

## Development
Create and activate the virtual environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Run tests:

```bash
python -m unittest test_app.py
```
