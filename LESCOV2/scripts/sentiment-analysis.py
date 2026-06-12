import os
import pandas as pd
from pysentimiento import create_analyzer
from tqdm import tqdm

# 1. File Configuration
TXT_FILE = "output/out_clean.txt"  # Change this to your file name
OUTPUT_EXCEL = "output/sentiment_results.xlsx"

def analyze_local_comments():
    # Check if the text file exists
    if not os.path.exists(TXT_FILE):
        print(f"Error: The file '{TXT_FILE}' was not found in this folder.")
        return

    print("Loading text file...")
    with open(TXT_FILE, "r", encoding="utf-8") as f:
        # Read line by line, stripping empty whitespaces and lines
        comments = [line.strip() for line in f if line.strip()]

    if not comments:
        print("The file is empty.")
        return

    print(f"Found {len(comments)} comments to analyze.")
    print("Initializing Spanish AI model (PySentimiento)...")
    
    # Creates the analyzer specifically trained for Spanish text
    analyzer = create_analyzer(task="sentiment", lang="es")

    results = []

    print("\nAnalyzing sentiments locally...")
    # tqdm displays a real-time progress bar in your console
    for comment in tqdm(comments):
        try:
            # The model predicts: 'POS' (Positive), 'NEG' (Negative), or 'NEU' (Neutral)
            prediction = analyzer.predict(comment)
            
            # Map labels to clear, human-readable terms
            scale = {"POS": "Positive", "NEG": "Negative", "NEU": "Neutral"}
            final_sentiment = scale.get(prediction.output, "Unknown")
            
            # Extract raw probabilities for finer filtering
            probabilities = prediction.probas
            
            results.append({
                "Comment": comment,
                "Sentiment": final_sentiment,
                "Prob_Positive": round(probabilities.get("POS", 0), 4),
                "Prob_Neutral": round(probabilities.get("NEU", 0), 4),
                "Prob_Negative": round(probabilities.get("NEG", 0), 4)
            })
        except Exception as e:
            # If an error happens on a specific line, skip it and continue
            results.append({
                "Comment": comment,
                "Sentiment": "Analysis Error",
                "Prob_Positive": 0, "Prob_Neutral": 0, "Prob_Negative": 0
            })

    # 3. Save results into an Excel spreadsheet
    print(f"\nSaving results to {OUTPUT_EXCEL}...")
    df = pd.DataFrame(results)
    df.to_excel(OUTPUT_EXCEL, index=False)
    print("Process successfully completed!")

if __name__ == "__main__":
    analyze_local_comments()
