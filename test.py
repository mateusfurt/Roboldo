import requests
import cv2
from openai import OpenAI

client = OpenAI()
CLIENT_ID = ""
IMAGE_PATH = "imagem.jpeg"
DELETE_HASHES_FILE = "deletehashes.txt"


def save_deletehash_in_text(image_link, deletehash):
    """Salva o deletehash e o link da imagem em um arquivo de texto."""
    try:
        with open(DELETE_HASHES_FILE, "a") as file:
            file.write(f"{image_link} | {deletehash}\n")
        print(f"Deletehash salvo com sucesso para a imagem: {image_link}")
    except Exception as e:
        print(f"Erro ao salvar o deletehash: {e}")


def upload_image(image_path):
    """Faz o upload da imagem e salva o deletehash em um arquivo de texto."""
    url = "https://api.imgur.com/3/upload"
    headers = {"Authorization": f"Client-ID {CLIENT_ID}"}
    with open(image_path, "rb") as image_file:
        payload = {"image": image_file.read()}
        response = requests.post(url, headers=headers, files=payload)

    if response.status_code == 200:
        data = response.json()["data"]
        print("Upload bem-sucedido!")
        print("Link da Imagem:", data["link"])
        save_deletehash_in_text(data["link"], data["deletehash"])
        return data["link"]
    else:
        print("Erro no upload:", response.status_code, response.text)


def delete_all_images():
    """Lê o arquivo de texto, deleta todas as imagens listadas e limpa o arquivo."""
    try:
        with open(DELETE_HASHES_FILE, "r") as file:
            lines = file.readlines()

        if not lines:
            print("Nenhuma imagem para deletar.")
            return

        for line in lines:
            try:
                image_link, deletehash = line.strip().split(" | ")
                url = f"https://api.imgur.com/3/image/{deletehash}"
                headers = {"Authorization": f"Client-ID {CLIENT_ID}"}
                response = requests.delete(url, headers=headers)

                if response.status_code == 200:
                    print(f"Imagem deletada com sucesso: {image_link}")
                else:
                    print(f"Erro ao deletar imagem {image_link}: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Erro ao processar a linha: {line.strip()} - {e}")

        # Limpa o arquivo após deletar todas as imagens
        open(DELETE_HASHES_FILE, "w").close()
        print("Todas as imagens foram deletadas e a lista foi limpa.")

    except FileNotFoundError:
        print("Arquivo de deletehashes.txt não encontrado.")




# Inicializa a captura da webcam
cam = cv2.VideoCapture(0)

# Captura uma imagem
res, imagem = cam.read()

# Verifica se a captura foi bem-sucedida
if res:
    # Exibe a imagem capturada
    cv2.imshow("Foto", imagem)
    
    # Salva a imagem em um arquivo no disco
    cv2.imwrite("foto_capturada.jpg", imagem)
    print("Imagem salva como 'foto_capturada.jpg'")
    
    # Aguarda uma tecla para fechar a janela
    cv2.waitKey(1)
    cv2.destroyAllWindows()

# Libera a câmera
cam.release()

# Exemplo de uso
link = upload_image("foto_capturada.jpg")  # Faz o upload e salva o deletehash
#delete_all_images()       # Deleta todas as imagens e limpa a lista


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "descreva a imagem"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": link,
                    },
                },
            ],
        }
    ],
)

print(response.choices[0])

delete_all_images()