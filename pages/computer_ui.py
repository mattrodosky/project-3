import gradio as gr
import json
import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Pantry file location
PANTRY_FILE = "data/pantry.json"

# Ensure pantry file exists
def initialize_pantry():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(PANTRY_FILE):
        with open(PANTRY_FILE, "w") as file:
            json.dump({"ingredients": []}, file, indent=4)

initialize_pantry()

# Load pantry ingredients
def load_pantry():
    """Load ingredients from pantry.json"""
    with open(PANTRY_FILE, "r") as file:
        pantry_data = json.load(file)
    return [item["name"] for item in pantry_data["ingredients"]]  # Extract ingredient names

# Load the fine-tuned model
MODEL_NAME = "JohnnyCloud/Recipe-names-model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_recipe_name(selected_ingredients):
    """Generate a structured recipe name from selected pantry ingredients."""
    if not selected_ingredients:
        return "Please select at least one ingredient."
    
    if len(selected_ingredients) > 5:
        return "Error: Please select a maximum of 5 ingredients."

    # MATCH THE TRAINING FORMAT
    input_text = f"What can I cook with {', '.join(selected_ingredients)}?"
    print(f"DEBUG: Input Text - {input_text}")  # ✅ Debug input

    # Tokenize input
    inputs = tokenizer(input_text, return_tensors="pt", padding="max_length", truncation=True, max_length=512).to(device)

    # Generate output
    outputs = model.generate(**inputs, max_new_tokens=20, do_sample=True, temperature=0.9, top_k=50, top_p=0.95)

    # Decode output
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    print(f"DEBUG: Raw Model Output - {generated_text}")  # ✅ Debug output

    # Ensure output is a valid recipe name
    if generated_text.lower().startswith("what can i cook with"):
        return "Error: Model repeated the question instead of generating a recipe name."

    return generated_text if len(generated_text.split()) > 1 else "Error: Generated name is too short."




# Recipe Name Generator Page (Formatted to Match Pantry Page)
def computer_page():
    available_ingredients = load_pantry()

    with gr.Blocks() as page:
        gr.Markdown("## Recipe Name Generator")

        ingredient_selector = gr.CheckboxGroup(
            choices=available_ingredients,  
            label="Select up to 5 ingredients"
        )

        generate_button = gr.Button("Generate Recipe Name")
        output_text = gr.Textbox(label="Generated Recipe Name")

        generate_button.click(generate_recipe_name, inputs=ingredient_selector, outputs=output_text)

    return page 