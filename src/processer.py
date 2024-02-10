import os
import glob
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import re


class Processer:
    def __init__(self, number_files):
        self.number_files = number_files
        self.download_dir = os.path.join(
            os.environ['USERPROFILE'], 'Downloads'
            )

    def get_files_path(self):
        files_path = glob.glob(os.path.join(self.download_dir, '*'))
        files_path.sort(key=os.path.getmtime, reverse=True)
        self.files_path = files_path[:self.number_files-1]

    def concatenate_pdfs(self):
        pdf_writer = PdfWriter()

        for pdf_file in self.files_path:
            pdf_reader = PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])

        self.pdf_file = BytesIO()
        pdf_writer.write(self.pdf_file)
        self.pdf_file.seek(0)

    def delete_files(self):
        for file in self.files_path:
            os.remove(file)

    def search_word_in_pdf(
            self, words=['precatórios', 'precatorio', 'prec']
            ):
        self.pdf_file.seek(0)
        pdf_reader = PdfReader(self.pdf_file)
        for word in words:
            regex = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if regex.search(text):
                    return True
        return False

    def run(self):
        self.get_files_path()
        self.concatenate_pdfs()
        self.delete_files()
        return self.search_word_in_pdf()
