import os
from pathlib import Path

from langchain_groq import ChatGroq


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

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=api_key)

print("Type your question (or 'exit' to quit):")
while True:
    question = input("You: ").strip()
    if question.lower() in {"exit", "quit", "q"}:
        print("Goodbye!")
        break
    if not question:
        continue

    response = llm.invoke(question)
    print(f"Assistant: {response.content}")