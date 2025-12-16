from __future__ import annotations

from PySide6.QtCore import Qt, Slot

from PySide6.QtWidgets import (
    QFormLayout, QVBoxLayout, QWidget, QLabel, QHBoxLayout
)

from UI.Widgets.input import LineInput, Button
from UI.Widgets.BookInfo import BookInfo
from UI.Widgets.TableModel import DictionaryTableModel
from UI.Widgets.TableView import TableView
from Backend.Signal import event_list
from Backend.async_worker import run_func_async
from Backend.Buisness_Logic import get_books_unfiltered, fetch_book_info, apply_filters, Search_Books, recommend_books
from Backend.Logger import main_logger

from Backend.Constants import CREATE_BOOKS_TABLE, UPDATE_BOOK_INFO

#This class is responsible for creating the UI for the search tab of the application
class SearchPage(QWidget):
    def __init__(self,parent): 
        super().__init__(parent=parent)

        #Create the book info panel
        self.book_info = BookInfo(parent=self)
        
        #Create a table view. Any time the table gets updated, a QAbstractTableItem will be constructed and and this gets pointed to that data
        self.table = TableView(parent=self)

        #This will get replaced when data is requested with the UPDATE_BOOKS_TABLE event
        self.table_model = None

        #Bottom half of the display. Has the table view on the left, and the book info panel on the right
        self.bottom = QHBoxLayout()
        self.bottom.addWidget(self.table)
        self.bottom.addWidget(self.book_info)

        #Create the search bar and filter form, then construct the UI using QHBoxLayouts and QVBoxLayouts
        self.createSearchBar()
        self.createFilterForm()
        self.buildLayout()
        self.setLayout(self.page_layout)

        #When return is pressed on the search input, run self.search_books
        self.search_input.returnPressed.connect(self.search_books)

        #when the filter button is clicked, run self.filter_books
        self.filter_button.clicked.connect(self.on_filter_books_clicked)

        #when reset button is clicked, run self.reset_books
        self.reset_button.clicked.connect(self.on_reset_books_clicked)

        self.recommend_books_button.clicked.connect(self.on_recommend_books_clicked)

        #when an item on the table is clicked, run self.on_row_clicked
        self.table.clicked.connect(self.on_row_clicked)
        self.show()

        #Create UPDATE_BOOKS_TABLE event
        event_list.create_event(CREATE_BOOKS_TABLE)
        #when run_func_async is called with UPDATE_BOOKS_TABLE, self.update_table will be run using the return values of the function.
        event_list.subscribe(CREATE_BOOKS_TABLE,result_funcs=[self.update_table])

        #Create UPDATE_BOOK_INFO event
        event_list.create_event(UPDATE_BOOK_INFO)
        event_list.subscribe(UPDATE_BOOK_INFO,result_funcs=[self.on_book_data_recieved])

        run_func_async(CREATE_BOOKS_TABLE,get_books_unfiltered)

    #Function is expecting an object to be returned from the function given to run_func_async()
    @Slot(object)
    def update_table(self, data):
        self.book_info.reset_book_info()
        #Give DictionaryTableModel the columns "Title" and "Authors", which will exclude the book_id variable from being shown.
        self.table_model = DictionaryTableModel(data,col_labels=['Title', 'Authors'])
        #Set the TableView to use the new data model 
        self.table.setModel(self.table_model)

    #Get data for book when the row is clicked
    def on_row_clicked(self,index):
        row = index.row()
        book_selected = self.table_model._data[row]
        run_func_async(UPDATE_BOOK_INFO, fetch_book_info, book_selected)

    #Function is expecting an object to be returned from the function given to run_func_async()
    @Slot(object)
    def on_book_data_recieved(self,data):
        self.book_info.set_book_info(data)

    def createSearchBar(self):
        self.search_input = LineInput()
        self.search_form = QFormLayout()
        self.search_form.addRow("Search:", self.search_input)

    def createFilterForm(self):
        self.options_label = QLabel("Filters")
        self.options_label.setAlignment(Qt.AlignCenter)
        self.genre_input = LineInput()
        self.year_input = LineInput()
        self.filter_form = QFormLayout()
        self.filter_form.addRow("Genre: ", self.genre_input)
        self.filter_form.addRow("Year: ", self.year_input)


        self.filter_button = Button("Filter")
        self.recommend_books_button = Button("Recommend Books")
        self.reset_button = Button("Reset")

        self.button_row = QHBoxLayout()
        self.button_row.addWidget(self.filter_button)
        self.button_row.addWidget(self.recommend_books_button)
        self.button_row.addWidget(self.reset_button)

    def buildLayout(self):
        self.page_layout = QVBoxLayout()
        self.page_layout.addWidget(self.options_label)
        self.page_layout.addLayout(self.filter_form)
        self.page_layout.addLayout(self.button_row)
        self.page_layout.addLayout(self.search_form)
        self.page_layout.addLayout(self.bottom)

    def search_books(self):
        text = self.search_input.text()
        #don't search if there is nothing in the search bar.
        if text != "":
            main_logger.Log(f"Searching for: \"{text}\"")
            run_func_async(CREATE_BOOKS_TABLE, Search_Books, text)

    def on_filter_books_clicked(self):
        genre_text = self.genre_input.text()
        if genre_text == '':
            genre_text = None

        year_text = self.year_input.text()
        if year_text == '':
            year_text = None

        #don't filter if there's nothing inputted
        if year_text is not None or genre_text is not None:
            run_func_async(CREATE_BOOKS_TABLE, apply_filters, genre_text, year_text)

    def on_reset_books_clicked(self):
        run_func_async(CREATE_BOOKS_TABLE,get_books_unfiltered)

    def on_recommend_books_clicked(self):
        run_func_async(CREATE_BOOKS_TABLE, recommend_books)
    
        

        
