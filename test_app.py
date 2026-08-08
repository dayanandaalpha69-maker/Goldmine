import importlib.util
import os
import sys
import types
import unittest
from pathlib import Path


class FakeChatOpenAI:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def invoke(self, text):
        return types.SimpleNamespace(content="hello")


class AppConfigTests(unittest.TestCase):
    def test_loads_openai_key_from_env_file(self):
        fake_module = types.ModuleType("langchain_openai")
        fake_module.ChatOpenAI = FakeChatOpenAI
        sys.modules["langchain_openai"] = fake_module

        original = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "sk-test-key"

        spec = importlib.util.spec_from_file_location("app_module", str(Path(__file__).resolve().parent / "app.py"))
        module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(module)
            self.assertEqual(module.api_key, "sk-test-key")
        finally:
            if original is not None:
                os.environ["OPENAI_API_KEY"] = original
            elif "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
            sys.modules.pop("langchain_openai", None)


if __name__ == "__main__":
    unittest.main()
