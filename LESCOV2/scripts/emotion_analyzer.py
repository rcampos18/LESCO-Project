import os
import pandas as pd
from pysentimiento import create_analyzer
from tqdm import tqdm

# 1. File Configuration
TXT_FILE = "output/out.txt"  # Your source text file
OUTPUT_EXCEL = "output/emotion_analysis_results.xlsx"  # The new separate output file

def analyze_local_emotions():
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
    print("Initializing Spanish Emotion AI model (PySentimiento)...")
    
    # Creates the analyzer specifically trained for EMOTIONS in Spanish text
    analyzer = create_analyzer(task="emotion", lang="es")

    results = []

    print("\nAnalyzing emotions locally...")
    # tqdm displays a real-time progress bar in your console
    for comment in tqdm(comments):
        try:
            # The model predicts the dominant emotion
            prediction = analyzer.predict(comment)
            
            # Map the model's English labels to clear names
            emotion_map = {
                "joy": "Joy / Happiness",
                "sadness": "Sadness",
                "anger": "Anger / Frustration",
                "fear": "Fear",
                "disgust": "Disgust",
                "surprise": "Surprise",
                "others": "Neutral / No Emotion"
            }
            dominant_emotion = emotion_map.get(prediction.output, "Unknown")
            
            # Extract raw probabilities for each emotion matrix
            probabilities = prediction.probas
            
            results.append({
                "Comment": comment,
                "Dominant_Emotion": dominant_emotion,
                "Prob_Joy": round(probabilities.get("joy", 0), 4),
                "Prob_Sadness": round(probabilities.get("sadness", 0), 4),
                "Prob_Anger": round(probabilities.get("anger", 0), 4),
                "Prob_Fear": round(probabilities.get("fear", 0), 4),
                "Prob_Disgust": round(probabilities.get("disgust", 0), 4),
                "Prob_Surprise": round(probabilities.get("surprise", 0), 4),
                "Prob_Neutral": round(probabilities.get("others", 0), 4)
            })
        except Exception as e:
            # If an error happens on a specific line, skip it and continue
            results.append({
                "Comment": comment,
                "Dominant_Emotion": "Analysis Error",
                "Prob_Joy": 0, "Prob_Sadness": 0, "Prob_Anger": 0,
                "Prob_Fear": 0, "Prob_Disgust": 0, "Prob_Surprise": 0, "Prob_Neutral": 0
            })

    # 3. Save results into a brand new Excel spreadsheet
    print(f"\nSaving emotional data to {OUTPUT_EXCEL}...")
    df = pd.DataFrame(results)
    df.to_excel(OUTPUT_EXCEL, index=False)
    print("Process successfully completed! Your emotion document is ready.")

if __name__ == "__main__":
    analyze_local_emotions()
