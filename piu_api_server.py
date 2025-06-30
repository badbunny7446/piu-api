from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)

# Hugging Face token from .env
HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def query_huggingface(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    print("STATUS CODE:", response.status_code)
    print("RESPONSE:", response.text)

    try:
        output = response.json()
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"]
        return "[Unexpected HF Output Format]"
    except Exception as e:
        return f"[Error parsing HF Response] {str(e)}"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    message = data.get("message")
    if not message:
        return jsonify({"error": "Missing message"}), 400
    
    reply = query_huggingface(message)
    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "✅ Piu AI is Live"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
