import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from plantilla import create_frame_horizontal, crear_label, create_button, create_entry, centrar_frame_principal

def connect_to_server():
    try:
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host_entry.get(), int(port_entry.get())))
        text_area.insert(tk.END, "Conectado al servidor\n")
        # Iniciar un hilo para recibir mensajes del servidor
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar al servidor: {e}")

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            text_area.insert(tk.END, f"Servidor: {message}\n")
            text_area.see(tk.END)
        except Exception as e:
            text_area.insert(tk.END, f"Error al recibir mensaje: {e}\n")
            break

def send_message():
    message = message_entry.get()
    if message:
        client_socket.sendall(message.encode())
        text_area.insert(tk.END, f"Tú: {message}\n")
        text_area.see(tk.END)
        message_entry.delete(0, tk.END)

# Crear la ventana principal
root = tk.Tk()
root.title("Cliente de Chat")
root.configure(bg="#0f1440")

# Titulo
label = tk.Label(root, text="Unirse a una sala", font=("Arial", 18, "bold"), fg="#cdd4ea", bg="#0f1440")
label.pack(pady=(10, 5))

# Frame para ip
frame_chat = create_frame_horizontal(root)
frame_chat.pack(padx=10, pady=10)

# Entradas para la IP y el puerto del servidor
crear_label("IP del Servidor:", frame_chat).grid(row=0, column=0, padx=10, ipadx=20, ipady=10)
host_entry = tk.Entry(frame_chat, width=20, font=("Sans-Serif", 12, "bold"),
        fg="#ffffff",  # Color del texto
        bg="#636cb4",  # Color de fondo del botón
        )
host_entry.insert(0, "127.0.0.1")  # Valor por defecto
host_entry.grid(row=0, column=1, padx=10, ipadx=20, ipady=10)

# Frame para puerto
frame_puerto = create_frame_horizontal(root)
frame_puerto.pack(padx=10, pady=10)

crear_label("Puerto:", frame_puerto).grid(row=0, column=0, padx=10, ipadx=20, ipady=10)
port_entry = create_entry(frame_puerto)
port_entry.insert(0, "12345")  # Valor por defecto
port_entry.grid(row=0, column=1, padx=10, ipadx=20, ipady=10)

# Área de texto para mostrar mensajes
text_area = scrolledtext.ScrolledText(root, width=40, height=10, font=("Sans-Serif", 12, "bold"),
        fg="#0f1440",  # Color del texto
        bg="#cdd4ea",  # Color de fondo del botón,
        )
text_area.pack(padx=10, pady=10)

# Crear un frame para los widgets de entrada de mensajes y botón
message_frame = tk.Frame(root, bg="#0f1440")
message_frame.pack(padx=10, pady=10)

# Entrada para enviar mensajes
message_entry = tk.Entry(message_frame, width=30, font=("Sans-Serif", 12, "bold"),
        fg="#ffffff",  # Color del texto
        bg="#636cb4",  # Color de fondo del botón
        )
message_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Botón para enviar mensajes
send_button = create_button(message_frame, ">", send_message)
send_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Botón para conectarse al servidor
connect_button = create_button(root, "Conectar", connect_to_server)
connect_button.pack(pady=10)

#----------Ajustar el tamaño de la ventana-------------

centrar_frame_principal(root)

# Iniciar el bucle principal de la interfaz
root.mainloop()
