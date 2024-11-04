from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import os

# Create and train the model
sentences = [
    "I love this product",
    "This is an amazing experience",
    "I feel very happy today",
    "This was an excellent day",
    "I am so sad and disappointed",
    "This is terrible, I hate it",
    "I feel bad about this",
    "This is an awful experience",
]

labels = [1, 1, 1, 1, 0, 0, 0, 0]

model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(sentences, labels)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict_sentiment():
    data = request.get_json()
    if not data or 'sentence' not in data:
        return jsonify({"error": "Please provide a sentence to analyze"}), 400

    user_input = data['sentence']
    prediction = model.predict([user_input])
    sentiment = "Positive" if prediction[0] == 1 else "Negative"

    return jsonify({
        "sentiment": sentiment
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  
    app.run(host='0.0.0.0', port=port)
