import sqlite3
import pandas as pd
from path_fix import resource_path
from Backend.Logger import main_logger

def book_category(conn):
    cursor = conn.cursor()
    query = "SELECT book_id, Category FROM BOOK_INFO"
    cursor.execute(query)
    result = cursor.fetchall()
    query_list = []

    for item in result:
        book_id = int(item[0])
        book_list_string = item[1]
        
        if book_list_string is not None:
            new_book_list = book_list_string.split(",")            
            for i in range(len(new_book_list)):
                category = new_book_list[i].strip()
                query_list.append([book_id, category])

    new_query = "INSERT INTO BOOK_CATEGORIES (\"book_id\", \"category\") VALUES (?, ?)"

    for parameters in query_list:
        cursor.execute(new_query, parameters)

def fill_database():
    df = pd.read_csv(resource_path("Backend/Books_Database/BooksDatasetClean.csv"))
    df.loc[df["Category"] == " Religion , Religion, Politics & State", "Category"] = "Religion, Politics & State"


    conn = sqlite3.connect(resource_path('Backend/Books_Database/BooksDatabase.db'))
    cursor = conn.cursor()

    #BOOKS
    cursor.execute("SELECT COUNT(*) FROM 'BOOKS'")
    BOOKS_is_empty = cursor.fetchone()[0] == 0

    if BOOKS_is_empty:
        db_books = df[["Title", "Authors"]]
        db_books.to_sql('BOOKS', conn, if_exists='append', index=False)
    else:
        main_logger.Log("BOOKS is already full")

    #BOOK_INFO
    cursor.execute("SELECT COUNT(*) FROM 'BOOK_INFO'")
    BOOK_INFO_is_empty = cursor.fetchone()[0] == 0

    if BOOK_INFO_is_empty:
        db_book_info = df[["Description", "Category", "Publisher", "Price Starting With ($)", "Publish Date (Month)", "Publish Date (Year)"]]
        db_book_info.to_sql('BOOK_INFO', conn, if_exists='append', index=False)
    else:
        main_logger.Log("BOOK_INFO is already full")

    #CATEGORIES
    cursor.execute("SELECT COUNT(*) FROM 'BOOK_CATEGORIES'")
    BOOK_CATEGORIES_is_empty = cursor.fetchone()[0] == 0

    if BOOK_CATEGORIES_is_empty:
        book_category(conn)
    else:
        main_logger.Log("BOOK_CATEGORIES is already full")


    #YEARS
    cursor.execute("SELECT COUNT(*) FROM 'YEARS'")
    BOOK_INFO_is_empty = cursor.fetchone()[0] == 0

    if BOOK_INFO_is_empty:
        df.rename(columns={'Publish Date (Year)': 'year'}, inplace=True)
        db_years = df["year"]
        db_years.to_sql('YEARS', conn, if_exists='append', index=False)
    else:
        main_logger.Log("YEARS is already full")

    conn.close()

def clear_db():
    conn = sqlite3.connect(resource_path('Backend/Books_Database/BooksDatabase.db'))
    cursor = conn.cursor()

    #BOOKS
    cursor.execute("DELETE FROM BOOKS")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='BOOKS'")

    cursor.execute("DELETE FROM BOOK_INFO")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='BOOK_INFO'")

    cursor.execute("DELETE FROM BOOK_CATEGORIES")

    cursor.execute("DELETE FROM YEARS")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='YEARS'")

    conn.commit()
    conn.close()

