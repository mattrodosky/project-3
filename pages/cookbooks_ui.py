import gradio as gr
import json
import os

# File path for preferences
PREFERENCES_FILE = "data/preferences.json"

# Preloaded options
CUISINE_OPTIONS = [
    "Italian", "French", "Mexican", "Japanese", "Chinese", "Indian", 
    "Thai", "Greek", "Spanish", "Korean", "Vietnamese", "Middle Eastern"
]
DIET_OPTIONS = [
    "Vegetarian", "Vegan", "Paleo", "Keto", "Gluten-Free", "Dairy-Free",
    "Pescatarian", "Low-Carb", "Mediterranean", "Whole30"
]

# Ensure preferences.json exists
def load_preferences():
    if not os.path.exists(PREFERENCES_FILE):
        default_data = {"cuisines": [], "diets": []}
        with open(PREFERENCES_FILE, "w") as file:
            json.dump(default_data, file, indent=4)
    with open(PREFERENCES_FILE, "r") as file:
        return json.load(file)

# Save preferences
def save_preferences(preferences):
    with open(PREFERENCES_FILE, "w") as file:
        json.dump(preferences, file, indent=4)

# Update preferences when checkboxes change
def update_preferences(selected_cuisines, selected_diets):
    preferences = {"cuisines": selected_cuisines, "diets": selected_diets}
    save_preferences(preferences)
    return format_preferences(preferences)

# Clear all preferences
def clear_preferences():
    save_preferences({"cuisines": [], "diets": []})
    return format_preferences({"cuisines": [], "diets": []})

# Format preferences display
def format_preferences(preferences):
    cuisine_list = ", ".join(preferences["cuisines"]) if preferences["cuisines"] else "None"
    diet_list = ", ".join(preferences["diets"]) if preferences["diets"] else "None"
    return f"**Preferred Cuisines:** {cuisine_list}\n\n**Dietary Preferences:** {diet_list}"

# Build Gradio UI
def cookbooks_page():
    preferences = load_preferences()

    with gr.Blocks() as page:
        gr.Markdown("# 📖 Cookbooks - Set Preferences")

        with gr.Row():
            cuisine_checkboxes = gr.CheckboxGroup(CUISINE_OPTIONS, label="Select Preferred Cuisines", value=preferences["cuisines"])
            diet_checkboxes = gr.CheckboxGroup(DIET_OPTIONS, label="Select Dietary Preferences", value=preferences["diets"])

        display_area = gr.Markdown(format_preferences(preferences))

        save_button = gr.Button("Save Preferences")
        clear_button = gr.Button("Clear All Preferences")

        save_button.click(update_preferences, inputs=[cuisine_checkboxes, diet_checkboxes], outputs=display_area)
        clear_button.click(clear_preferences, outputs=display_area)

    return page
