import sys
import pandas as pd
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget, QHBoxLayout

class CookbooksWindow(QWidget):
    def __init__(self, main_window, user_preferences):
        super().__init__()
        self.main_window = main_window
        self.user_preferences = user_preferences
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cookbooks")
        self.setGeometry(150, 150, 500, 300)
        
        main_layout = QHBoxLayout()
        input_layout = QVBoxLayout()
        display_layout = QVBoxLayout()
        
        # Input Fields
        self.cuisine_input = QLineEdit()
        self.cuisine_input.setPlaceholderText("Enter preferred cuisine...")
        input_layout.addWidget(QLabel("Preferred Cuisines:"))
        input_layout.addWidget(self.cuisine_input)
        
        self.diet_input = QLineEdit()
        self.diet_input.setPlaceholderText("Enter current diet...")
        input_layout.addWidget(QLabel("Current Diets:"))
        input_layout.addWidget(self.diet_input)
        
        self.submit_button = QPushButton("Add Preferences")
        self.submit_button.clicked.connect(self.add_preference)
        input_layout.addWidget(self.submit_button)
        
        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.clicked.connect(self.close_cookbooks)
        input_layout.addWidget(self.back_button)
        
        # Display Lists
        self.cuisine_list = QListWidget()
        display_layout.addWidget(QLabel("Preferred Cuisines:"))
        display_layout.addWidget(self.cuisine_list)
        
        self.diet_list = QListWidget()
        display_layout.addWidget(QLabel("Current Diets:"))
        display_layout.addWidget(self.diet_list)
        
        main_layout.addLayout(input_layout)
        main_layout.addLayout(display_layout)
        self.setLayout(main_layout)
        
        self.load_existing_preferences()
    
    def add_preference(self):
        cuisine = self.cuisine_input.text().strip()
        diet = self.diet_input.text().strip()
        
        if cuisine:
            self.cuisine_list.addItem(cuisine)
            new_entry = pd.DataFrame([[cuisine, ""]], columns=["Preferred Cuisines", "Diets"])
            self.user_preferences.loc[len(self.user_preferences)] = new_entry.iloc[0]  # Append properly
            self.cuisine_input.clear()
        
        if diet:
            self.diet_list.addItem(diet)
            new_entry = pd.DataFrame([["", diet]], columns=["Preferred Cuisines", "Diets"])
            self.user_preferences.loc[len(self.user_preferences)] = new_entry.iloc[0]  # Append properly
            self.diet_input.clear()
    
    def load_existing_preferences(self):
        for _, row in self.user_preferences.iterrows():
            if row["Preferred Cuisines"]:
                self.cuisine_list.addItem(row["Preferred Cuisines"])
            if row["Diets"]:
                self.diet_list.addItem(row["Diets"])

    def close_cookbooks(self):
        self.main_window.show()
        self.close()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    user_preferences = pd.DataFrame(columns=["Preferred Cuisines", "Diets"])
    window = CookbooksWindow(None, user_preferences)
    window.show()
    sys.exit(app.exec())