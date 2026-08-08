# Goldmine
**Goldmine AI Chat Assistant**
Goldmine is a lightweight terminal-based AI chat application built using Python, LangChain, and Groq. It loads the API key from a local .env file, initializes a chat model, and allows users to ask questions interactively from the command line.

This project is designed for local experimentation, learning, and quick AI-powered terminal workflows.

**Features**
Terminal-based conversational AI
LangChain integration
Groq-powered language model
Reads configuration from .env
Interactive chat loop
Secure secret handling using .gitignore

**Tech Stack**
Python
LangChain
Groq
VS Code
GitHub

**Project Structure** 
app.py — main chatbot logic
.env — stores local environment variables, including the API key
.gitignore — prevents sensitive files from being committed
README.md — project documentation

**Prerequisites**
Before you run the app, make sure you have:

Python 3.10 or newer
A valid Groq API key
A project virtual environment configured

**Installation**
Open the project folder in VS Code
Create and activate a virtual environment
Install the required dependency:
**pip install langchain-groq**

Create a .env file in the project root
**Add your Groq key**:**GROQ_API_KEY**

Run the App
**python app.py**

**
Then type your question in the terminal, for example: What is the capital of India?**

**To exit the app, type: exit
**

VS Code Environment Setup
If VS Code does not load variables from .env automatically, enable:
**"python.terminal.useEnvFile": true**

This ensures terminal sessions can read the values from the .env file.
**
Security
Do not commit your .env file to GitHub. Keep your API key local and safe.**

The project includes .gitignore entries such as:
.env
.venv/
__pycache__/
*.pyc

GitHub Repository
https://github.com/dayanandaalpha69-maker/Goldmine.git

Notes
This project was built and verified as a working AI chat application using Groq. It is intended for learning, experimentation, and quick chatbot development in a local environment.
