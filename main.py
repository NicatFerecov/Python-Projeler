import json
import os
import asyncio

class Book:
    def __init__(self, author, title, page: int, isbn):
        self.author=author
        self.title=title
        self.page=page
        self.isbn=isbn



    async def save_to_file(self, filename):
        data = {
            "Author": self.author,
            "Title": self.title,
            "Page": self.page,
            "ISBN": self.isbn
        }
        # Async file write
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._write_json, filename, data)
        print(f"{self.title} Added!")

    def _write_json(self, filename, data):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @classmethod
    async def load_from_file(cls, filename):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, cls._read_json, filename)
        return cls(
            author=data.get("Author"),
            title=data.get("Title"),
            page=data.get("Page"),
            isbn=data.get("ISBN")
        )

    @staticmethod
    def _read_json(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    async def list_books():
        loop = asyncio.get_event_loop()
        books = await loop.run_in_executor(None, lambda: [f for f in os.listdir() if f.endswith('.json')])
        if not books:
            print("No books found.")
        else:
            print("Books:")
            for book in books:
                print(f"- {book[:-5]}")

    @staticmethod
    async def search_books_by_author(author_name):
        """
        Asenkron olarak tüm kitap dosyalarını tarar ve yazar adına göre arama yapar.
        """
        loop = asyncio.get_event_loop()
        books = await loop.run_in_executor(None, lambda: [f for f in os.listdir() if f.endswith('.json')])
        found = []
        for book_file in books:
            data = await loop.run_in_executor(None, Book._read_json, book_file)
            if data.get("Author", "").lower() == author_name.lower():
                found.append(data.get("Title", book_file[:-5]))
        if found:
            print(f"Books by '{author_name}':")
            for title in found:
                print(f"- {title}")
        else:
            print(f"No books found by '{author_name}'.")

async def main():
    USERS = {
        "admin": "1234",
        "nicat": "abcd"
    }

    async def login():
        print("Login required!")
        for _ in range(3):
            username = input("Username: ")
            password = input("Password: ")
            if USERS.get(username) == password:
                print(f"Welcome, {username}!")
                return True
            else:
                print("Invalid credentials.")
        print("Too many failed attempts. Exiting...")
        return False

    logged_in = await login()
    if not logged_in:
        return

    while True:
        print("1 Add book")
        print("2. View book")
        print("3. List books")
        print("4. Search books by author")
        print("5. Exit")

        choice = input("What's Your Choice?: ")

        if choice == "1":
            author = input("Name a author: ")
            title = input(f"Name the {author} Book: ")
            page = input(f"Page the {title}: ")
            isbn = input("ISBN: ")

            manage = Book(author, title, page, isbn)
            await manage.save_to_file(f"{title}.json")

        elif choice == "2":
            name = input("Name a book: ")

            try:
                book = await Book.load_from_file(f"{name}.json")
                print(f"Author: {book.author}")
                print(f"Title: {book.title}")
                print(f"Page: {book.page}")
                print(f"ISBN: {book.isbn}")
            except FileNotFoundError:
                print("Book not found.")

        elif choice == "3":
            await Book.list_books()

        elif choice == "4":
            author_name = input("Enter author name to search: ")
            await Book.search_books_by_author(author_name)

        elif choice == "5":
            print("Exiting...")
            break


if __name__ == "__main__":
    asyncio.run(main())