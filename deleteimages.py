
import requests

DELETE_HASHES_FILE = "deletehashes.txt"
CLIENT_ID = "e998866e6f8c481"
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



delete_all_images()