import os
from flask import Flask, request, jsonify, Response
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/", methods=["GET","POST","OPTIONS"])
def home():
    resp = Response("MI AI Running")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp

@app.route("/chat", methods=["POST","OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        resp = Response()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return resp
    
    msg = request.get_json().get("message","")
    if not msg:
        return jsonify({"reply":"Type something"})
    try:
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"Answer helpfully"}, {"role":"user","content":msg}])
        return jsonify({"reply":res.choices[0].message.content})
    except:
        return jsonify({"reply":"Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
