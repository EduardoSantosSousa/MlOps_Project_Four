import requests

# Endpoint da API
API_URL = "https://guns-detection-api-200115564514.us-central1.run.app/predict/"

# Caminho da imagem
IMAGE_PATH = r"D:\MLOPS\MLOPS_PROJECT_FOUR\artifacts\raw\images\17.jpeg"

with open(IMAGE_PATH, "rb") as img_file:
    files = {
        "file": ("17.jpeg", img_file, "image/jpeg")  # Nome simples, tipo correto
    }

    headers = {
        "accept": "image/png"  # espera receber uma imagem como resposta
    }

    response = requests.post(API_URL, files=files, headers=headers)

if response.status_code == 200:
    with open("output.png", "wb") as f:
        f.write(response.content)
    print("✅ Imagem recebida e salva como output.png")
else:
    print("❌ Erro ao chamar a API")
    print(f"Status: {response.status_code}")
    print(response.text)


