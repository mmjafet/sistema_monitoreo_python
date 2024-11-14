import tkinter as tk
from tkinter import messagebox
import os

def verificar_conexion(ip):
    respuesta = os.system(f"ping -n 1 {ip} >nul")
    return respuesta == 0

def apagar_equipo():
    ip = entry_ip.get().strip()
    usuario = entry_usuario.get().strip()
    contrasena = entry_contrasena.get().strip()

    if ip and usuario and contrasena:
        # Verifica si se puede hacer ping a la IP
        if verificar_conexion(ip):
            try:
                # Reemplaza con el comando correcto de psshutdown o cualquier herramienta similar
                resultado = os.system(f'psshutdown.exe -s -u {usuario} -p {contrasena} \\\\{ip}')

                if resultado == 0:
                    messagebox.showinfo("Éxito", f"El equipo con IP {ip} se está apagando.")
                else:
                    messagebox.showerror("Error", "No se pudo apagar el equipo. Verifica permisos y configuración.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al intentar apagar el equipo: {e}")
        else:
            messagebox.showwarning("Advertencia", f"No se pudo conectar con el equipo {ip}. Verifica la IP y la conexión.")
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese todos los campos requeridos.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Apagar Equipo Remoto")

# Crear y colocar los widgets
label_ip = tk.Label(ventana, text="Dirección IP del equipo:")
label_ip.pack(pady=5)

entry_ip = tk.Entry(ventana)
entry_ip.pack(pady=5)

label_usuario = tk.Label(ventana, text="Usuario:")
label_usuario.pack(pady=5)

entry_usuario = tk.Entry(ventana)
entry_usuario.pack(pady=5)

label_contrasena = tk.Label(ventana, text="Contraseña:")
label_contrasena.pack(pady=5)

entry_contrasena = tk.Entry(ventana, show="*")
entry_contrasena.pack(pady=5)

boton_apagar = tk.Button(ventana, text="Apagar", command=apagar_equipo)
boton_apagar.pack(pady=20)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
