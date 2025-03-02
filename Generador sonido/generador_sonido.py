import os
import shutil  # Importar shutil para copiar archivos
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk  # Importar ttk
from gtts import gTTS

def generar_audio():
    texto = entry_texto.get().strip()
    nombre_archivo = entry_nombre.get().strip().replace(" ", "_")

    if not texto or not nombre_archivo:
        messagebox.showerror("Error", "Por favor, completa ambos campos.")
        return

    # Validar que no se repita el nombre del archivo
    for item in lista_sonidos.get_children():
        if lista_sonidos.item(item, "values")[0] == nombre_archivo:
            messagebox.showerror("Error", "El nombre del archivo ya existe. Por favor, elige otro nombre.")
            return

    texto_final = f"Emergencia código azul en {texto}. Emergencia."

    try:
        archivo_generado = nombre_archivo  # Guardar sin extensión
        tts = gTTS(text=texto_final, lang='es-us')
        tts.save(f"{archivo_generado}.mp3")

        lista_sonidos.insert("", "end", values=(nombre_archivo, texto_final))
        messagebox.showinfo("Éxito", f"Archivo '{archivo_generado}' guardado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

def reproducir_audio(nombre_archivo):
    if nombre_archivo and os.path.exists(f"{nombre_archivo}.mp3"):  # Cambiar && por and
        if os.name == "nt":  # Windows
            os.system(f"start {nombre_archivo}.mp3")
        else:  # Linux / MacOS
            os.system(f"mpg321 {nombre_archivo}.mp3")  # Requiere mpg321
    else:
        messagebox.showerror("Error", "El archivo de audio no existe.")

def guardar_todos():
    directorio = filedialog.askdirectory()
    if not directorio:
        return

    for item in lista_sonidos.get_children():
        nombre_archivo = lista_sonidos.item(item, "values")[0]
        if os.path.exists(f"{nombre_archivo}.mp3"):
            try:
                shutil.copy(f"{nombre_archivo}.mp3", os.path.join(directorio, f"{nombre_archivo}"))
            except PermissionError as e:
                messagebox.showerror("Error", f"No se pudo copiar el archivo '{nombre_archivo}.mp3': {e}")

    messagebox.showinfo("Éxito", "Todos los archivos han sido guardados.")

def on_item_selected(event):
    selected_item = lista_sonidos.selection()
    if selected_item:
        nombre_archivo = lista_sonidos.item(selected_item, "values")[0]
        reproducir_audio(nombre_archivo)

# Crear ventana principal
root = tk.Tk()
root.title("Texto a Voz")
root.geometry("600x400")

# Etiquetas y campos de entrada
tk.Label(root, text="Ingrese Ubicacion:").pack(pady=5)
entry_texto = tk.Entry(root, width=40)
entry_texto.pack(pady=5)

tk.Label(root, text="Codigo del Boton de llamado:").pack(pady=5)
entry_nombre = tk.Entry(root, width=40)
entry_nombre.pack(pady=5)

# Botones
btn_generar = tk.Button(root, text="Generar Audio", command=generar_audio)
btn_generar.pack(pady=10)

btn_guardar_todos = tk.Button(root, text="Guardar Todos", command=guardar_todos)
btn_guardar_todos.pack(pady=5)

# Tabla para listar sonidos generados
cols = ("Codigo del Boton de llamado", "Texto")
lista_sonidos = ttk.Treeview(root, columns=cols, show="headings")  # Usar ttk.Treeview
for col in cols:
    lista_sonidos.heading(col, text=col)
lista_sonidos.pack(pady=10, fill=tk.BOTH, expand=True)

# Vincular evento de selección
lista_sonidos.bind("<<TreeviewSelect>>", on_item_selected)

# Ejecutar la interfaz
root.mainloop()

