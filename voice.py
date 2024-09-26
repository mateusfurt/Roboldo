import speech_recognition as sr
import threading
import time
from openai import OpenAI
import wave
import pyaudio
import numpy as np
import pygame
import threading

client = OpenAI()
with open("template.txt", "r") as arquivo:
    inicio = arquivo.read()


historico = [{"role": "system", "content": inicio}]

def generate_response(prompt):
    historico.append({"role": "user", "content": prompt})
    
    # Envia o histórico de mensagens completo
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=historico
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
    SILENCE_THRESHOLD = 100  # Limite de silêncio (ajuste conforme necessário)
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

# Função para capturar o áudio e buscar a palavra de ativação "Roboldo"
def detect_wake_word(wake_word="Roboldo"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Esperando que digam 'Roboldo'...")

    while True:
        with mic as source:
            audio = recognizer.listen(source, phrase_time_limit=3)  # Limite de 3 segundos por trecho

        try:
            # Transcrição usando a API do Google
            transcription = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {transcription}")

            if wake_word.lower() in transcription.lower():
                print(f"'{wake_word}' detectado! Iniciando interação...")
                return True

        except sr.UnknownValueError:
            # Se a transcrição não for compreensível, ignora
            print("Não entendi o áudio.")
            continue
        except sr.RequestError as e:
            #print(f"Erro ao conectar ao serviço de reconhecimento; {e}")
            continue


def capture_audio_and_respond():
    # Função que grava áudio e responde (aqui ficaria sua lógica de gravação/resposta)
    print("Gravando áudio para resposta...")
    # Aqui chamaria a função de gravação de áudio e processamento do Roboldo
    play_audio("sim.mp3")
    audio_file = capture_audio()
    transcription = transcribe_audio(audio_file)
    print(f"Mensagem capturada: {transcription}")
    thread = threading.Thread(target=pensar, args=("pensando.mp3",))
    thread.start()

    resposta = generate_response(transcription)
    print(f"Resposta gerada: {resposta}")
    
    text_to_speech(resposta)
    play_audio("resposta.mp3")
    print("Resposta falada concluída.")


def main():
    while True:
        # Fica ouvindo até que "Roboldo" seja detectado
        if detect_wake_word("robô"):
            capture_audio_and_respond()


if __name__ == "__main__":
    main()
