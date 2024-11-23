from app.database import JsonDB
from app.models import Author, Book


def add_book(db: JsonDB):
    """Добавить книгу в базу данных."""
    title = input("Введите название книги: ")
    author_name = input("Введите имя автора: ")
    year = int(input("Введите год издания: "))

    # Проверка существующего автора
    existing_author = None
    for author_data in db._get_collection("authors"):
        if author_data["name"] == author_name:
            existing_author = Author.from_dict(author_data)
            break

    # Если автора нет, создаем нового
    if not existing_author:
        new_author = Author(name=author_name)
        db.add_entity("authors", new_author)
        existing_author = new_author

    # Добавляем книгу
    new_book = Book(title=title, author_id=existing_author.id, year=year)
    db.add_entity("books", new_book)
    print(f"Книга '{title}' успешно добавлена.")


def delete_book(db: JsonDB):
    """Удалить книгу из базы данных."""
    book_id = input("Введите ID книги, которую нужно удалить: ")
    try:
        db.delete_entity("books", book_id)
        print(f"Книга с ID {book_id} успешно удалена.")
    except ValueError as e:
        print(e)


def search_books(db: JsonDB):
    """Найти книги по названию, автору или году."""
    print("Выберите критерий поиска:")
    print("1. Название")
    print("2. Автор")
    print("3. Год издания")
    choice = input("Введите номер критерия: ")

    search_query = input("Введите строку поиска: ")

    match choice:
        case "1":
            results = [book for book in db._get_collection("books") if search_query.lower() in book["title"].lower()]
        case "2":
            results = []
            for author in db._get_collection("authors"):
                if search_query.lower() in author["name"].lower():
                    author_books = [book for book in db._get_collection("books") if book["author_id"] == author["id"]]
                    results.extend(author_books)
        case "3":
            try:
                year = int(search_query)
                results = [book for book in db._get_collection("books") if book["year"] == year]
            except ValueError:
                print("Некорректный ввод года. Ожидалось число.")
                return []
        case _:
            print("Некорректный выбор.")
            return []

    if results:
        print("Найденные книги:")
        for book in results:
            author = db.get_entity("authors", book["author_id"])
            print(f"ID: {book['id']}, Название: {book['title']}, Автор: {author['name']}, Год: {book['year']}, Статус: {book['status']}")
    else:
        print("Книг по вашему запросу не найдено.")


def display_all_books(db: JsonDB):
    """Отобразить все книги."""
    books = db._get_collection("books")
    if not books:
        print("Библиотека пуста.")
        return

    print("Список всех книг:")
    for book in books:
        author = db.get_entity("authors", book["author_id"])
        print(f"ID: {book['id']}, Название: {book['title']}, Автор: {author['name']}, Год: {book['year']}, Статус: {book['status']}")


def update_book_status(db: JsonDB):
    """Обновить статус книги."""
    while True:
        book_id = input("Введите ID книги: ").strip()

        try:
            book_data = db.get_entity("books", book_id)
            break
        except ValueError:
            print(f"Книга с ID {book_id} не найдена. Попробуйте снова.")

    while True:
        new_status = input("Введите новый статус ('в наличии' или 'выдана'): ").strip()
        if new_status in {"в наличии", "выдана"}:
            break
        print("Некорректный статус. Возможные значения: 'в наличии', 'выдана'.")

    book = Book.from_dict(book_data)
    book.status = new_status
    db.update_entity("books", book)
    print(f"Статус книги с ID {book_id} обновлен на '{new_status}'.")
