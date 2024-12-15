import re
from typing import List
from fastapi import HTTPException
import matplotlib.pyplot as plt
import numpy as np
import uuid
import os
from sympy.parsing.latex import parse_latex_lark
from latex2sympy import latex2sympy
from sympy import lambdify



IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)


class FormulaProcessor:
    def __init__(self):
        pass
    @staticmethod
    def parse_formula(formula: str) -> str:
        """Парсинг LaTeX-формул"""
        try:
            # Преобразуем LaTeX строку в символьное выражение
            parsed_formula = latex2sympy(formula, conf=None)
            return str(parsed_formula)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Ошибка парсинга LaTeX: {str(e)}")
        
    @staticmethod
    def parse_latex_from_text(text: str) -> List[str]:
        """Автоматический поиск формул LaTeX и обычных математических формул в тексте и их парсинг"""
        
        # Регулярное выражение для поиска формул LaTeX между $...$ или $$...$$
        latex_formulas = re.findall(r'\$.*?\$', text)
        
        # Регулярное выражение для поиска обычных математических выражений
        simple_formulas = re.findall(r'[a-zA-Z0-9\+\-\*/\^\(\)\=]+', text)

        # Объединяем найденные формулы
        formulas = latex_formulas + simple_formulas
        
        if not formulas:
            raise HTTPException(status_code=400, detail="Формулы не найдены.")
        
        parsed_formulas = []
        
        # Преобразуем каждую формулу LaTeX или обычную математическую в символьное выражение
        for formula in formulas:
            try:
                # Убираем знаки $ вокруг LaTeX формул
                if formula.startswith('$') and formula.endswith('$'):
                    formula = formula.strip('$')
                # Преобразуем формулу в символьное выражение
                parsed_formula = parse_latex_lark(formula)
                parsed_formulas.append(str(parsed_formula))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Ошибка при парсинге формулы: {str(e)}")
        
        return parsed_formulas
    

    @staticmethod
    def create_diagram(formula: str) -> str:
        """Создание диаграммы из формулы"""
        try:
            labels = ["A", "B", "C", "D"]
            values = [eval(formula.replace("x", str(i))) for i in range(1, 5)]
            plt.figure(figsize=(6, 4))
            plt.bar(labels, values, color="skyblue")
            plt.title("Диаграмма")
            plt.xlabel(formula)
            plt.ylabel("Значение")
            filename = f"{uuid.uuid4()}.png"
            filepath = os.path.join(IMAGE_DIR, filename)
            plt.savefig(filepath)
            plt.close()
            return filename
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @staticmethod
    def create_graph(formula: str) -> str:
        """Создание графика из формулы"""
        try:
            sympy_expr = FormulaProcessor.parse_latex_from_text(formula)
            f = lambdify("x", sympy_expr, modules=["numpy"])
            x = [ii/10 for ii in range(-100, 100)]
            y = [f(ii) for ii in x]
            plt.figure(figsize=(6, 4))
            plt.plot(x, y, label=formula, color="blue")
            plt.axhline(0, color="black", linestyle="--")
            plt.axvline(0, color="black", linestyle="--")
            plt.title("График")
            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.legend()
            filename = f"{uuid.uuid4()}.png"
            filepath = os.path.join(IMAGE_DIR, filename)
            plt.savefig(filepath)
            plt.close()
            return filepath
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        