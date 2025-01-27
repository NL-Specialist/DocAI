import openai
from modules.config import OPENAI_MODEL, OPENAI_API_KEY

SYSTEM_PROMPT = """
You analyze documents and answer questions strictly using provided data.
Rules:
1. If the answer isn't in the data, say "Not found in document."
2. Never invent answers.
3. Keep responses under 2 sentences.
"""

def ask_question(document_data: dict, question: str) -> str:
    """
    Queries OpenAI with document data and a question
    """
    openai.api_key = OPENAI_API_KEY

    context = f"""
    DOCUMENT TEXT:
    {document_data['text']}

    STRUCTURED DATA:
    {document_data['entities']}
    """

    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ],
        temperature=0.1  # Reduce creativity for factual answers
    )

    return response.choices[0].message['content']