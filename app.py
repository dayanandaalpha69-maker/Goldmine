import os
from pathlib import Path

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.messages.utils import count_tokens_approximately, trim_messages

MAX_MESSAGE_TOKENS = 200
SUMMARY_MESSAGE_INTERVAL = 10
SYSTEM_PROMPT = "You are a helpful assistant."

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

def _gemini_contents(messages: list[BaseMessage]) -> list[dict[str, object]]:
    contents = []
    for message in messages:
        role = "model" if isinstance(message, AIMessage) else "user"
        contents.append({"role": role, "parts": [{"text": str(message.content)}]})
    return contents


def ask(model_client, model_name: str, messages: list[BaseMessage] | str) -> str:
    if isinstance(messages, str):
        messages = [HumanMessage(content=messages)]

    if provider == "gemini":
        response = model_client.models.generate_content(
            model=model_name,
            contents=_gemini_contents(messages),
        )
        return response.text

    return model_client.invoke(messages).content


def summarize_messages(
    model_client, model_name: str, messages: list[BaseMessage]
) -> list[BaseMessage]:
    system_message = next(
        (message for message in messages if isinstance(message, SystemMessage)),
        SystemMessage(content=SYSTEM_PROMPT),
    )
    conversation = [message for message in messages if not isinstance(message, SystemMessage)]
    transcript = "\n".join(
        f"{message.type}: {message.content}" for message in conversation
    )
    summary_request = [
        SystemMessage(content="Summarize the conversation, preserving facts, decisions, and open questions."),
        HumanMessage(content=transcript),
    ]
    summary = ask(model_client, model_name, summary_request)
    recent_messages = conversation[-4:]
    combined_system = SystemMessage(
        content=f"{system_message.content}\n\nConversation summary:\n{summary}"
    )
    return [combined_system, *recent_messages]


def prepare_messages(messages: list[BaseMessage]) -> list[BaseMessage]:
    return trim_messages(
        messages,
        max_tokens=MAX_MESSAGE_TOKENS,
        token_counter=count_tokens_approximately,
        strategy="last",
        include_system=True,
    )

def main() -> None:
    model_client, model_name = create_model()
    messages: list[BaseMessage] = [SystemMessage(content=SYSTEM_PROMPT)]
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
            messages.append(HumanMessage(content=question))
            response = ask(model_client, model_name, prepare_messages(messages))
            messages.append(AIMessage(content=response))
            conversation_message_count = sum(
                not isinstance(message, SystemMessage) for message in messages
            )
            if conversation_message_count % SUMMARY_MESSAGE_INTERVAL == 0:
                messages = summarize_messages(model_client, model_name, messages)
            print(f"Assistant: {response}")
        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
