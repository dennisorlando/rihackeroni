import whisper
import sounddevice as sd
import numpy as np
import time
import threading
import keyboard  # Modulo per rilevare la pressione dei tasti

# Carica il modello Whisper
model = whisper.load_model("base")

# Parametri di configurazione
SAMPLERATE = 16000
CHANNELS = 1
BLOCK_SIZE = 1024
BUFFER_SIZE = SAMPLERATE * 2

# Variabile per gestire l'interruzione
stop_recording = False


# Funzione per acquisire e trascrivere audio in tempo reale
def record_and_transcribe():
    print("Inizia a parlare... Premi 'q' per fermare.")
    audio_buffer = np.zeros((BUFFER_SIZE,))

    while not stop_recording:
        audio_chunk = sd.rec(BLOCK_SIZE, samplerate=SAMPLERATE, channels=CHANNELS, dtype='int16')
        sd.wait()

        audio_buffer[:BLOCK_SIZE] = audio_chunk.flatten()

        try:
            result = model.transcribe(audio_buffer)
            print("Trascrizione:", result["text"])
        except Exception as e:
            print("Errore durante la trascrizione:", e)

        time.sleep(0.5)


# Thread per eseguire la registrazione e trascrizione in background
thread = threading.Thread(target=record_and_transcribe)
thread.daemon = True
thread.start()

# Controlla continuamente se premi il tasto 'q' per fermare l'ascolto
while True:
    if keyboard.is_pressed('q'):  # Premi 'q' per fermare l'ascolto
        stop_recording = True
        print("Ascolto interrotto.")
        break
    time.sleep(0.1)
