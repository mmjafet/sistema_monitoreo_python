import socket
import cv2
import pickle
import struct

def start_client(server_ip='172.168.1.242', port=9999):
    # Crear socket del cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print(f"[INFO] Conectado al servidor {server_ip}:{port}")

    try:
        data = b""
        payload_size = struct.calcsize("Q")

        while True:
            # Recibir datos del servidor
            while len(data) < payload_size:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet

            # Extraer tamaño del paquete
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4096)

            # Deserializar datos
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)

            # Mostrar la pantalla
            cv2.imshow("Pantalla del Servidor", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"[ERROR] Ocurrió un error: {e}")
    finally:
        client_socket.close()
        cv2.destroyAllWindows()
        print("[INFO] Conexión cerrada.")

if __name__ == "__main__":
    start_client()