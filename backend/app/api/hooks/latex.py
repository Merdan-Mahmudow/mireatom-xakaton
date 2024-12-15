import subprocess
from fastapi import UploadFile
from docx import Document
import os
import mimetypes

UPLOAD_DIR = "uploads"
LATEX_DIR = "latex_files"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LATEX_DIR, exist_ok=True)

class Latex:
    @staticmethod
    def save_file(file: UploadFile, upload_dir: str) -> str:
        """Сохраняет файл на диск."""
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        return file_path

    @staticmethod
    def validate_file_type(file_path: str) -> bool:
        """Проверяет MIME-тип файла."""
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type in [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
        ]

    @staticmethod
    def convert_docx_to_text(file_path: str) -> str:
        """Извлекает текст из .docx файла."""
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    @staticmethod
    def convert_doc_to_docx(file_path: str) -> str:
        """Конвертирует .doc в .docx используя libreoffice."""
        try:
            subprocess.run(
                ["libreoffice", "--headless", "--convert-to", "docx", file_path, "--outdir", os.path.dirname(file_path)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            converted_path = file_path.replace(".doc", ".docx")
            if not os.path.exists(converted_path):
                raise Exception(f"Не удалось конвертировать файл {file_path} в .docx")
            return converted_path
        except Exception as e:
            raise Exception(f"Ошибка при конвертации .doc в .docx: {str(e)}")

    @staticmethod
    def convert_doc_to_text(file_path: str) -> str:
        """Обработка .doc файлов через предварительную конвертацию в .docx."""
        docx_path = Latex.convert_doc_to_docx(file_path)
        return Latex.convert_docx_to_text(docx_path)

    @staticmethod
    def save_as_latex(content: str, filename: str, latex_dir: str) -> str:
        """Сохраняет текст в LaTeX формате."""
        latex_file_path = os.path.join(latex_dir, filename)
        with open(latex_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return latex_file_path
