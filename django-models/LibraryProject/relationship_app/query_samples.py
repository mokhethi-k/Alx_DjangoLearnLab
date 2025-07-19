from relationship_app.models import Author, Book, Library, Librarian
def book_by_author(author_name):
    author = Author.objects.get(name=author_name) 
    books = Book.objects.filter(author=author)     
    for book in books:
        print(book.title)


def All_books(library_name):
    library = Library.objects.get(name= library_name)
    for book in library.books.all():
        print(book.books)

def librarian_for_library(library_name):
    library = Library.objects.get(name = library_name)
    librarian = Librarian.objects.filter(library=library)
    print(librarian.name)