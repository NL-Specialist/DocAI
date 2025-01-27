import argparse
from modules.docai_processor import process_pdf
from modules.openai_handler import ask_question

def main():
    parser = argparse.ArgumentParser(description="Analyze PDF documents")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("question", help="Question to ask about the document")
    args = parser.parse_args()

    # Step 1: Extract data
    print(f"Processing {args.pdf_path}...")
    document_data = process_pdf(args.pdf_path)
    
    # Step 2: Answer question
    print(f"Answering: '{args.question}'")
    answer = ask_question(document_data, args.question)
    
    print("\n--- ANSWER ---")
    print(answer)

if __name__ == "__main__":
    main()