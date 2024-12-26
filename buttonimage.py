from openai import OpenAI
import wave
import pyaudio
import numpy as np
import pygame
import threading
import requests
import cv2

client = OpenAI()
CLIENT_ID = "e998866e6f8c481"
IMAGE_PATH = "imagem.jpeg"
DELETE_HASHES_FILE = "deletehashes.txt"
with open("template.txt", "r") as arquivo:
    inicio = arquivo.read()


historico = [{"role": "system", "content": inicio}]

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


def take_pic():
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
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Libera a câmera
    cam.release()


def generate_response_with_image(prompt, image_url):
    # Adiciona a mensagem e o link da imagem
    historico.append({
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": image_url},
            },
        ],
    })
    
    # Envia o histórico para a API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Substitua pelo modelo correto
        messages=historico,
        max_tokens=300
    )

    # Resposta gerada pela API
    resposta = completion.choices[0].message.content

    # Adiciona a resposta do assistente ao histórico
    historico.append({"role": "assistant", "content": resposta})
    
    return resposta

def text_to_speech(text):
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="echo",
        input=text
    ) as response:
        response.stream_to_file("resposta.mp3")


# Carregar as variáveis de ambiente do arquivo .env
# Configurar a chave da API da OpenAI

def capture_audio(filename="mensagem.wav"):
    # Configurar o PyAudio para captura de áudio
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    SILENCE_THRESHOLD = 300  # Limite de silêncio (ajuste conforme necessário)
    SILENCE_DURATION = 2  # Segundos de silêncio para parar a gravação
    OUTPUT_FILENAME = filename

    # Iniciar PyAudio
    audio = pyaudio.PyAudio()

    # Abrir fluxo de áudio
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Gravando...")

    frames = []
    silent_chunks = 0

    while True:
        # Ler dados do microfone
        data = stream.read(CHUNK)
        frames.append(data)
        
        # Converter dados em array de numpy
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Verificar o volume do áudio
        if np.abs(audio_data).mean() < SILENCE_THRESHOLD:
            silent_chunks += 1
        else:
            silent_chunks = 0
        
        # Se houve silêncio por um tempo suficiente, parar a gravação
        if silent_chunks > int(SILENCE_DURATION * RATE / CHUNK):
            print("Silêncio detectado, gravação finalizada.")
            break

    # Parar e fechar o fluxo
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Salvar a gravação no arquivo WAV
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    

    return OUTPUT_FILENAME

def transcribe_audio(file_path):
    # Abrir o arquivo de áudio e enviá-lo para a API da OpenAI
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
            )
    return transcription.text


def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    print("Reprodução de áudio concluída!")
    pygame.mixer.quit()

def pensar(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    print("Reprodução de áudio iniciada!")
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Garante que a execução espere até a conclusão do áudio
    pygame.mixer.quit() 


def main():
    while True:
        continuar = input('digite "sair" para encerrar')
        if continuar == "sair":
            delete_all_images()
            break
        play_audio("sim.mp3")
        audio_file = capture_audio()
        print("AUDIO GRAVADO")
        take_pic()
        link = upload_image("foto_capturada.jpg")
        
        transcription = transcribe_audio(audio_file)
        print(f"Mensagem: {transcription}")
        thread = threading.Thread(target=pensar, args=("pensando.mp3",))
        thread.start()        
        
        resposta = generate_response_with_image(transcription, link)
        print(f"Resposta: {resposta}")
        text_to_speech(resposta)
        print("TEXTO PARA AUDIO")
        play_audio('resposta.mp3')
        print("AUDIO REPRODUZIDO")
    

if __name__ == "__main__":
    main()

