import tkinter as tk
import subprocess
import os

def run_script(script_name):
    # Asegúrate de que la ruta del script sea correcta
    script_path = os.path.join(os.getcwd(), script_name)
    try:
        # Ejecutar el script en un nuevo proceso
        subprocess.Popen(['python3', script_path])
    except Exception as e:
        print(f"Error al ejecutar {script_name}: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Monitoreo")
root.configure(bg="#34495e")  # Fondo con un tono más oscuro

# Frame para centrar los botones
frame = tk.Frame(root, bg="#34495e")
frame.pack(expand=True, padx=20, pady=20)

# Etiqueta de título
title_label = tk.Label(frame, text="SISTEMA DE MONITOREO", font=("Helvetica", 18, "bold"), fg="#ecf0f1", bg="#34495e")
title_label.pack(pady=(0, 30))

# Botones mejorados para ejecutar diferentes scripts
button1 = tk.Button(frame, text="Compartir Pantalla", command=lambda: run_script("servidor.py"),
                    font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#e74c3c", activebackground="#c0392b")
button1.pack(pady=10, ipadx=20, ipady=10)

button2 = tk.Button(frame, text="Ver Pantalla Externa", command=lambda: run_script("cliente.py"),
                    font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#e74c3c", activebackground="#c0392b")
button2.pack(pady=10, ipadx=20, ipady=10)

button3 = tk.Button(frame, text="Iniciar Sala de Chats", command=lambda: run_script("servidor_mensajes.py"),
                    font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#e74c3c", activebackground="#c0392b")
button3.pack(pady=10, ipadx=20, ipady=10)

button4 = tk.Button(frame, text="Conectar a Sala de Chat", command=lambda: run_script("cliente_mensajes.py"),
                    font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#e74c3c", activebackground="#c0392b")
button4.pack(pady=10, ipadx=20, ipady=10)

button5 = tk.Button(frame, text="Enviar y recibir archivos", command=lambda: run_script("archivos.py"),
                    font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#e74c3c", activebackground="#c0392b")
button5.pack(pady=10, ipadx=20, ipady=10)

# Ajustar el tamaño de la ventana
root.geometry("500x450")
root.resizable(False, False)

# Iniciar el bucle principal de la interfaz
root.mainloop()
