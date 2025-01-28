import streamlit as st
import tempfile
import os
from modules.docai_processor import process_pdf
from modules.openai_handler import ask_question

# Initialize session state
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'qa_list' not in st.session_state:
    st.session_state.qa_list = []

def main():
    st.set_page_config(page_title="PDF Analyzer Pro", layout="wide")
    st.title("📄 PDF Analyzer Pro")
    st.markdown("Upload a PDF document and ask questions about its content")

    # File upload section
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file.read()
        st.success("PDF uploaded successfully!")

    # Question input and analyze button
    question = st.text_input("What would you like to know about the document?", "")
    analyze_clicked = st.button("Analyze")

    if analyze_clicked:
        handle_analysis(question)

    # Display analysis history
    display_history()

def handle_analysis(question):
    """Handle the analysis process when user clicks the Analyze button"""
    if not validate_inputs(question):
        return
    
    with st.spinner("Processing your request..."):
        tmp_path = None
        try:
            # Create temporary PDF file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(st.session_state.uploaded_file)
                tmp_path = tmp_file.name

            # Process PDF and analyze content
            with st.status("Analyzing document...", expanded=True) as status:
                st.write("Extracting document content...")
                document_data = process_pdf(tmp_path)
                
                st.write("Generating answer...")
                answer = ask_question(document_data, question)
                
                status.update(label="Analysis complete!", state="complete")

            # Store results
            st.session_state.qa_list.append((question, answer))
            st.rerun()

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Clean up temporary file
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

def validate_inputs(question):
    """Validate user inputs before processing"""
    if not st.session_state.uploaded_file:
        st.error("Please upload a PDF file first")
        return False
    if not question.strip():
        st.error("Please enter a valid question")
        return False
    return True

def display_history():
    """Display previous Q&A pairs"""
    if st.session_state.qa_list:
        st.divider()
        st.subheader("Analysis History")
        
        for q, a in reversed(st.session_state.qa_list):
            with st.expander(f"Q: {q}", expanded=True):
                st.markdown(f"**A:** {a}")

if __name__ == "__main__":
    main()