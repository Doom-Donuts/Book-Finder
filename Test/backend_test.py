from Backend.BooksTable import Books

#Checks if fetch_all() returns a list with 100 items
def test_fetch_all_length():
  books = Books.fetch_all()
  assert len(books) == 100

#Checks if to_dict() returns a list with 100 items
def test_to_dict_length():
  books_dict = Books.to_dict()
  assert len(books_dict) == 100
