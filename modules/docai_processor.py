from google.cloud import documentai_v1 as documentai
from modules.config import GOOGLE_PROJECT_ID, DOCAI_PROCESSOR_ID, DOCAI_LOCATION

def process_pdf(file_path: str) -> dict:
    """
    Extracts text/entities from PDF using Google DocAI
    Returns: {"text": "...", "entities": {"key": "value"}}
    """
    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(GOOGLE_PROJECT_ID, DOCAI_LOCATION, DOCAI_PROCESSOR_ID)

    with open(file_path, "rb") as f:
        content = f.read()

    raw_doc = documentai.RawDocument(content=content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_doc)
    result = client.process_document(request=request)

    # Extract structured entities
    entities = {
        entity.type_: {
            "value": entity.mention_text,
            "confidence": entity.confidence
        } for entity in result.document.entities
    }

    return {
        "text": result.document.text,
        "entities": entities
    }