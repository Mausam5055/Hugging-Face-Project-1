import gradio as gr
from src.translation import TranslationService
from src.summarization import SummarizationService

# Initialize models globally (load once)
# This can take a moment, so we print a message
print("Initializing AI Services...")
try:
    translator = TranslationService()
    summarizer = SummarizationService()
    print("Services loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")
    # In a real app, you might handle this more gracefully
    translator = None
    summarizer = None

def process_text(input_text):
    """
    Main processing function for the Gradio interface.
    1. Translate to English
    2. Summarize the English text
    """
    if not input_text or not input_text.strip():
        return "Please enter some text.", "No summary available."
    
    if not translator or not summarizer:
        return "Models failed to load. Check logs.", "Error."

    # Step 1: Translate
    print(f"Translating text: {input_text[:50]}...")
    translated_text = translator.translate(input_text)
    
    # Step 2: Summarize
    print(f"Summarizing translation...")
    summary_text = summarizer.summarize(translated_text)
    
    return translated_text, summary_text

# Define Gradio Interface
with gr.Blocks(title="Multilingual Translator & Summariser") as demo:
    gr.Markdown(
        """
        # 🌍 Multilingual Translator & Summariser 📝
        
        **Enter text in ANY language below.** 
        The AI will automatically detect the language, translate it to English, and provide a concise summary.
        """
    )
    
    with gr.Row():
        with gr.Column():
            input_box = gr.Textbox(
                label="Input Text (Any Language)", 
                placeholder="Paste your text here (French, Spanish, German, Hindi, etc.)...",
                lines=8
            )
            submit_btn = gr.Button("🚀 Process", variant="primary")
            
        with gr.Column():
            output_translation = gr.Textbox(
                label="English Translation", 
                lines=6,
                interactive=False
            )
            output_summary = gr.Textbox(
                label="Summary", 
                lines=4, 
                interactive=False
            )

    # Event Listener
    submit_btn.click(
        fn=process_text, 
        inputs=input_box, 
        outputs=[output_translation, output_summary]
    )
    
    gr.Markdown(
        """
        ---
        **Tech Stack:** Hugging Face Transformers | Facebook NLLB-200 | Facebook BART-Large-CNN | Gradio
        """
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
