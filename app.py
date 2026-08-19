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

# Prefer OPENAI_API_KEY when present (keeps compatibility with tests); otherwise use GROQ_API_KEY
api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY or OPENAI_API_KEY is not set. Add it to your environment or .env file.")

# Model selection with fallback support. Configure via `.env`:
# GROQ_MODEL=preferred_model
# GROQ_FALLBACK_MODELS=gpt-oss-20b,gpt-4o
preferred = os.getenv("GROQ_MODEL")
fallbacks = [m.strip() for m in os.getenv("GROQ_FALLBACK_MODELS", "gpt-oss-20b,gpt-4o").split(",") if m.strip()]
models = []
if preferred:
    models = [preferred] + [m for m in fallbacks if m != preferred]
else:
    models = fallbacks

current_model_index = 0
llm = None

def init_llm(idx: int):
    global llm, current_model_index
    if idx < 0 or idx >= len(models):
        return False
    model_to_try = models[idx]
    print(f"Attempting model: {model_to_try}")
    try:
        llm = ChatGroq(model=model_to_try, temperature=0, api_key=api_key)
        current_model_index = idx
        print(f"Using model: {model_to_try}")
        return True
    except Exception as e:
        print(f"Failed to initialize model {model_to_try}: {e}")
        llm = None
        return False

# initialize first available model
if not models:
    raise RuntimeError("No candidate models configured. Set GROQ_MODEL or GROQ_FALLBACK_MODELS in .env")
if not init_llm(0):
    # try remaining fallbacks
    for i in range(1, len(models)):
        if init_llm(i):
            break

def main():
    print("Type your question (or 'exit' to quit):")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break
        if not question:
            continue

        # attempt to invoke; on model-not-found errors, try next fallback
        try:
            if llm is None:
                raise RuntimeError("No model initialized. Check configuration.")
            response = llm.invoke(question)
            print(f"Assistant: {response.content}")
        except Exception as e:
            msg = str(e)
            model_error = False
            if GroqNotFoundError is not None and isinstance(e, GroqNotFoundError):
                model_error = True
            elif "model_not_found" in msg or "does not exist" in msg or "model not found" in msg:
                model_error = True

            if model_error:
                print(f"Model error with '{models[current_model_index]}': {msg}")
                # try next model if available
                next_idx = current_model_index + 1
                switched = False
                while next_idx < len(models):
                    if init_llm(next_idx):
                        switched = True
                        break
                    next_idx += 1

                if switched:
                    print(f"Switched to model {models[current_model_index]}; retrying your query...")
                    try:
                        response = llm.invoke(question)
                        print(f"Assistant: {response.content}")
                    except Exception as e2:
                        print(f"Retry failed: {e2}")
                else:
                    print("No available fallback models succeeded. See README for configuration and account access.")
            else:
                print(f"Error: {msg}")
            continue


if __name__ == "__main__":
    main()