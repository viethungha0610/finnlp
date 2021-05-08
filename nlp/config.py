from transformers import AutoTokenizer

BASE_MODEL_PATH = "../input/finbert"
MODEL_PATH = "model.bin"
TOKENIZER = AutoTokenizer.from_pretrained(BASE_MODEL_PATH)
MODEL = AutoModelForSequenceClassification.from_pretrained(BASE_MODEL_PATH)