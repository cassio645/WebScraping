import requests

response = requests.get("https://www.walissonsilva.com")
print(f"Código de Status: {response.status_code}")
print(f"Cabeçalho: {response.headers}")
print(f"=-"*30)
print(f"Conteudo: {response.content}")

