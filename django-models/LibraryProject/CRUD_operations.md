from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year="1949")

print(book)
book = Book.objects.get(title="1984")

print(f"Title: {book.tile}, Author: {book.author}, Year: {book.publication_year})
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
book.delete()
print(Book.objects.all())
