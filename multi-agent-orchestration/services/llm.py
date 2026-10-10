
import os
from typing import TypeVar, Type

import anthropic
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

T = TypeVar("T", bound=BaseModel)

MODEL_NAME = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def ask_claude_structured(
    system_prompt: str,
    user_prompt: str,
    response_model: Type[T],
) -> T:
    """
    Ask Claude for a response matching a Pydantic model.

    Args:
        system_prompt: Instructions defining Claude's role.
        user_prompt: The task or question.
        response_model: Pydantic model expected in the response.

    Returns:
        A validated instance of response_model.
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": (
                    "Return only valid JSON matching this schema:\n"
                    f"{response_model.model_json_schema()}\n\n"
                    f"Task:\n{user_prompt}"
                ),
            }
        ],
    )

    # Extract Claude's text response.
    text_blocks = [
        block.text
        for block in response.content
        if block.type == "text"
    ]

    if not text_blocks:
        raise RuntimeError("Claude returned no text response.")

    # Validate and parse the JSON into the requested Pydantic model.
    return response_model.model_validate_json(
        _strip_code_fences("\n".join(text_blocks))
    )


def _strip_code_fences(text: str) -> str:
    """Remove a ```json ... ``` wrapper if Claude adds one."""
    text = text.strip()
    if text.startswith("```"):
        # Drop the opening fence line (e.g. "```json").
        text = text.split("\n", 1)[1] if "\n" in text else ""
        text = text.rstrip()
        if text.endswith("```"):
            text = text[:-3]
    return text.strip()
