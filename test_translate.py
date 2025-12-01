import requests

r = requests.post(
    "https://translate.astian.org/translate",
    json={"q": "Hello world", "source": "en", "target": "no"}
)

print(r.status_code, r.text)