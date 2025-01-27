import os

# Google DocAI Config
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "your-project-id")
DOCAI_PROCESSOR_ID = os.getenv("DOCAI_PROCESSOR_ID", "your-processor-id")
DOCAI_LOCATION = os.getenv("DOCAI_LOCATION", "us")  # e.g., "us", "eu"

# OpenAI Config
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")  # Must be set externally