import os
import subprocess
import socket
import pyautogui
import io
import tkinter as tk
from tkinter import messagebox

def install_dependencies():
    """
    Verifica e instala las dependencias necesarias para capturar pantallas.
    """
    try:
        # Verificar si gnome-screenshot está instalado
        result = subprocess.run(["which", "gnome-screenshot"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not result.stdout:
            print("Instalando gnome-screenshot...")
            subprocess.run(["sudo", "apt", "install", "-y", "gnome-screenshot"], check=True)

        # Verificar e instalar Pillow
        try:
            import PIL
            from PIL import Image
            if not hasattr(PIL, 'PILLOW_VERSION') or int(PIL._version_.split('.')[0]) < 9:
                raise ImportError
        except ImportError:
            print("Instalando Pillow...")
            subprocess.run([os.sys.executable, "-m", "pip", "install", "Pillow>=9.2.0"], check=True)

        print("Todas las dependencias están instaladas.")
    except Exception as e:
        messagebox.showerror("Error de instalación", f"No se pudieron instalar las dependencias: {e}")
        raise

def get_local_ip():
    """
    Obtiene la IP local de la interfaz de red activa.
    """
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception as e:
        print(f"Error obteniendo la IP local: {e}")
        return "No se pudo obtener la IP"

def start_screen_monitoring_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = get_local_ip()
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Esperando conexiones en {host}:{port}...")

    ip_label.config(text=f"IP: {host}")
    port_label.config(text=f"Puerto: {port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Conexión establecida con {addr}")

            try:
                while True:
                    screenshot = pyautogui.screenshot()
                    byte_array = io.BytesIO()
                    screenshot.save(byte_array, format='JPEG')
                    image_data = byte_array.getvalue()

                    client_socket.sendall(len(image_data).to_bytes(4, byteorder='big'))
                    client_socket.sendall(image_data)
            except Exception as e:
                print(f"Error con {addr}: {e}")
            finally:
                print(f"Cerrando conexión con {addr}")
                client_socket.close()
    finally:
        server_socket.close()

# Crear la ventana principal
root = tk.Tk()
root.title("Servidor de Monitoreo de Pantalla")

ip_label = tk.Label(root, text="Esperando IP...")
ip_label.pack(pady=10)

port_label = tk.Label(root, text="Esperando puerto...")
port_label.pack(pady=10)

port = 12345

# Instalar dependencias antes de iniciar el servidor
try:
    install_dependencies()
except Exception:
    root.destroy()
    exit(1)

# Iniciar el servidor en un hilo separado
import threading
server_thread = threading.Thread(target=start_screen_monitoring_server, args=(port,), daemon=True)
server_thread.start()

root.geometry("600x400")
root.mainloop()