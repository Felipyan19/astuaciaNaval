import socket
import pickle
import numpy as np
import json
import threading
import tkinter as tk

users = {}
client_scores = {'id1': 0, 'id2': 0}  # Inicializa las puntuaciones para ambos jugadores

def compare_matrices(matrix1, matrix2):
    for i in range(len(matrix1)):
        for j in range(len(matrix1[i])):
            if matrix1[i][j] == 1 and matrix2[i][j] == 1:
                return True  # Hay un "1" en la misma posición, disparo acertado
    return False

def server():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    first_matrix_received = {}
    print(f"Server is listening on {host}:{port}")
    while True:
        client_socket, addr = server_socket.accept()

        data = client_socket.recv(4096)

        if not data:
            break

        response = ""
        received_id = "Cliente nuevo"
        received_matrix = None

        received_data = data.decode('utf-8')
        if received_data == "Nueva conexion":
            for user_id in range(1, 3):
                if f"id{user_id}" not in users:
                    users[f"id{user_id}"] = addr
                    response = f"id{user_id}"
                    break
            else:
                response = "No hay usuarios disponibles en este momento"

        else:
            received_data = json.loads(received_data)
            received_id = received_data['id']
            received_matrix = received_data['matrix']

            if received_id == "id1":
                another_id = "id2"
            else:
                another_id = "id1"

            if received_id not in first_matrix_received:
                first_matrix_received[received_id] = received_matrix
                response = "Barcos registrados correctamente"
            else:
                if compare_matrices(first_matrix_received[another_id], received_matrix):
                    response = "Disparo acertado"
                    client_scores[received_id] += 1
                else:
                    response = "Disparo fallido"
            print(f"Puntuación de {received_id}: {client_scores[received_id]}")

        client_socket.send(response.encode('utf-8'))

        # Notificar a la interfaz de usuario después de cada disparo
        update_gui()

        client_socket.close()

def start_server():
    server()

server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

def create_gui():
    global label2, label3  # Hacer que las etiquetas sean globales

    root = tk.Tk()
    label = tk.Label(root, text="Puntuación")
    label.pack()

    label2 = tk.Label(root, text=f"Puntuación Player 1: {client_scores['id1']}")
    label2.pack()

    label3 = tk.Label(root, text=f"Puntuación Player 2: {client_scores['id2']}")
    label3.pack()

    root.mainloop()

def update_gui():
    # Actualizar el contenido de las etiquetas dentro de esta función
    label2.config(text=f"Puntuación Player 1: {client_scores['id1']}")
    label3.config(text=f"Puntuación Player 2: {client_scores['id2']}")

gui_thread = threading.Thread(target=create_gui)
gui_thread.start()
