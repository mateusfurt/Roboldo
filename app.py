from openai import OpenAI
import wave
import pyaudio
import numpy as np
import pygame
import threading
import time
import serial
import socket
import random




UDP_IP = "0.0.0.0"
UDP_PORT = 5005  # qualquer porta livre, escolha uma

# Criar socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Aguardando mensagens UDP na porta {UDP_PORT}...")

client = OpenAI()
with open("app.txt", "r") as arquivo:
    inicio = arquivo.read()
    
    
historico = [{"role": "system", "content": inicio}]

arduino = serial.Serial('COM3', 9600, timeout=1)  # Altere 'COM3' conforme necessário
time.sleep(2)

def enviar_comando(comando):
    arduino.write(comando.encode())
    time.sleep(0.1)

def generate_response(prompt, max_retries=5):
    historico.append({"role": "user", "content": prompt})

    retries = 0
    while retries < max_retries:
        try:
            # Envia o histórico de mensagens completo
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=historico
            )
            
            # Resposta gerada pela API
            resposta = completion.choices[0].message.content

            # Adiciona a resposta ao histórico
            historico.append({"role": "assistant", "content": resposta})

            return resposta

        except Exception as e:
            erro = str(e)
            if "overloaded" in erro or "server_error" in erro:
                espera = 2 ** retries + random.uniform(0, 1)  # backoff exponencial com jitter
                print(f"[Aviso] Modelo sobrecarregado. Tentando novamente em {espera:.1f}s...")
                time.sleep(espera)
                retries += 1
            else:
                # Se for outro erro, não insiste
                raise e

    raise RuntimeError("Falha ao gerar resposta após várias tentativas (engine sobrecarregada).")


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
    SILENCE_THRESHOLD = 500  # Limite de silêncio (ajuste conforme necessário)
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
    pontuação = 0
    pergunta_atual = 1

    resposta = generate_response("Olá, Roboldo! se apresente")
    emocao = resposta[0]
    print(f"Resposta: {resposta}")
    text_to_speech(resposta[1:])
    print("TEXTO PARA AUDIO")
    enviar_comando("G")
    play_audio('resposta.mp3')
    enviar_comando(emocao)
    print("AUDIO REPRODUZIDO")
    while True:
        data, addr = sock.recvfrom(2048)  # buffer de 2048 bytes
        decoded_data = data.decode('utf-8')


        print(f"Recebido de {addr}: {decoded_data}")
        parts = decoded_data.split('|')
        
        if len(parts) == 3:
            pergunta = parts[0]
            resposta_correta = parts[1]
            resposta_usuario = parts[2]

            print("--- Dados recebidos ---")
            print(f"  Origem: {addr}")
            print(f"  Pergunta: {pergunta}")
            print(f"  Resposta Correta: {resposta_correta}")
            print(f"  Resposta do Usuário: {resposta_usuario}")
            print("-----------------------")
            print(f"debug {resposta_usuario} == {resposta_correta}")

            if resposta_usuario.strip().lower() == resposta_correta.strip().lower():
                print(f"debug {resposta_usuario} == {resposta_correta}")
                pontuação += 1
            mensagem = (
                f"--- Dados recebidos ---\n"
                f"  Origem: {addr}\n"
                f"  Pergunta: {pergunta}\n"
                f"  Resposta Correta: {resposta_correta}\n"
                f"  Resposta do Usuário: {resposta_usuario}\n"
                f"  Pergunta {pergunta_atual} de 10\n"
                f"-----------------------"
            )
        print(f"Mensagem formatada:\n{mensagem}")
        resposta = generate_response(mensagem)
        emocao = resposta[0]
        print(f"Resposta: {resposta}")
        text_to_speech(resposta[1:])
        print("TEXTO PARA AUDIO")
        enviar_comando("G")
        play_audio('resposta.mp3')
        enviar_comando(emocao)
        print("AUDIO REPRODUZIDO")
        if pergunta_atual == 10:
            mensagem = (
                f"--- Dados recebidos ---\n"
                f"  Pontuação final: {pontuação}/10\n"
                f"-----------------------"
            )
            resposta = generate_response(mensagem)
            emocao = resposta[0]
            print(f"Resposta: {resposta}")
            text_to_speech(resposta[1:])
            print("TEXTO PARA AUDIO")
            enviar_comando("G")
            play_audio('resposta.mp3')
            enviar_comando(emocao)
            print("AUDIO REPRODUZIDO")
            exit()
        pergunta_atual += 1
    

if __name__ == "__main__":
    main()

