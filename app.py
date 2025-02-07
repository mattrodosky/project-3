import gradio as gr
from pages.pantry_ui import pantry_page
from pages.stove_ui import stove_page
from pages.cookbooks_ui import cookbooks_page
from pages.computer_ui import computer_page

def main():
    with gr.Blocks() as app:
        gr.Markdown("# AI Assisted Recipe Assistant")
        gr.Image("assets/frontpage.png")

        # Persistent Navigation Buttons
        with gr.Row():
            pantry_btn = gr.Button("Pantry")
            stove_btn = gr.Button("Stove/Oven")
            cookbooks_btn = gr.Button("Cookbooks")
            computer_btn = gr.Button("Computer")

        # Hidden Sections (Initially Invisible)
        pantry_section = gr.Column(visible=False)
        stove_section = gr.Column(visible=False)
        cookbooks_section = gr.Column(visible=False)
        computer_section = gr.Column(visible=False)

        # Pantry Page UI
        with pantry_section:
            pantry_page()  

        # Stove Page UI (Placeholder)
        with stove_section:
            stove_page()

        # Cookbooks Page UI 
        with cookbooks_section:
            cookbooks_page()

        # Computer Page UI (Placeholder)
        with computer_section:
            computer_page()

        # Click Events to Show Sections
        pantry_btn.click(lambda: [gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)],
                         outputs=[pantry_section, stove_section, cookbooks_section, computer_section])

        stove_btn.click(lambda: [gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)],
                        outputs=[pantry_section, stove_section, cookbooks_section, computer_section])

        cookbooks_btn.click(lambda: [gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)],
                            outputs=[pantry_section, stove_section, cookbooks_section, computer_section])

        computer_btn.click(lambda: [gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)],
                           outputs=[pantry_section, stove_section, cookbooks_section, computer_section])

    app.launch()

if __name__ == "__main__":
    main()
