# Goldmine

Goldmine is a lightweight AI chat application built using Python, Gemini, and Streamlit. It loads the API key from a local `.env` file and offers both a browser UI and terminal chat.

Gemini is the default provider. Groq remains available by setting `PROVIDER=groq`.

## Features
- Terminal-based conversational AI
- LangChain integration
- Gemini-powered language model
- Reads configuration from `.env`
- Interactive chat loop
- Secure secret handling using `.gitignore`

## Tech Stack
- Python
- LangChain
- Google Gemini
- Groq (optional)
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
- A valid Gemini API key
- A project virtual environment configured

## Installation
1. Open the project folder in VS Code
2. Create and activate a virtual environment
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root
5. Add your Gemini key:

```env
PROVIDER=gemini
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.6-flash
```

## Run the App

Launch the browser chat UI:

```bash
streamlit run streamlit_app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

For the terminal version:

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
This project is intended for learning, experimentation, and quick chatbot development in a local environment.

---

## Examples
Run a quick question from the command line (non-interactive):

```bash
echo "What is the capital of India?" | python app.py
```

Override model selection in `.env`:

```env
# Gemini configuration
PROVIDER=gemini
GEMINI_MODEL=gemini-3.6-flash

# Optional Groq mode
# PROVIDER=groq
# GROQ_MODEL=openai/gpt-oss-20b
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
