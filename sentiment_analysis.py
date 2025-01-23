import numpy as np
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Load the tokenizer and model explicitly
model_name = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)  # Use slow tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Create the pipeline
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None, truncation=True)


db_path = './data/BATMAN_db.npy'

playlist_lyrics = np.load(db_path, allow_pickle=True)

for i in [1]:#range(playlist_lyrics.shape[0]):
    try:
        with open(f"lyrics/{playlist_lyrics[i, -2]}.txt", "r") as lyrics_file:
            lyrics = lyrics_file.read()
    except FileNotFoundError:
        print(f"Didn't find lyrics for {playlist_lyrics[i, 0]}")
        continue

 


# Analyze sentiment
for text in [lyrics]:
    text = text.replace('[Chorus]', '')
    text = text.replace('[Pre-Chorus]', '')
    text = text.replace('[Bridge]', '')
    text = text.replace('[Verse 1]', '')
    text = text.replace('[Verse 2]', '')

    print(f"Text: {text}")

    # results = classifier(text[:len(text)//2], truncation=True)
    results = classifier(text, truncation=True)
    # Iterate through results and print sentiment scores
    print("Sentiment Scores:")
    for sentiment in results[0]:  # Access the first (and only) list for a single text
        print(f"  {sentiment['label']}: {sentiment['score']:.4f}")