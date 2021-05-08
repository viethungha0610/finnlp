from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MAX_LEN = 64
BASE_MODEL_PATH = "../input/finbert/"
MODEL_PATH = "model.bin"
TOKENIZER = AutoTokenizer.from_pretrained(BASE_MODEL_PATH)
NLPMODEL = AutoModelForSequenceClassification.from_pretrained(BASE_MODEL_PATH)