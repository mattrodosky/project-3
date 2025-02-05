import gradio as gr
import json
import os

# File path for pantry data
PANTRY_FILE = "data/pantry.json"

# Standard Metric & Imperial Units
UNITS = [
    "grams", "kilograms", "milliliters", "liters",  # Metric
    "ounces", "pounds", "cups", "teaspoons", "tablespoons"  # Imperial
]

# Ensure pantry.json exists
def initialize_json():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(PANTRY_FILE):
        with open(PANTRY_FILE, "w") as file:
            json.dump({"ingredients": []}, file, indent=4)

initialize_json()

# Load pantry data
def load_pantry():
    with open(PANTRY_FILE, "r") as file:
        return json.load(file)

# Save pantry data
def save_pantry(data):
    with open(PANTRY_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Add ingredient to pantry and update display
def add_ingredient(name, category, quantity, unit):
    pantry = load_pantry()

    new_item = {
        "name": name,
        "category": category,
        "quantity": f"{quantity} {unit}" if quantity else "N/A"
    }

    pantry["ingredients"].append(new_item)
    save_pantry(pantry)

    return format_pantry_display(pantry["ingredients"])

# Format pantry list for display
def format_pantry_display(ingredients):
    if not ingredients:
        return "No ingredients in pantry."

    return "\n".join([f"{item['name']} ({item['category']}) - Qty: {item['quantity']}" for item in ingredients])

# Build Gradio UI
def pantry_page():
    pantry = load_pantry()

    with gr.Blocks() as page:
        gr.Markdown("## Pantry Management")

        # Ingredient Name
        name_input = gr.Textbox(placeholder="Enter ingredient name", label="Ingredient Name")

        # Category Selection
        category_input = gr.Dropdown(["Staple", "Rotating"], label="Category", interactive=True)

        # Quantity Input
        quantity_input = gr.Textbox(placeholder="Enter quantity", label="Quantity")

        # Measurement Selection
        unit_selection = gr.Dropdown(UNITS, label="Measurement", interactive=True)

        # Pantry Display
        pantry_display = gr.Textbox(value=format_pantry_display(pantry["ingredients"]), interactive=False, label="Current Pantry")

        # Add Button
        add_button = gr.Button("Add Ingredient")

        # Click Event for Adding Ingredients
        add_button.click(add_ingredient, 
                         inputs=[name_input, category_input, quantity_input, unit_selection], 
                         outputs=pantry_display)

    return page
