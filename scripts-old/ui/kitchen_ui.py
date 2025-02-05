from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import sys
import pandas as pd
from pantry_window import PantryWindow
from stove_window import StoveWindow
from cookbooks_window import CookbooksWindow
from whiteboard_window import WhiteboardWindow

class KitchenApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.user_preferences = pd.DataFrame(columns=["Preferred Cuisines", "Diets"])
        self.pantry_data = pd.DataFrame(columns=["Item Name", "Category", "Expiration Date", "Amount", "Unit"])
        self.reduced_pantry = pd.DataFrame(columns=["Item Name", "Category", "Expiration Date", "Amount", "Unit"])

    def initUI(self):
        self.setWindowTitle("AI Kitchen Prototype")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Welcome to Your AI Kitchen", self)
        layout.addWidget(self.label)
        
        self.pantry_button = QPushButton("Pantry/Fridge", self)
        self.pantry_button.clicked.connect(self.open_pantry)
        layout.addWidget(self.pantry_button)
        
        self.stove_button = QPushButton("Stove/Oven", self)
        self.stove_button.clicked.connect(self.open_stove)
        layout.addWidget(self.stove_button)
        
        self.whiteboard_button = QPushButton("Whiteboard", self)
        self.whiteboard_button.clicked.connect(self.open_whiteboard)
        layout.addWidget(self.whiteboard_button)
        
        self.cookbooks_button = QPushButton("Cookbooks", self)
        self.cookbooks_button.clicked.connect(self.open_cookbooks)
        layout.addWidget(self.cookbooks_button)
        
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)
        layout.addWidget(self.quit_button)
        
        self.setLayout(layout)
    
    def open_pantry(self):
        self.pantry_window = PantryWindow(self, self.pantry_data)
        self.pantry_window.show()
        self.hide()
    
    def open_stove(self):
        self.stove_window = StoveWindow(self)
        self.stove_window.show()
        self.hide()
    
    def open_whiteboard(self):
        self.whiteboard_window = WhiteboardWindow(self, self.reduced_pantry)
        self.whiteboard_window.show()
        self.hide()
    
    def open_cookbooks(self):
        self.cookbooks_window = CookbooksWindow(self, self.user_preferences)
        self.cookbooks_window.show()
        self.hide()

    def get_pantry_data(self):
        return self.pantry_data

    def get_user_preferences(self):
        return self.user_preferences
    
    def set_pantry_data(self, pantry_data):
        self.pantry_data = pantry_data
    
    def set_reduced_pantry(self):
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KitchenApp()
    window.show()
    sys.exit(app.exec())
