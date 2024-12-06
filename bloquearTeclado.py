import paramiko
import tkinter as tk
from tkinter import simpledialog, messagebox
from plantilla import create_frame_horizontal, crear_label, create_button, create_entry, centrar_frame_principal, obtener_ip_local

def ejecutar_comando_ssh(ip, username, password, comando, mensaje_exito):
    # Solicitar la contraseña de sudo
    sudo_password = simpledialog.askstring("Contraseña Sudo", "Introduce la contraseña de sudo:", show="*")
    if not sudo_password:
        messagebox.showerror("Error", "La contraseña de sudo es obligatoria.")
        return

    try:
        # Conexión SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if not ip or not username or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        client.connect(hostname=ip, username=username, password=password)

        # Ejecutar el comando
        full_command = f"echo {sudo_password} | sudo -S {comando}"
        stdin, stdout, stderr = client.exec_command(full_command)

        # Leer posibles errores
        error = stderr.read().decode()
        if error:
            messagebox.showerror("Éxito", f"Comando ejecutado:\n{error}")
        else:
            messagebox.showinfo("Éxito", mensaje_exito)
    except Exception as e:
        messagebox.showerror("Error de conexión", str(e))
    finally:
        client.close()

def bloquear_teclado_mouse():
    ip = ip_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    comando = "killall -STOP gnome-shell"
    ejecutar_comando_ssh(ip, username, password, comando, "El teclado y mouse han sido bloqueados.")
    bloquear_button.config(state=tk.DISABLED)  # Deshabilitar el botón de bloquear
    desbloquear_button.config(state=tk.NORMAL)  # Habilitar el botón de desbloquear

def desbloquear_teclado_mouse():
    ip = ip_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    comando = "killall -CONT gnome-shell"
    ejecutar_comando_ssh(ip, username, password, comando, "El teclado y mouse han sido desbloqueados.")
    desbloquear_button.config(state=tk.DISABLED)  # Deshabilitar el botón de desbloquear
    bloquear_button.config(state=tk.NORMAL)  # Habilitar el botón de bloquear

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Control de teclado y mouse remoto")
root.configure(bg="#0f1440")

tk.Label(root, text="Control de teclado y mouse", font=("Arial", 18, "bold"), fg="#cdd4ea", bg="#0f1440").pack(pady=10)

# Mostrar la dirección IP de la máquina
ip_local_label = tk.Label(root, text=f"Tu IP es: {obtener_ip_local()}", font=("Segoe UI", 14), fg="#ecf0f1", bg="#0f1440")
ip_local_label.pack(fill="x", pady=(0, 20))

#-------------------Frame para IP-------------------
frame_ip = create_frame_horizontal(root)
frame_ip.pack(padx=10, pady=10)

# Campos para IP, nombre de usuario y contraseña
crear_label("IP remota", frame_ip).grid(row=0, column=0, padx=10, ipadx=20, ipady=10)
ip_entry = create_entry(frame_ip,"")
ip_entry.grid(row=0, column=1, padx=10, ipadx=20, ipady=10)

#-----------------Frame para Usuario-------------------
frame_user = create_frame_horizontal(root)
frame_user.pack(padx=10, pady=10)
crear_label("Usuario:", frame_user).grid(row=0, column=0, padx=10, ipadx=20, ipady=10)
username_entry = create_entry(frame_user,"")
username_entry.grid(row=0, column=1, padx=10, ipadx=20, ipady=10)

#-----------------Frame para Contraseña-------------------
frame_psw = create_frame_horizontal(root)
frame_psw.pack(padx=10, pady=10)
crear_label("Contraseña", frame_psw).grid(row=0, column=0, padx=10, ipadx=20, ipady=10)
password_entry = create_entry(frame_psw, "*")
password_entry.grid(row=0, column=1, padx=10, ipadx=20, ipady=10)

# Botones para bloquear y desbloquear
frame_buttons = create_frame_horizontal(root)
frame_buttons.pack(padx=10, pady=20)

bloquear_button = create_button(frame_buttons, "Bloquear", bloquear_teclado_mouse)
bloquear_button.grid(row=0, column=0, padx=20)

desbloquear_button = create_button(frame_buttons, "Desbloquear", desbloquear_teclado_mouse)
desbloquear_button.grid(row=0, column=1, padx=20)
desbloquear_button.config(state=tk.DISABLED)  # Inicialmente deshabilitar el botón de desbloquear

#-----------Ajustar el tamaño de la ventana--------

centrar_frame_principal(root)

# Iniciar el bucle principal de la interfaz
root.mainloop()
