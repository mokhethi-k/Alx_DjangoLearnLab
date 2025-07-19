from relationship_app.models import Author, Book, Library, Librarian
def book_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    return books


def All_books(library_name):
    library = Library.objects.get(name= library_name)
    for book in library.books.all():
        print(book.title)

def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)