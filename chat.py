from openai import OpenAI
from pathlib import Path
import wave
import pyaudio
import numpy as np
import time
import pygame

client = OpenAI()

def generate_response(prompt):
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "você é o roboldo"},
        {
            "role": "user",
            "content": prompt
        }
        ]
    )

    return completion.choices[0].message.content


def text_to_speech(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=text
        )
    response.stream_to_file("speech.mp3")



# Carregar as variáveis de ambiente do arquivo .env
# Configurar a chave da API da OpenAI

def capture_audio(filename="mensagem.wav"):
    # Configurar o PyAudio para captura de áudio
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    SILENCE_THRESHOLD = 700  # Limite de silêncio (ajuste conforme necessário)
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

def main():
    
    
    audio_file = capture_audio()
    transcription = transcribe_audio(audio_file)
    print(f"Mensagem: {transcription}")
    
    
    resposta = generate_response(transcription)
    print(f"Resposta: {resposta}")
    text_to_speech(resposta)
    play_audio('speech.mp3')

if __name__ == "__main__":
    main()

