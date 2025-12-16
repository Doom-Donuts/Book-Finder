import sqlite3
from Backend.Logger import main_logger
from path_fix import resource_path

#A list of valid tables to read from
TABLE_NAMES = {"BOOKS", "BOOK_INFO", "READING_GOALS", "WISHLIST", "YEARS", "BOOK_CATEGORIES", "REVIEWS"}

class BooksTable:
    def __init__(self):
        # Initialize connection to the database file
        self.db_path = resource_path('Backend/Books_Database/BooksDatabase.db')
        self.conn = sqlite3.connect(self.db_path,check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # This allows column access by name

    def select_query(self, table, filters=None, like_filters=None, columns="*", limit=None):
        #Function to create select queries for each function below
        if table not in TABLE_NAMES:
            raise ValueError(f"Invalid table '{table}'")

        parameters = []
        query = f"SELECT {columns} FROM {table} WHERE 1=1 "

       
        if filters:
            for col, value in filters.items():
                query += f"AND \"{col}\" = ? "
                parameters.append(value)

       
        if like_filters:
            for col, value in like_filters.items():
                query += f"AND \"{col}\" LIKE ? "
                parameters.append(f"%{value}%")

        
        if limit is not None:
            query += f"LIMIT {limit}"

        main_logger.Log(f"{query},{parameters}")
        return query, parameters


    def fetch_books(self,id_filter=None,name_filter=None,limit=None):
        #Fetch all rows from the a table and return them as a list of dictionaries.
        filters = {}
        like_filters = {}

        if id_filter is not None:
            filters["book_id"] = id_filter

        if name_filter is not None:
            like_filters["Title"] = name_filter

        query, params = self.select_query(
            table="BOOKS",
            filters=filters,
            like_filters=like_filters,
            limit=limit
        )

        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    
    #Fetch rows from BOOK_INFO table based on the given filters.
    def fetch_book_info(self, id_filter=None, year_filter=None, genre_filter=None, limit=None):
        filters = {}

        if id_filter is not None:
            filters["book_id"] = id_filter

        if genre_filter is not None:
            filters["Category"] = genre_filter

        if year_filter is not None:
            filters["Publish Date (Year)"] = year_filter

        query, params = self.select_query(
            table="BOOK_INFO",
            filters=filters,
            limit=limit
        )

        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    #Function to fetch categories from the BOOK_CATEGORIES table
    def fetch_book_category(self, id_filter=None, column="book_id", category=None, limit=None):
        filters = {}

        if category is not None:
            filters["category"] = category

        if id_filter is not None:
            filters["book_id"] = id_filter

        query, params = self.select_query(
            table="BOOK_CATEGORIES",
            filters=filters,
            columns=column,
            limit=limit
        )

        cursor = self.conn.execute(query, params)
        return [row[column] for row in cursor.fetchall()]

    def fetch_books_with_year(self, year_filter=None, limit=None):
        filters = {}

        if year_filter is not None:
            filters["year"] = year_filter

        query, params = self.select_query(
            table="YEARS",
            filters=filters,
            columns="book_id",
            limit=limit
        )

        cursor = self.conn.execute(query, params)
        return [row["book_id"] for row in cursor.fetchall()]

    def add_review(self, book_id, review_score, review_text):
        with self.conn:
            cursor = self.conn.cursor()
            query = "INSERT INTO REVIEWS(book_id, score, text) VALUES (?, ?, ?);"
            parameters = [book_id, review_score, review_text]
            main_logger.Log(f"{query},{parameters}")
            cursor.execute(query, parameters)
            return None

    def edit_review(self, book_id, review_score, review_text):
        with self.conn:
            cursor = self.conn.cursor()
            query = "UPDATE REVIEWS SET score = ?, text = ? WHERE book_id = ?;"
            parameters = [review_score, review_text, book_id]
            main_logger.Log(f"{query},{parameters}")
            cursor.execute(query, parameters)
            return None

    def fetch_review_info(self, id_filter=None, limit=None):
        filters = {}

        if id_filter is not None:
            filters["book_id"] = id_filter

        query, params = self.select_query(
            table="REVIEWS",
            filters=filters,
            limit=limit
        )

        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
            