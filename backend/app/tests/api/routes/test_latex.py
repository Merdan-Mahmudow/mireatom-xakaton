import os
import unittest

from fastapi import UploadFile
from fastapi.testclient import TestClient

from app.api.routes.latex import router
from app.schemas import EditRequest, ConvertRequest
from app.api.hooks.latex import Latex





class TestLatexRoutes(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.latex = Latex()  # Replace with your actual Latex class
        self.test_docx_file = os.path.abspath("./app/pandoc_test1.docx") # Replace with an actual test docx file
        self.test_doc_file = os.path.abspath("./app/pandoc_test2.doc") # Replace with an actual test doc file



    async def test_upload_file_docx_success(self):
        with open(self.test_docx_file, "rb") as f:
            file = UploadFile("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response = await self.client.post("/upload", files={"file": file})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        os.remove(os.path.join("uploads", "test.docx")) # Clean up
        os.remove(os.path.join("latex_files", "test.tex"))


    async def test_upload_file_doc_success(self):
        with open(self.test_doc_file, "rb") as f:
            file = UploadFile("test.doc", f, "application/msword")
            response = await self.client.post("/upload", files={"file": file})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        os.remove(os.path.join("uploads", "test.doc")) # Clean up
        os.remove(os.path.join("latex_files", "test.tex"))


    async def test_upload_file_invalid_type(self):
        with open(__file__, "rb") as f:  # Use a python file as an invalid type
            file = UploadFile("test.txt", f, "text/plain")
            response = await self.client.post("/upload", files={"file": file})

        self.assertEqual(response.status_code, 200)  # Should return 200 with an error message
        self.assertEqual(response.json(), {"error": f"Файл 'test.txt' не является допустимым файлом Word."})



    async def test_get_all_files(self):
        # Create dummy files
        with open(os.path.join("latex_files", "test1.tex"), "w") as f:
            f.write("test")
        with open(os.path.join("latex_files", "test2.tex"), "w") as f:
            f.write("test")

        response = await self.client.get("/get-all-files")
        self.assertEqual(response.status_code, 200)
        self.assertIn("test1.tex", response.json())
        self.assertIn("test2.tex", response.json())

        # Clean up
        os.remove(os.path.join("latex_files", "test1.tex"))
        os.remove(os.path.join("latex_files", "test2.tex"))



    async def test_get_latex_success(self):

        with open(os.path.join("latex_files", "test.tex"), "w", encoding="utf-8") as f:
            f.write("latex content")


        response = await self.client.get("/get-latex?file_name=test.tex")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"latex_content": "latex content"})

        os.remove(os.path.join("latex_files", "test.tex"))


    # ... (tests for other routes using the same pattern)


    async def test_update_latex(self):
        file_name = "updated_latex_test"
        file_path = os.path.join("latex_files", file_name + ".tex")

        # Create a dummy LaTeX file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Initial LaTeX content")


        edit_request = EditRequest(file_name=file_name, latex_content="Modified LaTeX content")
        response = await self.client.put("/update-latex", json=edit_request.model_dump())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {"status": "success", "details": f"Файл '{file_name}' успешно обновлен."})

        # Verify the changes in the file.
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        self.assertEqual(file_content, "Modified LaTeX content")

        os.remove(file_path)

    #More tests for negative outcomes should be added as needed for all API calls.



    async def test_convert_latex_to_word(self):
        convert_request = ConvertRequest(latex_code="Some LaTeX code")
        response = await self.client.post("/convert-latex-to-word", json=convert_request.model_dump())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"word_content": "Конвертированный текст из LaTeX: Some LaTeX code"})


if __name__ == "__main__":
    unittest.main()
