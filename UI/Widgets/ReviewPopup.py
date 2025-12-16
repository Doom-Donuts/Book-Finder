from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QFrame, QVBoxLayout, QHBoxLayout, QApplication, QFormLayout, QLabel
from UI.Widgets.input import TextBox, Button, LineInput
from Backend.Signal import event_list
from Backend.Constants import ADD_REVIEW, EDIT_REVIEW, GET_REVIEW
from Backend.async_worker import run_func_async
from Backend.Buisness_Logic import Add_Review, Edit_Review, Fetch_Review

class ReviewPopup(QDialog):
    def __init__(self, main_window, book_id, mode):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Review Editor")
        self.mode = mode #Mode is either "Add" or "Edit"

        #Make sure book_id is the right format, then assign it
        try:
            int(book_id)
            self.book_id = book_id
        except ValueError:
            print("Error: book_id is not an int")
            self.close()

        # Create Widgets
        self.score_label = QLabel("Score: ")
        self.score_suffix_label = QLabel("/ 10")
        self.score_input = LineInput() #Input for the score.
        self.review_text_input = TextBox() #Text box to input the review text
        self.create_review_button = Button("Create Review",click_on_enter=False) #Create review button. 
        self.cancel_button = Button("Cancel",click_on_enter=False) #Cancel button

        #Make the score input field big enough for just two characters to visually suggest how long the input should be
        self.score_input.setMaximumWidth(50)
    
        self.score_input_form = QHBoxLayout()
        self.score_input_form.addStretch()
        self.score_input_form.addWidget(self.score_label)
        self.score_input_form.addWidget(self.score_input)
        self.score_input_form.addWidget(self.score_suffix_label)
        self.score_input_form.addStretch()

        self.score_input_form.setAlignment(Qt.AlignCenter)

        # Bottom buttons layout
        self.bottom_buttons = QHBoxLayout()
        self.bottom_buttons.addWidget(self.create_review_button)
        self.bottom_buttons.addWidget(self.cancel_button)

        # Main vertical layout
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addLayout(self.score_input_form)
        self.vertical_layout.addWidget(self.review_text_input)
        self.vertical_layout.addLayout(self.bottom_buttons)

        # Set border and shadow for text input
        self.review_text_input.setFrameShape(QFrame.Box)
        self.review_text_input.setFrameShadow(QFrame.Sunken)
        self.review_text_input.setLineWidth(1)
    
        # Get current stylesheet from application
        self.setStyleSheet(QApplication.instance().styleSheet())

        # Set the layout for the dialog
        self.setLayout(self.vertical_layout)

        # Connect signals to slots
        self.create_review_button.clicked.connect(self.on_Review_Button_Clicked)
        self.cancel_button.clicked.connect(self.close)
        self.score_input.textChanged.connect(self.clamp_values)

        #Creates an event for adding a review
        event_list.create_event(ADD_REVIEW)
        event_list.subscribe(ADD_REVIEW, result_funcs=[self.Post_Review])
        
        #Creates an event to get past review data
        event_list.create_event(GET_REVIEW)
        event_list.subscribe(GET_REVIEW, result_funcs=[self.Display_Review])

        #Creates an event for editing a review
        event_list.create_event(EDIT_REVIEW)
        event_list.subscribe(EDIT_REVIEW, result_funcs=[self.Post_Review])

        if self.mode == "Edit":
            run_func_async(GET_REVIEW, Fetch_Review, self.book_id)

    #Called to display the review in main window after it is added or edited
    @Slot(object)
    def Post_Review(self, data):
        self.main_window.set_book_info(data)
        print(data)
        self.close()
        
    def on_Review_Button_Clicked(self):
        review_score = self.score_input.text()
        review_text = self.review_text_input.toPlainText()
        if (self.mode == "Add"):
            run_func_async(ADD_REVIEW, Add_Review, self.book_id, review_score, review_text)
        else:
            run_func_async(EDIT_REVIEW, Edit_Review, self.book_id, review_score, review_text)

    def Display_Review(self, data):
        score = data["score"]
        text = data["text"]
        self.score_input.setText(str(score))
        self.review_text_input.setText(text)

    def closeEvent(self, event):
        self.main_window.popup = None
        event.accept()

    def clamp_values(self):
        #Remove whitespace from the end of the input
        self.score_input.setText(self.score_input.text().strip())
        try:
            value = int(self.score_input.text())
            #Clamp values in range 0-10
            if value > 10:
                self.score_input.setText("10")
            elif value < 0:
                self.score_input.setText("0")
        except ValueError:
            #Remove any non text characters
            self.score_input.setText(self.score_input.text()[:-1])