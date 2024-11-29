import paramiko
from scp import SCPClient
import tkinter as tk
from tkinter import filedialog, messagebox
from plantilla import create_frame_horizontal, crear_label, create_button, create_entry, centrar_frame_principal


# Función para seleccionar el archivo a enviar
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo")
    archivo_entry.delete(0, tk.END)
    archivo_entry.insert(0, archivo)

# Función para enviar el archivo (de local a remoto)
def enviar_archivo():
    try:
        # Obtener los valores de los campos de la interfaz
        hostname = ip_entry.get()
        username = usuario_entry.get()
        password = contrasena_entry.get()
        file_path = archivo_entry.get()
        destino = destino_entry.get()

        if not hostname or not username or not password or not file_path or not destino:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Establecer la conexión SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)

        # Transferir el archivo usando SCP
        with SCPClient(client.get_transport()) as scp:
            scp.put(file_path, destino)

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "El archivo se ha transferido correctamente.")

        # Cerrar la conexión SSH
        client.close()

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema: {e}")

# Función para recibir el archivo (de remoto a local)
def recibir_archivo():
    try:
        # Obtener los valores de los campos de la interfaz
        hostname = ip_entry.get()
        username = usuario_entry.get()
        password = contrasena_entry.get()
        archivo_remoto = archivo_entry.get()
        destino_local = destino_entry.get()

        if not hostname or not username or not password or not archivo_remoto or not destino_local:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Establecer la conexión SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)

        # Transferir el archivo usando SCP desde remoto a local
        with SCPClient(client.get_transport()) as scp:
            scp.get(archivo_remoto, destino_local)

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "El archivo se ha recibido correctamente.")

        # Cerrar la conexión SSH
        client.close()

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Compartir Archivos")
root.configure(bg="#0f1440")

tk.Label(root, text="Compartir Archivos", font=("Arial", 18, "bold"), fg="#cdd4ea", bg="#0f1440").pack(pady=10)

#-------------------Frame para datos-------------------
frame_data = create_frame_horizontal(root)
frame_data.pack(padx=10, pady=10)


# Crear los campos de la interfaz
crear_label("Dirección IP de la PC de destino", frame_data).grid(row=0, column=0, padx=10, ipadx=20, ipady=10)
ip_entry = create_entry(frame_data,"")
ip_entry.grid(row=0, column=1, padx=10, pady = 15, ipadx=20, ipady=7)

crear_label("Usuario", frame_data).grid(row=1, column=0, padx=10, ipadx=20, ipady=10)
usuario_entry = create_entry(frame_data, "")
usuario_entry.grid(row=1, column=1, padx=10, pady = 15, ipadx=20, ipady=7)

crear_label("Contraseña", frame_data).grid(row=2, column=0, padx=10, ipadx=20, ipady=10)
contrasena_entry = create_entry(frame_data, "*")
contrasena_entry.grid(row=2, column=1, padx=10, pady = 15, ipadx=20, ipady=7)

crear_label("Seleccionar archivo a enviar", frame_data).grid(row=3, column=0, padx=10, ipadx=20, ipady=10)
archivo_entry = create_entry(frame_data, "")
archivo_entry.grid(row=3, column=1, padx=10, pady = 15, ipadx=20, ipady=7)

seleccionar_button = create_button(frame_data, "Seleccionar archivo", seleccionar_archivo)
seleccionar_button.grid(row=3, column=2, padx=10, pady=5)

crear_label("Ruta de destino en la PC remota o local", frame_data).grid(row=4, column=0, padx=10, ipadx=20, ipady=10)
destino_entry = create_entry(frame_data, "")
destino_entry.grid(row=4, column=1, padx=10, pady = 15, ipadx=20, ipady=7)

# Botones para enviar o recibir archivos
enviar_button = create_button(frame_data, "Enviar archivo", enviar_archivo)
enviar_button.grid(row=5, column=0, padx=10, pady=20)

# recibir_button = create_button(frame_data, "Recibir archivo", recibir_archivo)
# recibir_button.grid(row=5, column=1, padx=10, pady=20)

#-----------Ajustar el tamaño de la ventana--------

centrar_frame_principal(root)
# Iniciar la interfaz gráfica
root.mainloop()