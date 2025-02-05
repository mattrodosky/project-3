import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QTextEdit

from dotenv import load_dotenv
import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

class StoveWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Stove/Oven")
        self.setGeometry(150, 150, 300, 200)
        
        layout = QVBoxLayout()
        
        self.suggest_button = QPushButton("Suggest Recipes!", self)
        self.suggest_button.clicked.connect(self.suggest_button_clicked)
        layout.addWidget(self.suggest_button)
        
        self.back_button = QPushButton("Back to Main Menu", self)
        self.back_button.clicked.connect(self.close_stove)
        layout.addWidget(self.back_button)
        
        self.recipe_dropdown = QComboBox()
        layout.addWidget(self.recipe_dropdown)

        self.recipe_select = QPushButton("Select Recipe", self)
        self.recipe_select.clicked.connect(self.get_full_recipe)
        layout.addWidget(self.recipe_select)

        self.recipe_label = QTextEdit(self)
        self.recipe_label.setReadOnly(True)
        layout.addWidget(self.recipe_label)

        self.setLayout(layout)
    
    def close_stove(self):
        self.main_window.show()
        self.close()

    def suggest_button_clicked(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        recipe_chooser = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-1.5-flash", temperature=0.3)

        pantry_data = self.main_window.get_pantry_data()  # Fetch latest pantry data
        user_preferences = self.main_window.get_user_preferences()
        
        cuisines = user_preferences['Preferred Cuisines'].unique().tolist()
        diet = user_preferences['Diets'].unique().tolist()

        prompt_base="""
            You are helping me plan out my meals based on what I have. I want to provide you
            a list of ingredients that I know for a fact that I have, and your job is to
            help me determine a main course that I can make using what I have. I want 3 different
            recipes to be provided so I have options.

            When selecting the recipes to make, try to ensure that they are different from
            each other as possible, since if I'm not in the mood for a certain style of food, 
            I still have a decent selection to choose from. I want the answer formatted as:
            1. Recipe #1 Name
            2. Recipe #2 Name
            3. Recipe #3 Name

            These are main ingredients that I have: {ingredients}

        """
        prompt_diet = ""
        if len(diet) > 0:
              prompt_diet = f"I am currently on the following diet(s): {diet}"

        prompt_cuisine = ""
        if len(cuisines) > 0:
              prompt_cuisine = f"Try to ensure that the meals are based on one of these cuisines : {cuisines}"

        prompt = prompt_base + prompt_diet + prompt_cuisine + "Answer:"

        # Convert DataFrames to lists of ingredients
        ingredients = pantry_data['Item Name'].tolist()
        prompt_template = PromptTemplate(
            input_variables=["ingredients"],
            template=prompt
        )
        
        query = {
            "ingredients":ingredients
        }
        chain = LLMChain(llm=recipe_chooser, prompt=prompt_template)
        result = chain.invoke(query)["text"]
        recipe_names = [line.split('. ', 1)[1] for line in result.split("\n") if line.strip().startswith(tuple("123"))]
        self.recipe_dropdown.clear()
        self.recipe_dropdown.addItems(recipe_names)
        
        self.recipe_label.setText(result)

    def get_full_recipe(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        recipe_chooser = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-1.5-flash", temperature=0.3)

        pantry_data = self.main_window.get_pantry_data()  # Fetch latest pantry data
        
        # Convert DataFrames to lists of ingredients
        ingredients = pantry_data['Item Name'].tolist()
        prompt_template = PromptTemplate(
            input_variables=["recipe_name", "ingredients"],
            template="""
                You are helping me plan out my meals based on what I have. I want
                to provide you the name of a recipe and a slist of ingredients that
                I have. I need a recipe that trys to stick to what I have as much
                as possible.

                Assume I have oil, herbs, and spices, but they are not listed.
                
                I need your answer to be in the format of:
                <Recipe Name>
                Ingredients:
                    - Amount Unit Ingredient #1
                    ...
                Directions:
                    1. Step 1 ...
                    ...

                I need a recipe for {recipe_name}.
                I have {ingredients}
                Answer:
            """
        )
        
        query = {
            "recipe_name":self.recipe_dropdown.currentText(),
            "ingredients":ingredients,
        }
        self.chain = LLMChain(llm=recipe_chooser, prompt=prompt_template)
        result = self.chain.invoke(query)["text"]

        print(result)
        self.recipe_label.setText(result)
        
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = StoveWindow(None)
    window.show()
    sys.exit(app.exec())
