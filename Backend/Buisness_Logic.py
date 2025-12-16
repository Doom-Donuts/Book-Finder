from Backend.BooksTable import BooksTable
import random

#Get the book data without using and filtering.
def get_books_unfiltered():
    return BooksTable().fetch_books(limit=100)

#Get the full information for a particular book
def fetch_book_info(book):
    #Get the id of the currently selected book
    book_id = book["book_id"]
    #get the info associated with that book. fetch_book_info returns a list so grab the first item in that list
    extra_info = BooksTable().fetch_book_info(id_filter=book_id)[0]
    #gets the review info for the book
    review_info_list = BooksTable().fetch_review_info(id_filter=book_id)
    #Add data from extra_info to book. Basically we're just combining the dictionaries here
    extra_info.update(book)
    #Gets the first review from the list, or sets score and text to empty strings if the list is empty
    if(len(review_info_list) > 0):
        review_info = review_info_list[0]
    else:
        review_info = {"score": "", "text": ""}
    extra_info.update(review_info)
    return extra_info

def Add_Review(book_id, review_score, review_text):
    if(not isinstance(book_id, int)):
        print("Book id needs to be a whole number")
    if(not isinstance(review_score, float)):
        print("Review score needs to be a number")
    BooksTable().add_review(book_id, review_score, review_text)
    return {"book_id": book_id, "score": review_score, "text": review_text}

def Fetch_Review(book_id):
    if(not isinstance(book_id, int)):
        print("Book id needs to be a whole number")

    #gets the review info for the book
    review_info_list = BooksTable().fetch_review_info(id_filter=book_id)
    #Gets the first review from the list, or sets score and text to empty strings if the list is empty
    if(len(review_info_list) > 0):
        review_info = review_info_list[0]
    else:
        review_info = {"score": "", "text": ""}
    return review_info


def Edit_Review(book_id, review_score, review_text):
    if(not isinstance(book_id, int)):
        print("Book id needs to be a whole number")
    if(not isinstance(review_score, float)):
        print("Review score needs to be a number")
    BooksTable().edit_review(book_id, review_score, review_text)
    return {"book_id": book_id, "score": review_score, "text": review_text}

def Search_Books(text):
    return(BooksTable().fetch_books(name_filter = text, limit=100))

def apply_filters(genre, year):
 
    return_list = []

    if genre is None and year is None:
        #grab data unfiltered
        return get_books_unfiltered()
    
    if genre is None:
        year_data = BooksTable().fetch_books_with_year(year_filter = year)
        year_and_genre = year_data

    if year is None:
        genre_data = BooksTable().fetch_book_category(category=genre)
        year_and_genre = genre_data

    else:
        year_data = BooksTable().fetch_books_with_year(year_filter = year)
        genre_data = BooksTable().fetch_book_category(category = genre)
        year_and_genre = list(set(genre_data).intersection(set(year_data)))

    for book in year_and_genre[:100]:
        return_list.append(BooksTable().fetch_books(id_filter=book)[0])

    return return_list

#Simple book reccomendation system.
#Just takes the highest review score and finds books that share a category
def recommend_books():
    book_reviews = BooksTable().fetch_review_info()
    #sort by score
    book_reviews.sort(key=lambda x: x["score"], reverse=True)
    
    most_liked_id = book_reviews[0]["book_id"]

    most_liked_categories = BooksTable().fetch_book_category(id_filter=most_liked_id, column="category")

    output_ids = []
    for category in most_liked_categories:
        output_ids.extend(BooksTable().fetch_book_category(category=category,limit=100))

    #Shuffle the ids to make sure they aren't dominated by one category
    random.seed(42)
    random.shuffle(output_ids)

    return_list = []
    for book in output_ids[:100]:
        return_list.append(BooksTable().fetch_books(id_filter=book)[0])

    return return_list
    


