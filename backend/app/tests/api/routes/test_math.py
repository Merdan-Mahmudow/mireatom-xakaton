import os
import unittest
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient

from app.api.routes.math import router, IMAGE_DIR  # Adjust import path as needed
from app.api.hooks.math import FormulaProcessor


class TestMathRoutes(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(router)
        os.makedirs(IMAGE_DIR, exist_ok=True) # Ensure directory exists

    def tearDown(self):
        # Clean up any generated image files
        for filename in os.listdir(IMAGE_DIR):
            file_path = os.path.join(IMAGE_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error during cleanup: {e}")
        os.rmdir(IMAGE_DIR)


    @patch.object(FormulaProcessor, 'create_diagram')
    def test_process_formula_diagram_success(self, mock_create_diagram):
        mock_create_diagram.return_value = os.path.join(IMAGE_DIR, "diagram.png")
        response = self.client.post("/process-formula", json={"formula": "x**2", "type": "diagram"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"image_url": "/images/diagram.png"})
        mock_create_diagram.assert_called_once_with("x**2")


    @patch.object(FormulaProcessor, 'create_graph')
    def test_process_formula_graph_success(self, mock_create_graph):
        mock_create_graph.return_value =  os.path.join(IMAGE_DIR, "graph.png")
        response = self.client.post("/process-formula", json={"formula": "x+2", "type": "graph"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"image_url": "/images/graph.png"})
        mock_create_graph.assert_called_once_with("x+2")

    def test_process_formula_invalid_type(self):
        response = self.client.post("/process-formula", json={"formula": "x+2", "type": "invalid"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Неверный тип объекта"})




    def test_get_image_success(self):
        # Create a dummy image file
        image_path = os.path.join(IMAGE_DIR, "test_image.png")
        with open(image_path, "wb") as f:
            f.write(b"dummy image content")

        response = self.client.post("/images/test_image.png")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"dummy image content")  # Check if the content is correct
        self.assertEqual(response.headers["content-type"], "image/png")



    def test_get_image_not_found(self):
        response = self.client.post("/images/non_existent_image.png")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Изображение не найдено"})

    @patch('app.api.routes.math.FormulaProcessor')
    def test_parse_latex_file(self, mock_processor):
        # Мокируем файл
        mock_file = Mock()
        mock_file.read.return_value = b'x^2 + y^2 = r^2'
        
        # Мокируем метод parse_latex_from_text
        mock_processor.parse_latex_from_text.return_value = ['x^2', 'y^2', 'r^2']

        response = self.client.post("/parse-latex-file", files={"file": ("filename", mock_file)})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'formulas': ['x^2', 'y^2', 'r^2']})


if __name__ == "__main__":
    unittest.main()

