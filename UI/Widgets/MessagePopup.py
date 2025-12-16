from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QApplication, QLabel
from UI.Widgets.input import Button

#Used for the system to display a message to the user(probably errors)
class MessagePopup(QDialog):
    def __init__(self, main_window, book_id, message):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("System Message")

        #Make sure book_id is the right format, then assign it
        try:
            int(book_id)
            self.book_id = book_id
        except ValueError:
            print("Error: book_id is not an int")
            self.close()

        # Create Widgets
        self.Message_Output = QLabel(message)
        self.cancel_button = Button("Cancel",click_on_enter=False) #Cancel button

        # Main vertical layout
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.Message_Output)
        self.vertical_layout.addWidget(self.cancel_button)
    
        # Get current stylesheet from application
        self.setStyleSheet(QApplication.instance().styleSheet())

        # Set the layout for the dialog
        self.setLayout(self.vertical_layout)

        self.cancel_button.clicked.connect(self.close)


    def closeEvent(self, event):
        self.main_window.popup = None
        event.accept()
