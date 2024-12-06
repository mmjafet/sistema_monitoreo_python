import paramiko
import tkinter as tk
from tkinter import simpledialog, messagebox
from plantilla import create_frame_horizontal, crear_label, create_button, create_entry, centrar_frame_principal, obtener_ip_local

def apagar_computadora():
    # Solicitar la contraseña de sudo
    sudo_password = simpledialog.askstring("Contraseña Sudo", "Introduce la contraseña de sudo:", show="*")
    if not sudo_password:
        messagebox.showerror("Error", "La contraseña de sudo es obligatoria.")
        return

    try:
        # Conexión SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Solicitar detalles de conexión
        ip = ip_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        if not ip or not username or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        client.connect(hostname=ip, username=username, password=password)

        # Ejecutar el comando de apagado
        comando = f"echo {sudo_password} | sudo -S shutdown -h now"
        stdin, stdout, stderr = client.exec_command(comando)

        # Leer posibles errores
        error = stderr.read().decode()
        if error:
            messagebox.showerror("Éxito", f"El comando de apagado se ejecutó correctamente:\n{error}")
        else:
            messagebox.showinfo("Éxito", "El comando de apagado se ejecutó correctamente.")
    except Exception as e:
        messagebox.showerror("Error de conexión", str(e))
    finally:
        client.close()

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Apagar computadora remota")
root.configure(bg="#0f1440")

tk.Label(root, text="Detalles de conexión", font=("Arial", 18, "bold"), fg="#cdd4ea", bg="#0f1440").pack(pady=10)

# Mostrar la dirección IP de la máquina
ip_local_label = tk.Label(root, text=f"Tu IP es: {obtener_ip_local()}", font=("Segoe UI", 14), fg="#ecf0f1", bg="#0f1440")
ip_local_label.pack(fill="x", pady=(0, 20))

#-------------------Frame para ip-------------------
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
password_entry = create_entry(frame_psw,"*")
password_entry.grid(row=0, column=1, padx=10, ipadx=20, ipady=10)

# Botón para apagar
apagar_button = create_button(root, "Apagar Computadora", apagar_computadora)
apagar_button.pack(pady=20)

#-----------Ajustar el tamaño de la ventana--------

centrar_frame_principal(root)

# Iniciar el bucle principal de la interfaz
root.mainloop()