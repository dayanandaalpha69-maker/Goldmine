import importlib.util
import os
import unittest
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


class AppConfigTests(unittest.TestCase):
    def test_loads_gemini_provider_configuration(self):
        original_provider = os.environ.get("PROVIDER")
        original_key = os.environ.get("GEMINI_API_KEY")
        os.environ["PROVIDER"] = "gemini"
        os.environ["GEMINI_API_KEY"] = "test-key"

        spec = importlib.util.spec_from_file_location("app_module", str(Path(__file__).resolve().parent / "app.py"))
        module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(module)
            self.assertEqual(module.provider, "gemini")
            client, model_name = module.create_model()
            self.assertEqual(model_name, "gemini-3.8-flash")
            self.assertIsNotNone(client)
        finally:
            if original_provider is not None:
                os.environ["PROVIDER"] = original_provider
            else:
                os.environ.pop("PROVIDER", None)
            if original_key is not None:
                os.environ["GEMINI_API_KEY"] = original_key
            elif "GEMINI_API_KEY" in os.environ:
                del os.environ["GEMINI_API_KEY"]


class ConversationTests(unittest.TestCase):
    @staticmethod
    def load_app():
        spec = importlib.util.spec_from_file_location(
            "app_module", str(Path(__file__).resolve().parent / "app.py")
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_prepare_messages_keeps_system_and_last_messages(self):
        module = self.load_app()
        messages = [SystemMessage(content="system")]
        messages.extend(
            HumanMessage(content=f"message {index} " + "word " * 40)
            for index in range(10)
        )

        trimmed = module.prepare_messages(messages)

        self.assertEqual(trimmed[0].content, "system")
        self.assertIn("message 9", trimmed[-1].content)

    def test_gemini_ask_uses_interactions_api_with_stateless_history(self):
        module = self.load_app()
        original_provider = module.provider
        module.provider = "gemini"

        class FakeClient:
            class Interactions:
                request = None

                @classmethod
                def create(cls, **request):
                    cls.request = request

                    class Response:
                        output_text = "reply"

                    return Response()

            interactions = Interactions()

        client = FakeClient()
        messages = [
            SystemMessage(content="system prompt"),
            HumanMessage(content="question"),
            AIMessage(content="answer"),
            HumanMessage(content="follow-up"),
        ]

        try:
            result = module.ask(client, "gemini-3.8-flash", messages)
        finally:
            module.provider = original_provider

        self.assertEqual(result, "reply")
        self.assertEqual(client.interactions.request["model"], "gemini-3.8-flash")
        self.assertEqual(client.interactions.request["system_instruction"], "system prompt")
        self.assertFalse(client.interactions.request["store"])
        self.assertEqual(
            [step["type"] for step in client.interactions.request["input"]],
            ["user_input", "model_output", "user_input"],
        )

    def test_summarize_messages_preserves_summary_and_recent_context(self):
        module = self.load_app()

        class FakeClient:
            class Interactions:
                @staticmethod
                def create(**request):
                    class Response:
                        output_text = "facts from the conversation"

                    return Response()

            interactions = Interactions()

        messages = [SystemMessage(content="system")]
        for index in range(5):
            messages.extend(
                [HumanMessage(content=f"question {index}"), AIMessage(content=f"answer {index}")]
            )

        result = module.summarize_messages(FakeClient(), "test", messages)

        self.assertIn("Conversation summary:", result[0].content)
        self.assertEqual(result[-1].content, "answer 4")


if __name__ == "__main__":
    unittest.main()
