import ollama
from modules.config import OLLAMA_MODEL, OLLAMA_HOST

SYSTEM_PROMPT = """
You analyze documents and answer questions strictly using provided data.
Rules:
1. If the answer isn't in the data, say "Not found in document."
2. Never invent answers.
3. Keep responses under 2 sentences.
4. Be concise and factual.
"""

def ask_question(document_data: dict, question: str) -> str:
    """
    Queries local Ollama LLM with document data and question
    """
    client = ollama.Client(host=OLLAMA_HOST)  # Default: http://localhost:11434
    
    # Truncate context for local models
    context = f"""
    DOCUMENT TEXT:
    {document_data['text'][:1500]}  # First 1500 characters
    
    STRUCTURED DATA:
    {str(document_data['entities'])[:500]}
    """

    try:
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
            ],
            options={
                "temperature": 0.3,
                "num_ctx": 2048,  # Context window size
                "num_predict": 2048  # Max response tokens
            }
        )
        return response['message']['content']
    
    except Exception as e:
        return f"LLM Error: {str(e)}"