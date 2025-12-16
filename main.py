from __future__ import annotations
import sys

from path_fix import resource_path

from PySide6.QtWidgets import (
    QApplication, QMainWindow
)

from UI.Widgets.tabs import Tab_Widget

# This class is responsible for handling the window itself, including the title bar, keyboard shortcuts, and theme.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Get a reference to the application itself.
        self.app = QApplication.instance()

        #Create a widget that contains the tabbing system.
        self.tabs = Tab_Widget(parent=self)

        #Get the stylesheets and put them into self.dark_stylesheet and self.light_stylesheet
        self.getStyleSheets()

        #Default to being in dark mode
        self.setCurrentMode(dark_mode=True)

        # Set window title, menu, etc.
        self.setWindowTitle("BookFinder")
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        dark_mode_button = self.file_menu.addAction("Toggle Dark Mode",lambda: self.setCurrentMode(dark_mode=not self.dark_mode))
        dark_mode_button.setShortcut("Ctrl+Shift+D")

        #Add an option to the file tab on the top bar for exiting the program. 
        exit_action = self.file_menu.addAction("Exit", self.close)
        #Map this exit button to the keyboard shortcut
        exit_action.setShortcut("Ctrl+Q")
        
        self.setCentralWidget(self.tabs)

    def setCurrentMode(self,dark_mode):
        if dark_mode:
            self.app.setStyleSheet(self.dark_stylesheet)
            self.dark_mode = True
        else:
            self.app.setStyleSheet(self.light_stylesheet)
            self.dark_mode = False
    
    def getStyleSheets(self):
        with open(resource_path("UI/Themes/light_red.qss")) as f:
            self.light_stylesheet = f.read()

        with open(resource_path("UI/Themes/dark_red.qss")) as f:
            self.dark_stylesheet = f.read()    

        with open(resource_path("UI/Themes/fixes.qss")) as f:
            fixes_stylesheet = f.read()

        self.light_stylesheet += fixes_stylesheet
        self.dark_stylesheet += fixes_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #Create the main window for the application
    window = MainWindow()
    window.resize(1000, 750)
    window.show()
    sys.exit(app.exec())
    