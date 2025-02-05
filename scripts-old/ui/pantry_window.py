import sys
import pandas as pd
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QDateEdit, QFormLayout, QLabel

class PantryWindow(QWidget):
    def __init__(self, main_window, pantry_data):
        super().__init__()
        self.main_window = main_window
        self.pantry_data = pantry_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pantry/Fridge")
        self.setGeometry(150, 150, 400, 300)
        
        layout = QFormLayout()
        
        self.item_input = QLineEdit()
        layout.addRow("Item Name:", self.item_input)
        
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["Staple", "Fresh"])
        layout.addRow("Category:", self.category_dropdown)
        
        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        layout.addRow("Expiration Date (Optional):", self.expiry_date)
        
        self.amount_input = QLineEdit()
        layout.addRow("Amount (Optional):", self.amount_input)
        
        self.submit_button = QPushButton("Add Item")
        self.submit_button.clicked.connect(self.add_item)
        layout.addWidget(self.submit_button)
        
        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.clicked.connect(self.close_pantry)
        layout.addWidget(self.back_button)
        
        self.status_label = QLabel()
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def add_item(self):
        item_name = self.item_input.text()
        category = self.category_dropdown.currentText()
        expiry_date = self.expiry_date.date().toString("yyyy-MM-dd") if self.expiry_date.text() else "N/A"
        amount = self.amount_input.text() if self.amount_input.text() else "N/A"
        
        new_entry = pd.DataFrame([[item_name, category, expiry_date, amount]],
                                 columns=["Item Name", "Category", "Expiration Date", "Amount"])
        
        self.pantry_data = pd.concat([self.pantry_data, new_entry], ignore_index=True)
        self.status_label.setText(f"Added: {item_name}")
        self.item_input.clear()
        self.amount_input.clear()

    def close_pantry(self):
        self.main_window.pantry_data = self.pantry_data
        self.main_window.show()
        self.close()

    def get_pantry_data(self):
        return self.pantry_data.copy()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = PantryWindow(None)
    window.show()
    sys.exit(app.exec())
