import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

class TranslationService:
    def __init__(self, model_name="facebook/nllb-200-distilled-600M"):
        """
        Initializes the translation model and tokenizer.
        We use the pipeline API for simplicity, or we can load manually for more control.
        Here we use manual loading to strictly enforce source/target languages if needed,
        or just use the pipeline which handles a lot.
        
        For NLLB, specifying source language is often helpful, but for a general 
        "detect and translate" flow, pipeline("translation", ...) with NLLB 
        can be tricky without lang codes.
        
        However, the requirement says "Automatically detects source language". 
        NLLB can do this if we just ask it to translate to English.
        """
        print(f"Loading Translation Model: {model_name}...")
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Using the pipeline for abstraction. 
        # Note: NLLB usually requires src_lang and tgt_lang tokens. 
        # A generic pipeline might need specific handling for NLLB.
        # Let's stick to the specific model loading for finer control if needed, 
        # but 'translation_xx_to_yy' isn't standard in pipeline for NLLB without args.
        # 
        # Actually, NLLB works best when we explicitly tell it the target language is English ('eng_Latn').
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        if self.device == 0:
            self.model = self.model.to("cuda")

    def translate(self, text, target_lang="eng_Latn"):
        """
        Translates input text to English.
        NLLB requires a forced BOS token for the target language.
        """
        if not text:
            return ""

        # NLLB automatically detects language if we don't separate it? 
        # Actually in NLLB-200, it's good to just feed it. 
        
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        if self.device == 0:
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        # forced_bos_token_id is crucial for NLLB to know the target language
        forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(target_lang)
        
        with torch.no_grad():
            translated_tokens = self.model.generate(
                **inputs, 
                forced_bos_token_id=forced_bos_token_id, 
                max_length=512
            )
            
        result = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return result
