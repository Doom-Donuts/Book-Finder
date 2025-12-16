from Backend.BooksTable import BooksTable
import Backend.Buisness_Logic

#Unit tests for BooksTable
class Test_BooksTable():
  #Test covering select_query
  def test_sq(self):
    filters = {}
    like_filters = {}
    filters["book_id"] = 1
    like_filters["Title"] = "Goat Brothers"
    books = BooksTable()

    query, parameters = books.select_query("BOOKS", filters, like_filters, 10)
    assert query == "SELECT 10 FROM BOOKS WHERE 1=1 AND \"book_id\" = ? AND \"Title\" LIKE ? "
    assert parameters == [1, "%Goat Brothers%"]

  #Test covering fetch_books
  def test_fb(self):
    books = BooksTable()
    rows = books.fetch_books(2, "The Missing Person", 50)
    expected_ans= [{"book_id": 2, "Title": "The Missing Person", "Authors": "By Grumbach, Doris"}]
    assert rows == expected_ans

  #Test covering fetch_book_info
  def test_fb_info(self):
    books = BooksTable()
    rows = books.fetch_book_info(10, 1986, " Cooking , General", 20) #Isn't working with just 1 of the categories
    expected_ans = [{"book_id": 10, "Description": "", "Category": " Cooking , General", "Publisher": "Oxmoor House", "Price Starting With ($)": "12.98", "Publish Date (Month)": "June", "Publish Date (Year)": "1986"}]
    assert rows == expected_ans

  #Test covering fetch_book_category
  def test_fbc(self):
    books = BooksTable()
    rows = books.fetch_book_category(2, "book_id", "Fiction",  10) #Book 2 has Fiction and General categories
    expected_ans= [2]
    assert rows == expected_ans

"""
  #Test covering fetch_books_with_year
  def test_fb_year(self):
    assert 1

  #Test covering add_review
  def test_add_review(self):
    assert 1

  #Test covering edit_review
  def test_edit_review(self):
    assert 1

  #Test covering fetch_review_info
  def test_fr(self):
    assert 1
"""

class Test_BusinessLogic():
  #Test covering get_books_unfiltered
  def gbu():
    assert 0