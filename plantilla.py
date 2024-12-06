import tkinter as tk
import socket

def create_button(frame, texto, comando):
    button = tk.Button(
        frame,
        text=texto,
        command=comando,
        font=("Sans-Serif", 12, "bold"),
        fg="#ffffff",  # Color del texto
        bg="#282e61",  # Color de fondo del botón
        activebackground="#636cb4",  # Color de fondo cuando el botón está activo
        highlightthickness=0,  # Grosor del contorno
        highlightbackground="#282e61",  # Color del contorno (mismo que el fondo del botón)
        highlightcolor="#282e61"  # Color del contorno al enfocar el botón
    )
    return button

def create_frame_horizontal(frame1):
    frame = tk.Frame(frame1, bg="#0f1440")
    return frame

def crear_label(texto, frame):
    label = tk.Label(frame, text=texto, font=("Arial", 16), fg="#cdd4ea", bg="#0f1440")
    return label

def create_entry(frame, mostrar):
    entry = tk.Entry(frame, width=20, font=("Sans-Serif", 12, "bold"),
        fg="#ffffff",  # Color del texto
        bg="#636cb4",  # Color de fondo del botón
        show=mostrar
        )
    return entry

def centrar_frame_principal(root):
    # Hacer que la ventana ajuste su tamaño según el contenido
    root.update_idletasks()  # Asegura que la ventana haya calculado su tamaño

    # Obtener las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Obtener las dimensiones de la ventana (después de que se haya ajustado al contenido)
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Calcular las coordenadas para centrar la ventana
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Establecer la geometría de la ventana con las coordenadas calculadas
    root.geometry(f"+{x}+{y}")

    #root.geometry("500x500")
    root.resizable(True, True)

# Obtener la IP local de la máquina
def obtener_ip_local():
    try:
        # Conecta a un servidor público (como Google DNS) para determinar la IP asignada
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Usa un servidor externo
        ip_externa = s.getsockname()[0]
        s.close()
        return ip_externa
    except Exception as e:
        return "No se pudo obtener la IP externa"