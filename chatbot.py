from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load .env file
load_dotenv()

# 2. Get API Key securely
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")  # Replace with your actual key
# 3. Create Flask app
app = Flask(__name__)
CORS(app)

# 4. Configure Gemini API
genai.configure(api_key=API_KEY)
# Chat history for maintaining context
chat_history = [
    {"role": "user", "parts": [{"text": "You are a helpful AI assistant."}]}
]

def chat_with_gemini(prompt):
    try:
        chat_history.append({"role": "user", "parts": [{"text": prompt}]})
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(chat_history)
        ai_response = response.text.strip() if response and response.text else "I didn't get that. Can you clarify?"
        chat_history.append({"role": "model", "parts": [{"text": ai_response}]})
        return ai_response
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
    reply = chat_with_gemini(prompt)
    return jsonify({"response": reply})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    