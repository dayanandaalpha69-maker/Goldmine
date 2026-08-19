import os
from pathlib import Path

from langchain_groq import ChatGroq

try:
    from groq import NotFoundError as GroqNotFoundError
except Exception:
    GroqNotFoundError = None


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = [part.strip() for part in line.split("=", 1)]
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        os.environ.setdefault(key, value)


load_env_file(Path(__file__).resolve().parent / ".env")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set. Add it to your environment or .env file.")

model_name = os.getenv("GROQ_MODEL", "gpt-oss-20b")
print(f"Using model: {model_name}")
llm = ChatGroq(model=model_name, temperature=0, api_key=api_key)

print("Type your question (or 'exit' to quit):")
while True:
    question = input("You: ").strip()
    if question.lower() in {"exit", "quit", "q"}:
        print("Goodbye!")
        break
    if not question:
        continue

    try:
        response = llm.invoke(question)
        print(f"Assistant: {response.content}")
    except Exception as e:
        # Handle model not found / access errors gracefully and provide guidance
        msg = str(e)
        if GroqNotFoundError is not None and isinstance(e, GroqNotFoundError):
            print("Error: model not found or inaccessible.")
        else:
            # Inspect message for common provider error text
            if "model_not_found" in msg or "does not exist" in msg:
                print("Error: model not found or you do not have access to it.")
            else:
                print(f"Error: {msg}")

        print("Suggestion: set a different model via the GROQ_MODEL environment variable (for example, GROQ_MODEL=gpt-4o)")
        print("Or verify your Groq account has access to the requested model and that the API key is correct.")
        continue