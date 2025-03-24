import requests
import os
from dotenv import load_dotenv
import time
load_dotenv()
API_KEY=os.getenv("API_KEY")
def get_sentiment(text):
    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}

    data = {"inputs": text}
    response = requests.post(API_URL, headers=HEADERS, json=data)

    try:
        result = response.json()

        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            best_label = max(result[0], key=lambda x: x["score"])  # Extract highest score
            return best_label["label"]
        else:
            return "Error: Unexpected response format"

    except requests.exceptions.JSONDecodeError:
        return "Error: Empty or invalid JSON response"



def summarize_text(text, max_length=150, min_length=50):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}

    data = {
        "inputs": text,
        "parameters": {"max_length": max_length, "min_length": min_length, "do_sample": False}
    }

    response = requests.post(API_URL, headers=HEADERS, json=data)

    try:
        result = response.json()
        if isinstance(result, list) and "summary_text" in result[0]:
            return result[0]["summary_text"]  # Extract summary text
        else:
            return "Error: Unexpected response format"

    except requests.exceptions.JSONDecodeError:
        return "Error: Empty or invalid JSON response"  

def extract_keywords(text, top_n=5):
    API_URL = "https://api-inference.huggingface.co/models/ml6team/keyphrase-extraction-kbir-inspec"
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}

    data = {"inputs": text}

    response = requests.post(API_URL, headers=HEADERS, json=data)

    try:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            keywords = [item["word"] for item in result[:top_n]]
            return keywords
        else:
            return "Error: Unexpected response format"

    except requests.exceptions.JSONDecodeError:
        return "Error: Empty or invalid JSON response"
    
def text_to_speech(text):
    API_URL = 'https://api-inference.huggingface.co/models/facebook/mms-tts-hin'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    payload = {'inputs': text}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        with open('output.wav', 'wb') as f:
            f.write(response.content)
        print('Audio content written to output.wav')
    else:
        print(f'Error: {response.status_code}, {response.text}')




HEADERS = {"Authorization": f"Bearer {API_KEY}"}
MODELS = {
    "comparison": "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2",
    "sentiment": "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
}

def request_huggingface(api_url, payload, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.post(api_url, headers=HEADERS, json=payload)
            
            if response.status_code == 200:
                return response.json()

            elif response.status_code in [429, 503]:  # Rate limited or service unavailable
                print(f"Rate limited. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    print("Failed to get a valid response after retries.")
    return None

def comparison_impact(text1, text2):
    # Comparison Analysis
    comparison_payload = {"inputs": {"source_sentence": text1, "sentences": [text2]}}
    comparison_result = request_huggingface(MODELS["comparison"], comparison_payload)

    # Sentiment Analysis for Impact
    sentiment1 = request_huggingface(MODELS["sentiment"], {"inputs": text1})
    sentiment2 = request_huggingface(MODELS["sentiment"], {"inputs": text2})

    if sentiment1 and sentiment2:
        sentiment1_label = max(sentiment1[0], key=lambda x: x["score"])["label"]
        sentiment2_label = max(sentiment2[0], key=lambda x: x["score"])["label"]

        impact_analysis = f"Sentiment Shift: '{sentiment1_label}' → '{sentiment2_label}'"
    else:
        impact_analysis = "Error in sentiment analysis."

    return {
        "Comparison Result": comparison_result,
        "Impact Analysis": impact_analysis
    }



