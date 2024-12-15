from app.api.hooks.latex import Latex
from app.schemas import ConvertRequest, EditRequest
from fastapi import File, UploadFile, HTTPException, Query, APIRouter
import os
from typing import List

UPLOAD_DIR = "uploads"
LATEX_DIR = "latex_files"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LATEX_DIR, exist_ok=True)

router = APIRouter()

@router.post("/upload", response_model=dict, summary="Загрузить документ Word", description="Загрузить документ Word (.docx или .doc) и преобразовать его в LaTeX.")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = Latex.save_file(file, UPLOAD_DIR)

        if not Latex.validate_file_type(file_path):
            return {"error": f"Файл '{file.filename}' не является допустимым файлом Word."}

        if file.filename.endswith(".docx"):
            content = Latex.convert_docx_to_text(file_path)
        elif file.filename.endswith(".doc"):
            content = Latex.convert_doc_to_text(file_path)
        else:
            return {"error": "Неподдерживаемый формат файла."}

        latex_filename = file.filename.replace(".docx", ".tex").replace(".doc", ".tex")
        Latex.save_as_latex(content, latex_filename, LATEX_DIR)

        return {
            "status": "success",
            "filename": file.filename,
            "preview": content[:100],
        }
    except Exception as e:
        return {"status": "error", "details": str(e)}

@router.get("/get-all-files", response_model=List[str], summary="Получить все LaTeX файлы", description="Получить список всех сохраненных LaTeX файлов.")
async def get_all_files():
    files = os.listdir(LATEX_DIR)
    return files

@router.get("/get-latex", response_model=dict, summary="Получить содержимое LaTeX файла", description="Получить содержимое конкретного LaTeX файла.")
async def get_latex(file_name: str = Query(None, description="Имя LaTeX файла для получения")):
    if file_name is None:
        raise HTTPException(status_code=400, detail="Имя файла обязательно")

    latex_file_path = os.path.join(LATEX_DIR, file_name)

    if not os.path.exists(latex_file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    if not file_name.endswith(".tex"):
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")

    try:
        with open(latex_file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки файла: {str(e)}")

    return {"latex_content": content}

@router.put("/update-latex", response_model=dict, summary="Обновить LaTeX файл", description="Обновить содержимое конкретного LaTeX файла.")
async def update_latex(edit_request: EditRequest):
    latex_file_path = os.path.join(LATEX_DIR, edit_request.file_name + ".tex")

    if not os.path.exists(latex_file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    try:
        with open(latex_file_path, "w", encoding="utf-8") as f:
            f.write(edit_request.latex_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки файла: {str(e)}")

    return {"status": "success", "details": f"Файл '{edit_request.file_name}' успешно обновлен."}

@router.delete("/delete-file", response_model=dict, summary="Удалить файл", description="Удалить файл из папки uploads или latex_files.")
async def delete_file(file_name: str = Query(..., description="Имя файла для удаления")):
    word_file_path_docx = os.path.join(UPLOAD_DIR, file_name + ".docx")
    word_file_path_doc = os.path.join(UPLOAD_DIR, file_name + ".doc")
    latex_file_path = os.path.join(LATEX_DIR, file_name + ".tex")

    if os.path.exists(word_file_path_docx):
        os.remove(word_file_path_docx)
    if os.path.exists(word_file_path_doc):
        os.remove(word_file_path_doc)
    if os.path.exists(latex_file_path):
        os.remove(latex_file_path)

    return {"status": "success", "details": f"Файл '{file_name}' и соответствующие ему файлы были удалены."}

@router.post("/convert-latex-to-word", response_model=dict, summary="Конвертировать LaTeX в Word", description="Конвертировать LaTeX код в формат Word.")
async def convert_latex_to_word(convert_request: ConvertRequest):
    try:
        word_content = f"Конвертированный текст из LaTeX: {convert_request.latex_code}"
        return {"word_content": word_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка конвертации: {str(e)}")
