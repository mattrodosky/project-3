import gradio as gr
import json
import os

# File path for pantry data
PANTRY_FILE = "data/pantry.json"

# In-memory storage for the base ingredient
base_ingredient = None

# Ensure pantry.json exists
def load_pantry():
    if os.path.exists(PANTRY_FILE):
        with open(PANTRY_FILE, "r") as file:
            return json.load(file).get("ingredients", [])
    return []

# Extract ingredient names for dropdown
def get_pantry_ingredients():
    pantry = load_pantry()
    return [item["name"] for item in pantry] if pantry else ["No ingredients available"]

# Set the base ingredient
def set_base_ingredient(selected_ingredient):
    global base_ingredient
    base_ingredient = selected_ingredient
    return f"**Base Ingredient:** {base_ingredient}"

# Build Gradio UI
def computer_page():
    with gr.Blocks() as page:
        gr.Markdown("# 💻 Computer - Custom Recipe Development")

        gr.Markdown("### **Select a base ingredient from your pantry:**")
        ingredient_dropdown = gr.Dropdown(get_pantry_ingredients(), label="Choose an Ingredient", interactive=True)

        gr.Markdown("### **Selected Base Ingredient:**")
        base_ingredient_display = gr.Markdown("No ingredient selected.")

        set_button = gr.Button("Set Base Ingredient")

        set_button.click(set_base_ingredient, inputs=[ingredient_dropdown], outputs=base_ingredient_display)

    return page
