from dataclasses import dataclass, asdict, field
from uuid import uuid4

@dataclass()
class Author:
    """Класс для представления автора"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default="")
    books: list[str] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "Author":
        """Создание экземпляра автора из словаря"""
        return Author(
            id=data['id'],
            name=data["name"],
            books=data.get("books", []),
        )

    def to_dict(self) -> dict:
        """Сериализация для упаковки в словарь"""
        return asdict(self)

    def add_book(self, book_id: str):
        """Добавление книги к уже существующему автору"""
        if book_id not in self.books:
            self.books.append(book_id)


@dataclass()
class Book:
    """Класс для представления книги"""
    author_id: str | None
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = field(default="")
    year: int = field(default=0)
    status: str = field(default="В наличии")

    @staticmethod
    def from_dict(data: dict) -> "Book":
        """Создание экземпляра книги из словаря"""
        return Book(
            id=data["id"],
            title=data["title"],
            year=data["year"],
            status=data["status"],
            author_id=data["author_id"],
        )

    def to_dict(self) -> dict:
        return asdict(self)