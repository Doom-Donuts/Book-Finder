from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSizePolicy,QSpacerItem, QFrame, QScrollArea
from UI.Widgets.input import Button
from UI.Widgets.ReviewPopup import ReviewPopup
from UI.Widgets.MessagePopup import MessagePopup

class BookInfo(QWidget):
    def __init__(self,parent):
        super().__init__(parent=parent)  
        self.label_info = {
            "Title" : Book_Label("<h4>Title:</h4> "),
            "Authors" : Book_Label("<h4>Authors:</h4> "),
            "Description" : Book_Label("<h4>Description:</h4>"),
            "Category" : Book_Label("<h4>Category: </h4>"),
            "Publisher" : Book_Label("<h4>Publisher: </h4>"),
            "Price Starting With ($)" : Book_Label("<h4>Price:</h4>"),
            "Publish Date (Month)" : Book_Label("<h4>Publish Month: </h4>"),
            "Publish Date (Year)" : Book_Label("<h4>Publish Year: </h4>"),
            "score" : Book_Label("<h4>Review Score: </h4>"),
            "text" : Book_Label("<h4>Review Text: </h4>", include_seperator=False)
        }

        self.info = {}

        self.book_id = None
        self.popup = None
        self.has_score = None

        #TODO: FIND A BETTER WAY TO NOT HAVE THE ITEMS MOVE DOWN WHEN STRETCHING THE WINDOW
        self.spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)


        self.add_review_button = Button("Add Review")
        self.edit_review_button = Button("Edit Review")

        self.add_review_button.setDisabled(True)
        self.edit_review_button.setDisabled(True)

        self.add_review_button.clicked.connect(self.on_add_button_clicked)
        self.edit_review_button.clicked.connect(self.on_edit_button_clicked)

        self.horizontal_buttons = QHBoxLayout()
        self.horizontal_buttons.addWidget(self.add_review_button)
        self.horizontal_buttons.addWidget(self.edit_review_button)

        self.vertical_layout = QVBoxLayout()

        for _,label in self.label_info.items():
            self.vertical_layout.addLayout(label.vertical_layout) 

        self.vertical_layout.addLayout(self.horizontal_buttons)
        self.vertical_layout.addItem(self.spacer)

        self.vertical_layout.setContentsMargins(10, 10, 10, 10)
        
        # Set the layout to be scrollable
        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget(self)
        self.scroll_widget.setLayout(self.vertical_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        # Set the scroll area as the main layout of the widget
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.scroll_area)

        # Set the fixed width of the widget
        self.setFixedWidth(350)
        self.setLayout(self.main_layout)


    def on_add_button_clicked(self):
        if self.popup is None:
            #Checks if there is already a review
            score_check = "score" in self.info and self.info["score"] is not None
            text_check = "text" in self.info and self.info["text"] is not None
            if (score_check or text_check):
                message = "A review for this book already exists."
                self.popup = MessagePopup(main_window=self, book_id=self.book_id, message=message)
                self.popup.resize(200,100)
                self.popup.exec()
            else:
                self.popup = ReviewPopup(main_window=self, book_id=self.book_id, mode="Add")
                self.popup.resize(800, 600)
                self.popup.exec()
        else:
            self.popup.raise_()

    def on_edit_button_clicked(self):
        if self.book_id is not None:
            print("getting review info for book_id: " + str(self.book_id))

        #TODO: REFACTOR THIS TO NOT USE THE TEXT FROM self.info.
        if self.popup is None:
            score_check = "score" in self.info and self.info["score"] is not None
            text_check = "text" in self.info and self.info["text"] is not None
            if (not score_check and not text_check):
                message = "There is not a review to edit because no reviews for this book exist."
                self.popup = MessagePopup(main_window=self, book_id=self.book_id, message=message)
                self.popup.resize(200,100)
                self.popup.exec()
            else:
                self.popup = ReviewPopup(main_window=self, book_id=self.book_id, mode="Edit")
                self.popup.resize(800, 600)
                self.popup.exec()
        else:
            self.popup.raise_()
            
        
    #TODO: REFACTOR THIS TO MAKE IT MORE READABLE
    def set_book_info(self,book_data):
        for key, value in book_data.items():
            #print(key == "Price Starting With ($)")
            if key == "Price Starting With ($)":
                self.label_info[key].changeData(value,include_dollar_sign=True)
            elif key == "score":
                self.label_info[key].changeData(value, include_out_of_10 = True)
            elif key == "book_id":
                self.book_id = value
                #Enable the add and review buttons only when a book actually exists
                self.add_review_button.setDisabled(False)
                self.edit_review_button.setDisabled(False)
            else:
                self.label_info[key].changeData(value)

            if value == "":
                value = None
            self.info[key] = value

    def reset_book_info(self):
        for key, value in self.label_info.items():
            value.changeData("")
            self.info[key] = None
        self.add_review_button.setDisabled(True)
        self.edit_review_button.setDisabled(True)

class Book_Label(QWidget):
    def __init__(self, text, data=None, include_seperator=True):
        super().__init__()
        self.text = text
        
        #Optional starting info.
        if data is not None:
            self.text += data
    
        self.label = QLabel(text)
        self.label.setWordWrap(True)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.label)

        if include_seperator:
            seperator = QFrame()
            seperator.setFrameShape(QFrame.HLine)  # Horizontal line
            seperator.setFrameShadow(QFrame.Sunken) # Gives a 3D effect (optional)
            self.vertical_layout.addWidget(seperator)

    def changeData(self,new_data,include_dollar_sign=False, include_out_of_10=False):
        text = self.text

        if include_dollar_sign:
            text += "$"

        #if no data can be found to be given to the label, display "None".
        #This has the advantage of keeping the formatting consistent across lines.
        if new_data == "":
            new_data = "None"

        text += str(new_data)

        if (include_out_of_10 & (new_data!="None")):
            text += " / 10"

        #print(text)
        self.label.setText(text)
