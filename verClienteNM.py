import subprocess
from tkinter import simpledialog, messagebox

def ejecutar_nomachine():
    # Solicitar la contraseña de sudo
    sudo_password = simpledialog.askstring("Contraseña Sudo", "Introduce la contraseña de sudo:", show="*")
    if not sudo_password:
        messagebox.showerror("Error", "La contraseña de sudo es obligatoria.")
        return

    try:
        # Ejecutar el comando para iniciar NoMachine en tu equipo local
        comando = f"echo {sudo_password} | sudo -S /usr/NX/NX/bin/nxplayer"
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            messagebox.showerror("Error", f"Se produjo un error al ejecutar el comando:\n{resultado.stderr}")
        else:
            messagebox.showinfo("Éxito", "El comando 'nomachine' se ejecutó correctamente en tu equipo local.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error: {str(e)}")

# Llamada para ejecutar el comando directamente en la terminal
ejecutar_nomachine()