from gtts import gTTS
import os

# Entrada de texto para convertir a voz
texto = input("Introduce el texto a convertir a voz: ")

# Nombre del archivo de salida
namefile = input("Introduce el nombre del archivo sin la extensión: ")

# Genera el archivo de audio usando gTTS
tts = gTTS(text=texto, lang='es')

# Guarda el archivo con el nombre proporcionado
tts.save(f"{namefile}")

print("Archivo guardado con éxito")

