from pydantic import BaseModel, Field
from typing import Literal



class FormulaRequest(BaseModel):
    formula: str = Field(..., description="Строка формулы, например х**2 или х+2")
    type: Literal["diagram", "graph"] = Field(..., description="Тип объекта, diagram или formula")
    
class FormulaResponse(BaseModel):
    image_url: str = Field(..., description="URL созданного изображения")
    
class EditRequest(BaseModel):
    file_name: str = Field(..., description="Имя файла LaTeX")
    latex_content: str = Field(..., description="Измененный текст LaTeX")
    

class ConvertRequest(BaseModel):
    latex_code: str = Field(..., description="Текст LaTeX для конвертации")

