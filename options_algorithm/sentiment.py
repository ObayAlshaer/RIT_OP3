from transformers import BertTokenizer, BertForSequenceClassification
from torch import softmax
import torch

tokenizer = BertTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = BertForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

def get_sentiment(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    
    with torch.no_grad():
        logits = model(**inputs).logits
        
    probs = softmax(logits, dim=1)
    
    sentiment = torch.argmax(probs, dim=1).item()
    
    if sentiment == 0:
        return "negative"
    elif sentiment == 1:
        return "neutral"
    else:
        return "positive"

