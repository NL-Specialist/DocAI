import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
import queue
from modules.docai_processor import process_pdf
from modules.openai_handler import ask_question

class PDFAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Analyzer Pro")
        master.geometry("800x600")

        # Create widgets
        self.create_widgets()

        # Queue for thread-safe GUI updates
        self.queue = queue.Queue()
        self.check_queue()

    def create_widgets(self):
        # Header
        header = ttk.Label(self.master, text="📄 PDF Analyzer Pro", 
                         font=('Helvetica', 16, 'bold'))
        header.pack(pady=10)

        ttk.Label(self.master, 
                text="Upload a PDF document and ask questions about its content").pack()

        # File Upload Section
        file_frame = ttk.Frame(self.master)
        file_frame.pack(pady=10, fill='x', padx=20)
        
        self.upload_btn = ttk.Button(file_frame, text="Upload PDF", 
                                   command=self.upload_pdf)
        self.upload_btn.pack(side='left')
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.pack(side='left', padx=10)

        # Question Input
        self.question_input = ttk.Entry(self.master)
        self.question_input.pack(pady=10, fill='x', padx=20)
        self.question_input.insert(0, "What would you like to know about the document?")

        # Analyze Button
        self.analyze_btn = ttk.Button(self.master, text="Analyze", 
                                    command=self.start_processing)
        self.analyze_btn.pack(pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(self.master, orient='horizontal', 
                                      mode='determinate')
        self.progress.pack(fill='x', padx=20)

        # Output Area
        self.output_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.output_area.pack(pady=10, fill='both', expand=True, padx=20)
        self.output_area.tag_config('question', font=('Helvetica', 10, 'bold'))
        self.output_area.tag_config('answer', font=('Helvetica', 10))

        # Status Bar
        self.status_label = ttk.Label(self.master, text="Ready", 
                                    relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill='x', side=tk.BOTTOM)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.file_label.config(text=file_path)
            self.update_status("PDF uploaded")

    def start_processing(self):
        pdf_path = self.file_label.cget('text')
        question = self.question_input.get()
        
        if not pdf_path or pdf_path == "No file selected":
            self.update_status("Please upload a PDF first")
            return
        if not question.strip():
            self.update_status("Please enter a question")
            return

        self.analyze_btn.config(state='disabled')
        self.update_status("Processing...")
        self.progress['value'] = 0

        # Start processing in background thread
        thread = threading.Thread(target=self.process_pdf, 
                                args=(pdf_path, question))
        thread.start()

    def process_pdf(self, pdf_path, question):
        try:
            self.queue.put(('progress', 10))
            self.queue.put(('status', "Uploading PDF..."))
            document_data = process_pdf(pdf_path)

            self.queue.put(('progress', 50))
            self.queue.put(('status', "Analyzing content..."))
            answer = ask_question(document_data, question)

            self.queue.put(('output', question, answer))
            self.queue.put(('progress', 100))
            self.queue.put(('status', "Analysis complete"))
            
        except Exception as e:
            self.queue.put(('error', str(e)))
        finally:
            self.queue.put(('enable_btn',))

    def check_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                if task[0] == 'progress':
                    self.progress['value'] = task[1]
                elif task[0] == 'status':
                    self.status_label.config(text=task[1])
                elif task[0] == 'output':
                    self.show_output(task[1], task[2])
                elif task[0] == 'error':
                    self.output_area.delete(1.0, tk.END)
                    self.output_area.insert(tk.END, f"Error: {task[1]}", 'error')
                    self.status_label.config(text="Error occurred")
                elif task[0] == 'enable_btn':
                    self.analyze_btn.config(state='normal')
        except queue.Empty:
            pass
        self.master.after(100, self.check_queue)

    def show_output(self, question, answer):
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, f"Question: {question}\n\n", 'question')
        self.output_area.insert(tk.END, f"Answer: {answer}\n", 'answer')

    def update_status(self, message):
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFAnalyzerApp(root)
    root.mainloop()