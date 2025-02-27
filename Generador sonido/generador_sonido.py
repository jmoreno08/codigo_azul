import os
import tkinter as tk
from tkinter import messagebox
from gtts import gTTS

def generar_audio():
    texto = entry_texto.get().strip()
    nombre_archivo = entry_nombre.get().strip().replace(" ", "_")

    if not texto or not nombre_archivo:
        messagebox.showerror("Error", "Por favor, completa ambos campos.")
        return

    texto_final = f"Emergencia código azul en {texto}. Emergencia."

    try:
        global archivo_generado
        archivo_generado = f"{nombre_archivo}.mp3"
        tts = gTTS(text=texto_final, lang='es-us')
        tts.save(archivo_generado)

        messagebox.showinfo("Éxito", f"Archivo '{archivo_generado}' guardado correctamente.")
        btn_reproducir.config(state=tk.NORMAL)  # Activar el botón de reproducción
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

def reproducir_audio():
    if archivo_generado and os.path.exists(archivo_generado):
        if os.name == "nt":  # Windows
            os.system(f"start {archivo_generado}")
        else:  # Linux / MacOS
            os.system(f"mpg321 {archivo_generado}")  # Requiere mpg321
    else:
        messagebox.showerror("Error", "El archivo de audio no existe.")

# Crear ventana principal
root = tk.Tk()
root.title("Texto a Voz")
root.geometry("400x250")

archivo_generado = None  # Variable global para almacenar el nombre del archivo generado

# Etiquetas y campos de entrada
tk.Label(root, text="Texto a convertir:").pack(pady=5)
entry_texto = tk.Entry(root, width=40)
entry_texto.pack(pady=5)

tk.Label(root, text="Nombre del archivo:").pack(pady=5)
entry_nombre = tk.Entry(root, width=40)
entry_nombre.pack(pady=5)

# Botones
btn_generar = tk.Button(root, text="Generar Audio", command=generar_audio)
btn_generar.pack(pady=10)

btn_reproducir = tk.Button(root, text="Reproducir Audio", command=reproducir_audio, state=tk.DISABLED)
btn_reproducir.pack(pady=5)

# Ejecutar la interfaz
root.mainloop()

