import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return "MI AI Running"

@app.route("/chat", methods=["POST","OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return "", 200
    msg = request.get_json().get("message","")
    if not msg:
        return jsonify({"reply":"Type something"})
    try:
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"Answer questions helpfully."}, {"role":"user","content":msg}])
        return jsonify({"reply":res.choices[0].message.content})
    except:
        return jsonify({"reply":"Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
