import sys
import pandas as pd
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox

class WhiteboardWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.reduced_pantry = []
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Develop a Recipe")
        self.setGeometry(150, 150, 300, 200)
        
        layout = QVBoxLayout()
        
        #Change to search from your ingredients

        self.pantry_dropdown = QComboBox()
        pantry_data = self.main_window.get_pantry_data()
        self.pantry_dropdown.addItems(pantry_data['Item Name'].tolist())
        self.add_priority_button = QPushButton("Add as Priority", self)
        self.add_priority_button.clicked.connect(self.add_priority_button_clicked)
        layout.addWidget(self.add_priority_button)
        
        self.back_button = QPushButton("Back to Main Menu", self)
        self.back_button.clicked.connect(self.close_stove)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def close_stove(self):
        self.main_window.show()
        self.main_window.set_reduced_pantry(self.reduced_pantry)
        self.close()
    
    def add_priority_button_clicked(self):
        self.reduced_pantry.append(self.pantry_dropdown.currentText())
        self.pantry_dropdown.removeItem(self.reduced_pantry.index())

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = WhiteboardWindow(None)
    window.show()
    sys.exit(app.exec())