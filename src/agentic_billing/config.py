"""Centralized configuration loaded from environment variables."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_openai_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. "
            "Copy .env.example to .env and add your API key."
        )
    return key


def get_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_temporal_address() -> str:
    return os.getenv("TEMPORAL_ADDRESS", "localhost:7233")


def get_langfuse_config() -> dict:
    return {
        "secret_key": os.getenv("LANGFUSE_SECRET_KEY", ""),
        "public_key": os.getenv("LANGFUSE_PUBLIC_KEY", ""),
        "host": os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
    }
