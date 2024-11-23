from pathlib import Path
from app.database import JsonDB
from app.utils import (
    add_book,
    delete_book,
    search_books,
    display_all_books,
    update_book_status,
)

DB_PATH = Path("db.json")


def show_menu():
    """Вывод меню приложения."""
    print("\nМеню:")
    print("1. Добавить книгу")
    print("2. Удалить книгу")
    print("3. Искать книги")
    print("4. Отобразить все книги")
    print("5. Обновить статус книги")
    print("6. Выход")


def main():
    """Главная функция приложения."""
    db = JsonDB(DB_PATH)
    while True:
        show_menu()
        choice = input("\nВведите номер действия: ").strip()
        match choice:
            case "1":
                add_book(db)
            case "2":
                delete_book(db)
            case "3":
                search_books(db)
            case "4":
                display_all_books(db)
            case "5":
                update_book_status(db)
            case "6":
                print("Выход из приложения...")
                break
            case _:
                print("Некорректный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
