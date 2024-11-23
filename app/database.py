import json
from pathlib import Path

from app.models import Author, Book


class JsonDB:
    """Класс для управления БД """

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.data = {"authors": [], "books": []}
        self._load()

    def _load(self):
        """Загрузка данных из файла"""
        if self.db_path.exists():
            with open(self.db_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        else:
            self._save()

    def _save(self):
        """Сохранение данных в файл"""
        with open(self.db_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def _get_collection(self, entity_type: str) -> list[dict]:
        match entity_type:
            case "authors":
                return self.data["authors"]
            case "books":
                return self.data["books"]
            case _:
                raise ValueError(f"Неподдерживаемый тип сущности '{entity_type}'.")

    def add_entity(self, entity_type: str, entity: Author | Book):
        """Добавить сущность (автора или книгу)."""
        collection = self._get_collection(entity_type)
        collection.append(entity.to_dict())
        self._save()

    def update_entity(self, entity_type: str, entity: Author | Book):
        """Обновить сущность (автора или книгу)."""
        collection = self._get_collection(entity_type)
        for idx, item in enumerate(collection):
            if item["id"] == entity.id:
                collection[idx] = entity.to_dict()
                self._save()
                return
        raise ValueError(f"Entity with ID {entity.id} not found in {entity_type}.")

    def delete_entity(self, entity_type: str, entity_id: str):
        """Удалить сущность (автора или книгу)."""
        collection = self._get_collection(entity_type)
        for idx, item in enumerate(collection):
            if item["id"] == entity_id:
                del collection[idx]
                self._save()
                return
        raise ValueError(f"Entity with ID {entity_id} not found in {entity_type}.")

    def get_entity(self, entity_type: str, entity_id: str) -> dict:
        """Получить сущность (автора или книгу) по ID."""
        collection = self._get_collection(entity_type)
        for item in collection:
            if item["id"] == entity_id:
                return item
        raise ValueError(f"Entity with ID {entity_id} not found in {entity_type}.")