"""Shared LLM client setup using instructor for structured outputs."""

import instructor
from openai import OpenAI

from .config import get_openai_api_key


def get_llm_client() -> instructor.Instructor:
    """Create an instructor-wrapped OpenAI client that returns Pydantic models."""
    return instructor.from_openai(
        OpenAI(api_key=get_openai_api_key())
    )
