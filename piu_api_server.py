from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the token securely from the environment
hf_token = os.getenv("HF_TOKEN")

app = Flask(__name__)

# API details
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
headers = {
    "Authorization": f"Bearer {hf_token}"
}

def query_huggingface(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    try:
        return response.json()[0]["generated_text"]
    except:
        return "Sorry, mujhe samajh nahi aaya. Dobara puchho 😊"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("message")
    if not user_input:
        return jsonify({"error": "Missing 'message' field"}), 400

    ai_reply = query_huggingface(user_input)
    return jsonify({"reply": ai_reply})

@app.route("/")
def home():
    return "Piu AI is Live 😇"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
