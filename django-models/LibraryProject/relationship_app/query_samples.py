from relationship_app.models import Author, Book, Library, Librarian
def book_by_author(author_name):
    books = Book.objects.filter(author__name = author_name)
    for book in books:
        print(book.title)


def All_books(library_name):
    library = Library.objects.get(name= library_name)
    for book in library.books.all():
        print(book.books)

def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    print(library.librarian.name)