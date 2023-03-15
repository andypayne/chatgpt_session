# chatgpt_session

[ChatGPT Completions Guide](https://platform.openai.com/docs/guides/chat)


## Usage

### API Key

1. Generate an OpenAI platform [API key](https://platform.openai.com/account/api-keys).
2. Copy the key and set it in the environment variable `$OPENAI_PLATFORM_KEY` (or specify it some other way).

### Sample code

Sample usage code (also in the file):

```python
import os
from chatgpt_session import ChatGPTSession

api_key = os.environ.get("OPENAI_PLATFORM_KEY")
session = ChatGPTSession(api_key)
prompt = "Tell a joke about computers."
session.add_msg(prompt)
response = session.run_completion()
print(f"A joke:\n{response}")
```

