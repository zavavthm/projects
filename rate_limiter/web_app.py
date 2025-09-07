import random
from flask import Flask, request, jsonify
import nltk
nltk.download("words")
from nltk.corpus import words
word_list = words.words()

from rate_limiter import FixedWindowRateLimiter

MAX_REQUESTS = 5
WINDOW_SIZE = 10

rl = FixedWindowRateLimiter(MAX_REQUESTS, WINDOW_SIZE)

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask Web App!"

@app.route('/word', methods=['GET'])
def generate_random_word():
    if rl.allow_request():
        random_word = random.sample(word_list, 1)
        return jsonify({"payload": random_word[0]})
    else:
        return jsonify({"payload": "Number of requests exceeding MAX_Requests. Wait till the current window lapses."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)