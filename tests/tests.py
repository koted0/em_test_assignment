import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

from app.database import JsonDB
from app.models import Book
from app.utils import update_book_status


class TestJsonDB(unittest.TestCase):
    def setUp(self):
        """Создание временной базы данных с тестовыми данными"""
        self.temp_db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = Path(self.temp_db_file.name)
        test_data = {
            "authors": [
                {"id": "auth1", "first_name": "Лев", "last_name": "Толстой", "middle_name": "Николаевич"},
                {"id": "auth2", "first_name": "Фёдор", "last_name": "Достоевский", "middle_name": "Михайлович"}
            ],
            "books": [
                {"id": "book1", "title": "Война и мир", "author_id": "auth1", "year": 1869, "status": "в наличии"},
                {"id": "book2", "title": "Преступление и наказание", "author_id": "auth2", "year": 1866, "status": "выдана"}
            ]
        }
        with open(self.temp_db_file.name, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=4)

        self.db = JsonDB(self.db_path)

    def tearDown(self):
        """Удаление временной базы данных"""
        self.temp_db_file.close()
        self.db_path.unlink()

    def test_get_entity(self):
        """Проверка получения сущностей"""
        author = self.db.get_entity("authors", "auth1")
        self.assertEqual(author["first_name"], "Лев")

        book = self.db.get_entity("books", "book1")
        self.assertEqual(book["title"], "Война и мир")

    def test_update_book_status(self):
        """Проверка обновления статуса книги"""
        book = self.db.get_entity("books", "book1")
        self.assertEqual(book["status"], "в наличии")

        book_obj = Book.from_dict(book)
        book_obj.status = "выдана"
        self.db.update_entity("books", book_obj)

        updated_book = self.db.get_entity("books", "book1")
        self.assertEqual(updated_book["status"], "выдана")


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.db = JsonDB("test_db.json")
        self.db.data = {
            "authors": [{"id": "auth1", "name": "Лев"}],
            "books": [
                {"id": "book1", "title": "Война и мир", "author_id": "auth1", "year": 1869, "status": "в наличии"}
            ]
        }
        self.db._save()

    def tearDown(self):
        self.db.db_path.unlink()  # Удаляем тестовый файл после выполнения тестов

    def test_update_book_status_interactive(self):
        """Тест интерактивного обновления статуса книги"""
        def mock_input(prompt):
            responses = {
                "Введите ID книги: ": "book1",  # ID книги
                "Введите новый статус ('в наличии' или 'выдана'): ": "выдана"  # Новый статус
            }
            return responses[prompt]

        with patch("builtins.input", mock_input):
            update_book_status(self.db)

        updated_book = self.db.get_entity("books", "book1")
        self.assertEqual(updated_book["status"], "выдана")


if __name__ == "__main__":
    unittest.main()