import os
from pathlib import Path

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

provider = os.getenv("PROVIDER", "gemini").lower()

def create_model():
    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set in .env.")

        from google import genai

        model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        return genai.Client(api_key=api_key), model_name

    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set in .env.")

        from langchain_groq import ChatGroq

        model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
        return ChatGroq(model=model_name, temperature=0, api_key=api_key), model_name

    raise RuntimeError("Unsupported PROVIDER. Use 'gemini' or 'groq'.")

def ask(model_client, model_name: str, question: str) -> str:
    if provider == "gemini":
        response = model_client.models.generate_content(
            model=model_name,
            contents=question,
        )
        return response.text

    return model_client.invoke(question).content

def main() -> None:
    model_client, model_name = create_model()
    print(f"Using provider: {provider} ({model_name})")
    print("Type your question (or 'exit' to quit):")

    while True:
        try:
            question = input("You: ").strip()
        except EOFError:
            print("\nGoodbye!")
            break

        if question.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break
        if not question:
            continue

        try:
            print(f"Assistant: {ask(model_client, model_name, question)}")
        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
