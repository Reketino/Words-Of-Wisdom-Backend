from flask import Flask, jsonify, request
from flask_cors import CORS  
import requests
import random
import os


app = Flask(__name__)
CORS(app)

session = requests.Session()




def fetch_quote():
    url = "https://zenquotes.io/api/random"


    try:
        res = session.get(url, timeout=5)
        data = res.json()
        return {"quote": data[0]["q"], "author": data[0]["a"]}
    except Exception: 


        fallback = [
            {"quote": "Selv den viseste kan lære mer.", "author": "Ukjent"},
            {"quote": "Stillhet er en kilde til styrke.", "author": "Lao Tzu"},
        ]
        return random.choice(fallback)

@app.route("/quote")
def quote():
    return jsonify(fetch_quote())




def translate_text(text, target_lang):
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"en|{target_lang}"
        }


        res = session.get(url, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()


        return data["responseData"]["translatedText"]
    

    except Exception:
        return None



@app.route("/translate", methods=["POST"])
def translate():
    data = request.json or {}
    quote_text = data.get("quote")
    target_lang = data.get("lang", "no")

    if not quote_text:
        return jsonify({"error": "No quote provided"}), 400

   
    translated = translate_text(quote_text, target_lang)


    if translated is None: 
       return jsonify({
           "success": False,
           "translated": None,
           "message": "Translation API failed"
       })

    return jsonify({
        "success": True,
        "translated": translated
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)