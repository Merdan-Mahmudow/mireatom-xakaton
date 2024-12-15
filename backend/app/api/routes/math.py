import os
from app.api.hooks.math import IMAGE_DIR, FormulaProcessor
from app.schemas import FormulaRequest, FormulaResponse
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/process-formula", summary="Обработка формулы")
async def process_formula(request: FormulaRequest):
    processor = FormulaProcessor()
    if request.type == "diagram":
        print(request.formula)
        image_url = processor.create_diagram(str(request.formula.replace(" ", "")))
    elif request.type == "graph":
        print(request.formula)
        image_url = processor.create_graph(str(request.formula.replace(" ", "")))
    else:
        raise HTTPException(status_code=400, detail="Неверный тип объекта")
    return FormulaResponse(image_url=f"/images/{os.path.basename(image_url)}")

@router.post("/images/{image_name}", summary="Получение изображения")
async def get_image(image_name: str):
    """"Возвращает изображение по его имени"""
    if not os.path.exists("images"):
        raise HTTPException(status_code=404, detail="Изображения не найдены")
    image_path = os.path.join(IMAGE_DIR, image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    return FileResponse(image_path)

@router.post("/parse-latex-file", response_model=FormulaResponse)
async def parse_latex_file(file: UploadFile = File(...)):
    """Роут для загрузки файла и парсинга LaTeX-формул"""
    
    # Читаем содержимое файла
    try:
        contents = await file.read()
        text = contents.decode("utf-8")  # Предполагаем, что файл в формате UTF-8
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при чтении файла: {str(e)}")
    
    # Парсим LaTeX формулы из текста
    parsed_formulas = FormulaProcessor.parse_latex_from_text(text)
    return FormulaResponse(formulas=parsed_formulas)
