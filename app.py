import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*", "methods": ["POST", "GET"], "allow_headers": ["Content-Type"]}, r"/": {"origins": "*"}})

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return "MI AI Running 🚀"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"reply": "Please type a message."})
        response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": "You are MI AI. Creator: M.I. Muhammadh. Age: 17 years old. Answer correctly, don't invent facts, be helpful and friendly. Detect user language and reply in same language/script."}, {"role": "user", "content": user_message}])
        answer = response.choices[0].message.content
        return jsonify({"reply": answer})
    except Exception as e:
        return jsonify({"reply": "MI AI Error: " + str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
