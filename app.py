import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Simple CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return "MI AI Running 🚀"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return "", 200
    
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"reply": "Please type a message."})
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are MI AI. Answer correctly and be helpful."},
                {"role": "user", "content": user_message}
            ]
        )
        
        answer = response.choices[0].message.content
        return jsonify({"reply": answer})
    
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
