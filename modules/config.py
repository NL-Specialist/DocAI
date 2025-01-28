import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ollama model
OLLAMA_MODEL =  os.getenv("OLLAMA_MODEL")
OLLAMA_HOST =  os.getenv("OLLAMA_HOST")

# Google DocAI Config
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
DOCAI_PROCESSOR_ID = os.getenv("DOCAI_PROCESSOR_ID")
DOCAI_LOCATION = os.getenv("DOCAI_LOCATION", "us")  # Default to "us" if not set

# OpenAI Config
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")  # Default to "gpt-4" if not set
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Must be set externally

# Example usage
print("Google Project ID:", GOOGLE_PROJECT_ID)
print("DocAI Processor ID:", DOCAI_PROCESSOR_ID)
print("DocAI Location:", DOCAI_LOCATION)
print("OpenAI Model:", OPENAI_MODEL)
print("OpenAI API Key:", OPENAI_API_KEY)