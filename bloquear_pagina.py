import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import paramiko
from plantilla import crear_label, create_entry, create_button, centrar_frame_principal, create_frame_horizontal, obtener_ip_local

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

# Mostrar la dirección IP de la máquina
ip_local_label = tk.Label(root, text=f"Tu IP es: {obtener_ip_local()}", font=("Segoe UI", 14), fg="#ecf0f1", bg="#0f1440")
ip_local_label.pack(fill="x", pady=(0, 20))

# Campos para ingresar los datos
#-------------------Frame para IP-------------------
frame_ip = create_frame_horizontal(root)
frame_ip.pack(padx=10, pady=10)

crear_label("Dominio de página:", frame_ip).grid(row=0, column=0, padx=10, ipadx=20, ipady=10)
dominio_entry = create_entry(frame_ip, "")
dominio_entry.grid(row=0, column=1, padx=10, pady = 15, ipadx=20, ipady=7)

crear_label("IP remota:", frame_ip).grid(row=1, column=0, padx=10, ipadx=20, ipady=10)
ip_entry = create_entry(frame_ip,"")
ip_entry.grid(row=1, column=1, padx=10, pady = 15, ipadx=20, ipady=7)

crear_label("Usuario:", frame_ip).grid(row=2, column=0, padx=10, ipadx=20, ipady=10)
usuario_entry = create_entry(frame_ip, "")
usuario_entry.grid(row=2, column=1, padx=10, pady = 15, ipadx=20, ipady=7)

crear_label("Contraseña:", frame_ip).grid(row=3, column=0, padx=10, ipadx=20, ipady=10)
password_entry = create_entry(frame_ip,"*")
password_entry.grid(row=3, column=1, padx=10, pady = 15, ipadx=20, ipady=7)

crear_label("Contraseña administrador:", frame_ip).grid(row=4, column=0, padx=10, ipadx=20, ipady=10)
password_sudo_entry = create_entry(frame_ip, "*")
password_sudo_entry.grid(row=4, column=1, padx=10, pady = 15, ipadx=20, ipady=7)

# Botones para bloquear y desbloquear
bloquear_button = create_button(frame_ip, "Bloquear Página", bloquear_pagina)
bloquear_button.grid(row=5, column=0, padx=10, pady=20)

desbloquear_button = create_button(frame_ip, "Desbloquear Página", desbloquear_pagina)
desbloquear_button.grid(row=5, column=1, padx=10, pady=20)

#-----------Ajustar el tamaño de la ventana--------

centrar_frame_principal(root)
root.mainloop()
