import requests

API_KEY = ""
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

data = {
    "contents": [
        {"parts": [{"text": "Hello Gemini, are you working?"}]}
    ]
}

resp = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
print(resp.json())
