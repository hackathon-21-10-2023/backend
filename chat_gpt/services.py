import openai
import g4f

# API_KEY = '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'
# openai.api_key = API_KEY
openai.api_base = "http://localhost:1337/v1"


def ask_gpt():
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
        stream=True,
    )

