from flask import Flask, jsonify, request
from flask_cors import CORS  
import requests, random,os


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def fetch_quote():
    try:
        res = requests.get("https://zenquotes.io/api/random", timeout=5)
        data = res.json()
        return {"quote": data[0]["q"], "author": data[0]["a"]}
    except:
        fallback = [
            {"quote": "Selv den viseste kan lære mer.", "author": "Ukjent"},
            {"quote": "Stillhet er en kilde til styrke.", "author": "Lao Tzu"},
        ]
        return random.choice(fallback)

@app.route("/quote")
def quote():
    return jsonify(fetch_quote())

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    quote_text = data.get("quote")
    target_lang = data.get("lang", "en")

    if not quote_text:
        return jsonify({"error": "No quote provided"}), 400

    try:
        response = requests.post(
            "https://libretranslate.com/translate",
            json={
                "q": quote_text,
                "source": "en",
                "target": target_lang
            },
            timeout=5
        )
        translated = response.json()["translatedText"]
        return jsonify({"translated": translated})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)