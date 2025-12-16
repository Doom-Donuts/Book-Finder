import sqlite3

path = "BooksDatabase.db"

conn = sqlite3.connect(path)

cursor = conn.cursor()

query = "SELECT book_id, Category FROM BOOK_INFO"

cursor.execute(query)

result = cursor.fetchall()

query_list = []

for item in result:
    book_id = int(item[0])
    book_list_string = item[1]

    new_book_list = book_list_string.split(",")
    
    for i in range(len(new_book_list)):
        category = new_book_list[i].strip()
        query_list.append([book_id, category])



new_query = "INSERT INTO BOOK_CATEGORIES_2 (\"book_id\", \"category\") VALUES (?, ?)"

for parameters in query_list:
    print(parameters)
    cursor.execute(new_query, parameters)

conn.commit()
