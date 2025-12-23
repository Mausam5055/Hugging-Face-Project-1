from transformers import pipeline

class SummarizationService:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        """
        Initializes the summarization pipeline.
        BART-large-cnn is standard for summarization.
        """
        print(f"Loading Summarization Model: {model_name}...")
        # device=0 for GPU, -1 for CPU
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize(self, text, max_length=130, min_length=30):
        """
        Summarizes the input English text.
        """
        if not text:
            return ""
            
        # Error handling for short text
        if len(text.split()) < 20:
            return "Text too short to summarize."

        try:
            # Pipeline returns a list of dictionaries: [{'summary_text': '...'}]
            result = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return result[0]['summary_text']
        except Exception as e:
            return f"Error during summarization: {str(e)}"
