from PySide6.QtWidgets import QLineEdit, QPushButton, QSizePolicy, QTextEdit

#Two Simple Wrapper classes for QLineEdit and QPushButton. 

class LineInput(QLineEdit):
    def __init__(self, include_clear_button=False):
        super().__init__(clearButtonEnabled=include_clear_button)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,  # horizontal stretch
            QSizePolicy.Policy.Preferred   # vertical size stays preferred
        )


class Button(QPushButton):
    def __init__(self, text, enabled=True, click_on_enter=True):
        super().__init__(text)
        
        #make enter not run the .clicked event
        if not click_on_enter:
            self.setAutoDefault(False)

        self.setEnabled(enabled)

class TextBox(QTextEdit):
    def __init__(self):
        super().__init__()

