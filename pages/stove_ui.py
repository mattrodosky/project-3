import gradio as gr

# Build Gradio UI
def stove_page():
    with gr.Blocks() as page:
        gr.Markdown("# 🔥 Stove & Oven - Recipe Generator")

        gr.Markdown("Click the button below to generate a recipe based on your pantry ingredients.")

        generate_button = gr.Button("Generate Recipe")
        recipe_output = gr.Markdown("Recipe will appear here...")

        # This will later be connected to the LLM function
        generate_button.click(lambda: "🔄 **Generating Recipe...** (LLM Integration Pending)", outputs=recipe_output)

    return page
