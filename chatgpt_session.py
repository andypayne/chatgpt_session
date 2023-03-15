import os
import arrow
import openai


class ChatGPTSession:
    """
    https://platform.openai.com/docs/guides/chat

    Sample API response:
    {
      "choices": [
        {
          "finish_reason": "stop",
          "index": 0,
          "message": {
            "content": "....",
            "role": "assistant"
          }
        }
      ],
      "created": 1678397396,
      "id": "chatcmpl-1234",
      "model": "gpt-3.5-turbo-0301",
      "object": "chat.completion",
      "usage": {
        "completion_tokens": 215,
        "prompt_tokens": 23,
        "total_tokens": 238
      }
    }
    """

    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
        self.messages = []
        self.resp = None

    def generate_system_msg(self, current_date=None):
        """
        From the docs:
        "In general, gpt-3.5-turbo-0301 does not pay strong attention to the system
        message, and therefore important instructions are often better placed in a
        user message."

        Example:
        {"role": "system", "content": "You are a helpful assistant that translates
        English to French."}

        """
        current_date = (
            current_date if current_date else arrow.now().format(fmt="MMMM DD YYYY")
        )
        knowledge_cutoff = "September 2021"
        system_msg = (
            "You are ChatGPT, a large language model trained by OpenAI. Answer as "
            "concisely as possible. "
            f"Knowledge cutoff: {knowledge_cutoff} "
            f"Current date: {current_date}"
        )
        return system_msg

    def clear(self):
        """
        Clear the history/context of previous messages.
        """
        self.messages = []

    def add_system_msg(self):
        self.messages.append({"role": "system", "content": self.generate_system_msg()})

    def add_msg(self, content):
        self.messages.append(
            {
                "role": "user",
                "content": content,
            }
        )

    def run_completion(self, max_tokens=500, temperature=1):
        """
        temperature:
        https://platform.openai.com/docs/api-reference/completions/create#completions/create-temperature
        """
        self.resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=self.messages,
        )
        assert self.resp["object"] == "chat.completion"
        resp_choice = self.resp["choices"][0]["message"]
        resp_role = resp_choice["role"]
        self.messages.append(
            {
                "role": resp_role,
                "content": resp_choice["content"],
            }
        )
        return resp_choice["content"]


if __name__ == "__main__":
    import sys

    api_key = os.environ.get("OPENAI_PLATFORM_KEY", None)
    if not api_key:
        print("Error: You must set the environment variable $OPENAI_PLATFORM_KEY.")
        sys.exit(1)
    session = ChatGPTSession(api_key)
    prompt = "Tell the world about the ChatGPT API in the style of a pirate."
    print(f"Prompt:\n{prompt}\n")
    session.add_msg(prompt)
    res = session.run_completion()
    print(f"Response:\n{res}")
