import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET","POST","OPTIONS"], "allow_headers": "*"}})

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return "MI AI Running"

@app.route("/chat", methods=["POST","OPTIONS"])
def chat():
    msg = request.get_json().get("message","") if request.get_json() else ""
    if not msg:
        return jsonify({"reply":"Type something"})
    try:
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"Answer helpfully"}, {"role":"user","content":msg}])
        return jsonify({"reply":res.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply":"Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
