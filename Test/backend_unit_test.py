import pytest
import sqlite3
from path_fix import resource_path
from Backend.BooksTable import BooksTable
import Backend.Buisness_Logic as Logic

#Unit tests for functions in BooksTable(with parameters(except self) in parentheses above the test)
class Test_BooksTable():
  #Some functions will only return one book when given book_id
  #So, these tests are hard coded with specific info of that book

  #Test covering select_query(table,filters=None,like_filters=None,columns="*",limit=None)
  def test_sq(self):
    filters = {}
    like_filters = {}
    filters["book_id"] = 1 #Using this means only one book is returned
    like_filters["Title"] = "Goat Brothers"
    col = "Title"
    books = BooksTable()

    query, parameters = books.select_query("BOOKS", filters, like_filters, col, 10)
    assert query == "SELECT Title FROM BOOKS WHERE 1=1 AND \"book_id\" = ? AND \"Title\" LIKE ? LIMIT 10"
    assert parameters == [1, "%Goat Brothers%"]

  #Test ensuring an error is reported if the wrong table name is given in select_query
  def test_sq_wrong_name(self):
    books = BooksTable()
    with pytest.raises(ValueError, match="Invalid table \'CAT\'"):
      books.select_query("CAT")

  #Test covering fetch_books(id_filter=None,name_filter=None,limit=None)
  def test_fb(self):
    books = BooksTable()
    #the first parameter is book_id, so using it means only 1 book is returned
    rows = books.fetch_books(2, "The Missing Person", 50)
    expected_ans= [{"book_id": 2, "Title": "The Missing Person", "Authors": "By Grumbach, Doris"}]
    assert rows == expected_ans

  #Test covering fetch_book_info(id_filter=None,year_filter=None,genre_filter=None,limit=None)
  def test_fb_info(self):
    books = BooksTable()
    #the first parameter is book_id, so using it means only 1 book is returned
    rows = books.fetch_book_info(10, 1986, " Cooking , General", 20) #Isn't working with just 1 of the categories
    expected_ans = [{"book_id": 10, "Description": None, "Category": " Cooking , General", "Publisher": "Oxmoor House", "Price Starting With ($)": "12.98", "Publish Date (Month)": "June", "Publish Date (Year)": "1986"}]
    assert rows == expected_ans

  #Test covering fetch_book_category(id_filter=None,column="book_id",category=None,limit=None)
  def test_fbc(self):
    books = BooksTable()
    #the first parameter is book_id, so using it means only 1 book is returned
    rows = books.fetch_book_category(2, "book_id", "Fiction",  10) #Book 2 has Fiction and General categories
    expected_ans= [2]
    assert rows == expected_ans

  #Test covering fetch_books_with_year(year_filter=None, limit=None)
  def test_fb_year(self):
    books = BooksTable()
    rows = books.fetch_books_with_year(1986, 10)
    assert len(rows) == 10

#Unit tests covering functions in Bussiness_Logic(with parameters in parentheses above the test)
class Test_BusinessLogic():
  #Test covering get_books_unfiltered()
  def test_gbu(self):
    assert len(Logic.get_books_unfiltered()) == 100

  #Test covering fetch_book_info(book)
  def test_fetch_book_info(self):
    expected_ans = {"book_id": 10, "Description": None, "Category": " Cooking , General", "Publisher": "Oxmoor House", "Price Starting With ($)": "12.98", "Publish Date (Month)": "June", "Publish Date (Year)": "1986", "score": "", "text": ""}
    assert Logic.fetch_book_info({"book_id": 10}) == expected_ans

  #Test covering Add_Review(book_id, review_score, review_text)
  def test_ar(self):
    expected_ans = {"book_id": 1, "score": 9, "text": "Great Book"}
    assert Logic.Add_Review(1, 9, "Great Book") == expected_ans

  #Test covering Fetch_Review(book_id) if there is a review
  def test_fr_exist(self):
    expected_ans = {"book_id": 1, "score": 9, "text": "Great Book"}
    assert Logic.Fetch_Review(1) == expected_ans

  #Test covering Fetch_Review(book_id) if there is not a review
  def test_fr_exist(self):
    expected_ans = {"score": "", "text": ""}
    assert Logic.Fetch_Review(2) == expected_ans

  #Test covering Edit_Review(book_id, review_score, review_text)
  def test_er(self):
    expected_ans = {"book_id": 1, "score": 10, "text": "Amazing Book"}
    assert Logic.Edit_Review(1, 10, "Amazing Book") == expected_ans

  #Test covering Search_Books(text)
  def test_Search_Books(self):
    expected_ans= [{"book_id": 2, "Title": "The Missing Person", "Authors": "By Grumbach, Doris"}]
    assert Logic.Search_Books("The Missing Person") == expected_ans

  #Test covering apply_filters(genre, year) when there are no filters
  def test_af_none(self):
    assert len(Logic.apply_filters(None, None)) == 100

  #Test covering apply_filters(genre, year) when there is a genre filter
  def test_af_genre(self):
    assert len(Logic.apply_filters("General", None)) == 100

  #Test covering apply_filters(genre, year) when there is a year filter
  def test_af_year(self):
    assert len(Logic.apply_filters(None, 1986)) == 100

  #Test covering apply_filters(genre, year) when there is a genre and year filter
  def test_af_both(self):
    assert len(Logic.apply_filters("General", 1986)) == 100

  #Test covering recommend_books()
  def test_rb(self):
    assert len(Logic.recommend_books()) == 100
    self.delete_review(1)

  #Function to delete a test review
  def delete_review(self, book_id):
    #Have this part here since pytest doesn't like classes with init function
    # Initialize connection to the database file
    self.db_path = resource_path('Backend/Books_Database/BooksDatabase.db')
    self.conn = sqlite3.connect(self.db_path,check_same_thread=False)
    self.conn.row_factory = sqlite3.Row  # This allows column access by name

    with self.conn:
      cursor = self.conn.cursor()
      query = "DELETE FROM REVIEWS WHERE book_id = ?"
      param = [book_id]
      cursor.execute(query, param)
