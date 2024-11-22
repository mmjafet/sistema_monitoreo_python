import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import paramiko
from plantilla import crear_label, create_entry, create_button, centrar_frame_principal, create_frame_horizontal

# Función para ejecutar comandos con sudo
def run_command(command, password):
    full_command = f"echo {password} | sudo -S {command}"
    try:
        result = subprocess.run(full_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando el comando: {e.stderr.decode()}")

# Función para bloquear un dominio
def bloquear_pagina():
    dominio = dominio_entry.get()
    ip = ip_entry.get()
    usuario = usuario_entry.get()
    contraseña = password_entry.get()
    password_sudo = password_sudo_entry.get()

    if dominio and ip and usuario and contraseña and password_sudo:
        # Comandos para conectarse y bloquear el dominio en /etc/hosts
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=usuario, password=contraseña)

            # Comando para agregar el dominio al archivo /etc/hosts
            comando = f"echo '127.0.0.1 {dominio}' | sudo tee -a /etc/hosts"
            stdin, stdout, stderr = ssh.exec_command(comando, get_pty=True)
            stdin.write(f"{password_sudo}\n")
            stdin.flush()

            # Leer salida y errores
            salida = stdout.read().decode()
            error = stderr.read().decode()

            if salida:
                print(f"Salida: {salida}")
            if error:
                print(f"Error: {error}")

            ssh.close()
            messagebox.showinfo("Éxito", f"La página {dominio} ha sido bloqueada.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al intentar bloquear la página: {e}")
    else:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")

# Función para desbloquear un dominio
def desbloquear_pagina():
    dominio = dominio_entry.get()
    ip = ip_entry.get()
    usuario = usuario_entry.get()
    contraseña = password_entry.get()
    password_sudo = password_sudo_entry.get()

    if dominio and ip and usuario and contraseña and password_sudo:
        # Comandos para conectarse y desbloquear el dominio en /etc/hosts
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=usuario, password=contraseña)

            # Comando para eliminar el dominio del archivo /etc/hosts
            comando = f"sudo sed -i '/{dominio}/d' /etc/hosts"
            stdin, stdout, stderr = ssh.exec_command(comando, get_pty=True)
            stdin.write(f"{password_sudo}\n")
            stdin.flush()

            # Leer salida y errores
            salida = stdout.read().decode()
            error = stderr.read().decode()

            if salida:
                print(f"Salida: {salida}")
            if error:
                print(f"Error: {error}")

            ssh.close()
            messagebox.showinfo("Éxito", f"La página {dominio} ha sido desbloqueada.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al intentar desbloquear la página: {e}")
    else:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Bloquear/Desbloquear Páginas")
root.configure(bg="#0f1440")

# Titulo
action_label = tk.Label(root, text="Bloquear/Desbloquear página", font=("Segoe UI", 25, "bold"), fg="#ecf0f1", bg="#0f1440")
action_label.pack(fill="x", pady=(20, 30))

# Campos para ingresar los datos
#-------------------Frame para IP-------------------
frame_ip = create_frame_horizontal(root)
frame_ip.pack(padx=10, pady=10)

crear_label("Dominio a bloquear/desbloquear:", frame_ip).grid(row=0, column=0, padx=10, ipadx=20, ipady=10)
dominio_entry = tk.Entry(frame_ip, font=("Arial", 12), width=40)
dominio_entry.grid(row=0, column=1, padx=10, ipadx=20, ipady=10)

crear_label("IP del servidor:", root).pack(pady=5)
ip_entry = tk.Entry(root, font=("Arial", 12), width=40)
ip_entry.pack(pady=5)

crear_label("Usuario:", root).pack(pady=5)
usuario_entry = tk.Entry(root, font=("Arial", 12), width=40)
usuario_entry.pack(pady=5)

crear_label("Contraseña:", root).pack(pady=5)
password_entry = tk.Entry(root, font=("Arial", 12), width=40, show="*")
password_entry.pack(pady=5)

crear_label("Contraseña administrador:", root).pack(pady=5)
password_sudo_entry = tk.Entry(root, font=("Arial", 12), width=40, show="*")
password_sudo_entry.pack(pady=5)

# Botones para bloquear y desbloquear
bloquear_button = tk.Button(root, text="Bloquear Página", font=("Arial", 12), bg="#282e61", fg="#ffffff", command=bloquear_pagina)
bloquear_button.pack(pady=10)

desbloquear_button = tk.Button(root, text="Desbloquear Página", font=("Arial", 12), bg="#282e61", fg="#ffffff", command=desbloquear_pagina)
desbloquear_button.pack(pady=10)

#-----------Ajustar el tamaño de la ventana--------

centrar_frame_principal(root)
root.mainloop()
