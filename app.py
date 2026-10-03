from flask import Flask, render_template, request, jsonify
from transformers import pipeline
from textblob import TextBlob
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import requests
import os
import sys
print("🟢 Using Python from:", sys.executable)

try:
    from deepface import DeepFace
    print("✅ DeepFace is available.")
except ImportError:
    print("❌ DeepFace NOT found in this environment.")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
sentiment_pipeline = pipeline("sentiment-analysis")

def get_sentiment(text):
    if not text.strip():
        return {"sentiment": "Neutral", "score": 0.0, "emoji": "😐"}

    result = sentiment_pipeline(text)[0]
    score = round(result['score'], 2)
    sentiment = result['label']
    emoji = "😃" if sentiment == "POSITIVE" else "😢" if sentiment == "NEGATIVE" else "😐"
    return {"sentiment": sentiment, "score": score, "emoji": emoji}

def extract_text_from_url(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup.get_text()
    except:
        return ""

@app.route('/')
def home():
    return render_template('sentiment.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('text', '')

    if 'file' in request.files and request.files['file'].filename:
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text += " " + f.read()

    if request.form.get('url'):
        url_text = extract_text_from_url(request.form['url'])
        text += " " + url_text

    if request.form.get('emoji'):
        text += " " + request.form.get('emoji')

    if request.form.get('stars'):
        stars = int(request.form.get('stars'))
        if stars >= 4:
            text += " I'm very satisfied"
        elif stars == 3:
            text += " I'm okay with this"
        else:
            text += " I'm disappointed"

    result = get_sentiment(text)

    return render_template('sentiment.html', result=result)

@app.route('/detect_mood', methods=['POST'])
def detect_mood():
    # DeepFace is not available, return mock response
    return jsonify({
        "mood": "Neutral",
        "emoji": "😐",
        "feedback": "Mood detection module is not enabled. (DeepFace not installed)"
    })

if __name__ == '__main__':
    app.run(debug=True)
