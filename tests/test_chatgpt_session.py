import sys
import unittest
from unittest.mock import patch
import arrow
sys.path.append("../../chatgpt_session")
from chatgpt_session import ChatGPTSession


class TestChatGPTSession(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_key"
        self.session = ChatGPTSession(self.api_key)

    def test_generate_system_msg(self):
        system_msg = self.session.generate_system_msg(current_date="March 22 2023")
        self.assertIn("ChatGPT", system_msg)
        self.assertIn("September 2021", system_msg)
        self.assertIn("March 22 2023", system_msg)

    def test_clear(self):
        self.session.add_msg("Hello")
        self.assertEqual(len(self.session.messages), 1)
        self.session.clear()
        self.assertEqual(len(self.session.messages), 0)

    def test_add_system_msg(self):
        with patch.object(self.session, "generate_system_msg", return_value="Test system message") as mock_generate:
            self.session.add_system_msg()
            self.assertEqual(len(self.session.messages), 1)
            self.assertEqual(self.session.messages[0]["role"], "system")
            self.assertEqual(self.session.messages[0]["content"], "Test system message")
            mock_generate.assert_called_once_with()

    def test_add_msg(self):
        self.session.add_msg("Hello")
        self.assertEqual(len(self.session.messages), 1)
        self.assertEqual(self.session.messages[0]["role"], "user")
        self.assertEqual(self.session.messages[0]["content"], "Hello")

    def test_run_completion(self):
        resp = {
            "object": "chat.completion",
            "choices": [
                {
                    "message": {
						"content": "Ahoy mateys! Let me tell ye about the ChatGPT API!",
						"role": "assistant",
					},
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "stop",
                    "prefix": "Tell the world about the ChatGPT API in the style of a pirate.",
                    "model": "text-davinci-002",
                    "prompt": "Tell the world about the ChatGPT API in the style of a pirate.",
                    "created": "2023-03-22T18:31:42.766185Z",
                    "completions": 1,
                }
            ],
        }
        with patch.object(self.session, "resp", resp), \
             patch("openai.ChatCompletion.create", return_value=resp), \
             patch("arrow.now", return_value=arrow.get("2023-03-22")) as mock_arrow:
            self.assertEqual(self.session.run_completion(), "Ahoy mateys! Let me tell ye about the ChatGPT API!")
            self.assertEqual(len(self.session.messages), 1)
            #self.assertEqual(self.session.messages[1]["role"], "system")
            #self.assertEqual(self.session.messages[1]["content"], "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Knowledge cutoff: September 2021 Current date: March 22 2023")
            #mock_arrow.assert_called_once()

