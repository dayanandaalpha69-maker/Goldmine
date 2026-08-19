import importlib.util
import os
import unittest
from pathlib import Path


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
            self.assertEqual(model_name, "gemini-3.6-flash")
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


if __name__ == "__main__":
    unittest.main()
