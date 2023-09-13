import tkinter as tk
import socket
import pickle
import numpy as np
import json

class MatrixEditor:
    host = '127.0.0.1'
    port = 12345
    global id
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    response = "Nueva conexion"
    client_socket.send(response.encode('utf-8'))
    id = client_socket.recv(4096).decode('utf-8')
    client_socket.close()

    def __init__(self, root):
        self.root = root

        if id == "id1":
            self.root.title("Player 1")
        else:
            self.root.title("Player 2")

        self.root.geometry("300x400")  # Ancho x Alto
        self.matrix1 = np.zeros((3, 3), dtype=int)
        self.matrix2 = np.zeros((3, 3), dtype=int)
        self.last_shot_matrix = None
        self.matrix1_buttons = [[None, None, None], [None, None, None], [None, None, None]]
        self.matrix2_buttons = [[None, None, None], [None, None, None], [None, None, None]]

        title_label1 = tk.Label(root, text="Disparos", font=("Helvetica", 16))
        title_label1.grid(row=0, column=0, columnspan=3)

        title_label2 = tk.Label(root, text="Barcos", font=("Helvetica", 16))
        title_label2.grid(row=4, column=0, columnspan=3)
        
        self.create_matrix_frame(self.matrix1, self.matrix1_buttons, 1)
        self.create_matrix_frame(self.matrix2, self.matrix2_buttons, 5)

        for i in range(3):
            for j in range(3):
                self.matrix1_buttons[i][j].config(state=tk.DISABLED)

        self.Disparo = tk.Button(root, text="Disparar", command=self.print_and_send_matrices)
        self.Disparo.grid(row=9, column=0, columnspan=3)

        self.Disparo.grid_remove()

        self.send_matrix2_button = tk.Button(root, text="Registrar barcos", command=self.send_barcos)
        self.send_matrix2_button.grid(row=10, column=0, columnspan=3)

    def create_matrix_frame(self, matrix, button_matrix, row_offset):
        matrix_frame = tk.Frame(self.root)
        matrix_frame.grid(row=row_offset, column=0, padx=10, pady=10)

        for i in range(3):
            for j in range(3):
                button = tk.Button(matrix_frame, text=str(matrix[i][j]), width=5,
                                   command=lambda r=i, c=j: self.toggle_button(matrix, button_matrix, r, c))
                button.grid(row=i, column=j)
                button_matrix[i][j] = button

    def toggle_button(self, matrix, button_matrix, row, col):
        matrix[row][col] = 1 if matrix[row][col] == 0 else 0
        button_matrix[row][col].config(text=str(matrix[row][col]))
        self.last_shot_matrix = np.zeros((3, 3), dtype=int)
        self.last_shot_matrix[row][col] = matrix[row][col]

        for i in range(3):
            for j in range(3):
                self.matrix1_buttons[i][j].config(state=tk.DISABLED)

    def print_and_send_matrices(self):
        self.send_matrix_to_server(self.last_shot_matrix)

        for i in range(3):
            for j in range(3):
                self.matrix1_buttons[i][j].config(state=tk.NORMAL)

    def send_barcos(self):
        self.send_matrix_to_server(self.matrix2)

        for i in range(3):
            for j in range(3):
                self.matrix2_buttons[i][j].config(state=tk.DISABLED)

        self.send_matrix2_button.grid_remove()
        self.Disparo.grid()

        for i in range(3):
            for j in range(3):
                self.matrix1_buttons[i][j].config(state=tk.NORMAL)

    def send_matrix_to_server(self, matrix):
        host = '127.0.0.1'
        port = 12345
        matrix_as_list = matrix.tolist()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        data_to_send = {
            'id': id,  
            'matrix': matrix_as_list  
        }
        json_data = json.dumps(data_to_send)
        client_socket.send(json_data.encode('utf-8'))   
        data = client_socket.recv(1024)

        if data.decode('utf-8') == "Disparo acertado":
            for i in range(3):
                for j in range(3):
                    if self.last_shot_matrix[i][j] == 1:
                        self.matrix1_buttons[i][j].config(bg='green') 
                        self.matrix1_buttons[i][j].config(state=tk.DISABLED)

        client_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixEditor(root)  # Sin argumentos aquí
    root.mainloop()


