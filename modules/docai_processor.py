from google.cloud import documentai
from PyPDF2 import PdfReader, PdfWriter
from modules.config import GOOGLE_PROJECT_ID, DOCAI_PROCESSOR_ID, DOCAI_LOCATION
import os

def process_pdf(file_path: str) -> dict:
    """
    Processes a PDF document by splitting it into chunks of 15 pages and
    processing each chunk separately using Google Document AI.

    Args:
        file_path (str): Path to the PDF file to process.

    Returns:
        dict: A dictionary containing the combined text and entities from all chunks.
    """
    # Helper function to split PDF into chunks
    def split_pdf(file_path: str, chunk_size: int = 15) -> list:
        """
        Splits a PDF file into smaller chunks with a maximum of `chunk_size` pages.

        Args:
            file_path (str): Path to the input PDF file.
            chunk_size (int): Maximum number of pages per split file.

        Returns:
            list: List of file paths for the split PDF files.
        """
        reader = PdfReader(file_path)
        output_files = []
        
        # Split the PDF into chunks
        for i in range(0, len(reader.pages), chunk_size):
            writer = PdfWriter()
            for page in reader.pages[i:i + chunk_size]:
                writer.add_page(page)
            chunk_path = f"{file_path}_chunk_{i // chunk_size + 1}.pdf"
            with open(chunk_path, "wb") as chunk_file:
                writer.write(chunk_file)
            output_files.append(chunk_path)

        return output_files

    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(
        GOOGLE_PROJECT_ID,
        DOCAI_LOCATION,
        DOCAI_PROCESSOR_ID
    )

    # Split the PDF into 15-page chunks
    chunk_files = split_pdf(file_path)

    combined_text = ""
    combined_entities = {}

    # Process each chunk
    for chunk in chunk_files:
        with open(chunk, "rb") as f:
            content = f.read()

        # Document AI raw document format
        raw_document = documentai.RawDocument(
            content=content,
            mime_type="application/pdf"
        )

        # Process the document with Document AI
        request = documentai.ProcessRequest(
            name=processor_name,
            raw_document=raw_document
        )
        result = client.process_document(request=request)

        # Extract text and entities
        combined_text += result.document.text
        for entity in result.document.entities:
            entity_type = entity.type_
            if entity_type not in combined_entities:
                combined_entities[entity_type] = []
            combined_entities[entity_type].append({
                "value": entity.mention_text,
                "confidence": entity.confidence
            })

        # Optionally delete the chunk after processing
        os.remove(chunk)

    return {
        "text": combined_text,
        "entities": combined_entities
    }
