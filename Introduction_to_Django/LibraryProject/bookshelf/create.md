>>> from bookshelf.models import Book
>>> book1 = Book.objects.create(title = '1984', author = 'George Orwell', publication_year = 1949)
>>> # This indicate that the Book instance has been created successfully 

>>> book1.save()
>>> 