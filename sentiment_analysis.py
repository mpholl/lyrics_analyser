import numpy as np
# import matplotlib
# matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

verbose = False

# Load the tokenizer and model explicitly
model_name = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)  # Use slow tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Create the pipeline
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None, truncation=True, return_all_scores=True)
# classifier = pipeline("text-classification", model=model_name, top_k=None, truncation=True, return_all_scores=True)


db_path = './data/BATMAN700_db.npy'

playlist_lyrics = np.load(db_path, allow_pickle=True)

languages = np.loadtxt('languages.txt', dtype=str)

print(playlist_lyrics.shape[0])

# Define the fixed order of emotion labels (from GoEmotions dataset)
fixed_labels = [
    "anger",
    "fear",
    "neutral",
    "disgust",
    "surprise",
    "sadness",
    "joy"
]


sentiments = np.zeros((playlist_lyrics.shape[0], len(fixed_labels)))
sentiments[:] = np.nan
for i in range(playlist_lyrics.shape[0]):
    print('='*30)
    print(playlist_lyrics[i,0], '\n')
    try:
        with open(f"lyrics/{playlist_lyrics[i, -2]}.txt", "r") as lyrics_file:
            lyrics = lyrics_file.read()
    except FileNotFoundError:
        print(f"Didn't find lyrics for {playlist_lyrics[i, 0]}")
        continue
    
    if not languages[i] == 'en':
        print(f'Skipping sentiment analysis for {playlist_lyrics[i, 0]}, language is {languages[i]}')
        continue

    lyrics = lyrics.replace('[Chorus]', '')
    lyrics = lyrics.replace('[Pre-Chorus]', '')
    lyrics = lyrics.replace('[Bridge]', '')
    lyrics = lyrics.replace('[Verse 1]', '')
    lyrics = lyrics.replace('[Verse 2]', '')

    if verbose:
        print(f"Text: {lyrics}")

    results = classifier(lyrics, truncation=True)
    # Iterate through results and print sentiment scores
    print("Sentiment Scores:")
    counter = 0
    for sentiment in results[0]:  # Access the first (and only) list for a single text
        print(f"  {sentiment['label']}: {sentiment['score']:.4f}")
        
        # Create a dictionary of scores from the model output
        emotion_scores = {emotion["label"]: emotion["score"] for emotion in results[0]}
        
        # Build a consistent NumPy array with scores in the fixed order
        scores_array = np.array([emotion_scores.get(label, 0.0) for label in fixed_labels], dtype="f4")
        sentiments[i] = scores_array
        counter += 1

np.save('sentiments', sentiments)