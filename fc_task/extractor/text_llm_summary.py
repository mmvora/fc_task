import backoff
import openai
from openai.types.chat import ChatCompletion
from typing import Any

from ..config import load_openai_creds, get_openai_model

load_openai_creds()
openai_client = openai.OpenAI()


# This function is a wrapper around the OpenAI API client that retries on RateLimitError
@backoff.on_exception(backoff.expo, openai.RateLimitError, max_tries=5, factor=3)
def completions_with_backoff(**kwargs: Any) -> ChatCompletion:
    return openai_client.chat.completions.create(**kwargs)


def get_text_summary(text: str) -> str:
    response = completions_with_backoff(
        model=get_openai_model(),
        n=1,
        messages=[
            {
                "role": "system",
                "content": "You are a text summarization assistant that can help me summarize articles",
            },
            {
                "role": "user",
                "content": f"""Summarize the provided article, making sure you include and key points, termniology, and concepts:
                {text}""",
            },
        ],
    )
    response_content = response.choices[0].message.content
    if response_content is None:
        raise ValueError("Empty response from LLM")

    return response_content
