import requests

r = requests.post(
    "https://reketino-s-word-of-wisdom.onrender.com/",
    json={"quote": "Hello world", "lang": "no"},
)

print(r.status_code, r.json())