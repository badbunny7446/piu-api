import requests

res = requests.post("http://localhost:5000/ask", json={"message": "Tell me a joke"})
print(res.json())
