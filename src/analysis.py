from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import numpy as np

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, return_all_scores=True)

def feedback_analysis(review: str):
    scores = classifier(review)[0] 

    probs = np.array([item["score"] for item in scores])
    stars = np.array([1, 2, 3, 4, 5])
    weighted_score = float(np.dot(probs, stars))
    final_score = int(round(weighted_score))
    confidence = float(probs[final_score - 1])

    return final_score, confidence