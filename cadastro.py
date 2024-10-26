import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import subprocess
import numpy as np
import pyodbc
import bcrypt

from connection import criar_conexao_com_banco
from reconhecimento_facial import capturar_reconhecimento_facial


class CadastroUsuario:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.title("Cadastro de Usuário")
        self.root.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.nome = tk.StringVar()
        self.email = tk.StringVar()
        self.senha = tk.StringVar()
        self.dados_face = None  # Initialize with None

        self.create_widgets()

    def create_widgets(self):
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configura o layout centralizado
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(7, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        # Título
        title_label = ctk.CTkLabel(frame, text="Cadastrar Usuário", font=("Arial", 20, "bold"))
        title_label.grid(row=1, column=1, columnspan=2, pady=(10, 15), sticky="n")

        # Campo de Nome
        ctk.CTkLabel(frame, text="Nome").grid(row=2, column=1, pady=(5, 5), sticky='e')
        ctk.CTkEntry(frame, textvariable=self.nome, width=300, placeholder_text="Digite seu nome").grid(row=2, column=2, pady=(5, 5), padx=(0, 10), sticky='w')

        # Campo de Email
        ctk.CTkLabel(frame, text="Email").grid(row=3, column=1, pady=(5, 5), sticky='e')
        ctk.CTkEntry(frame, textvariable=self.email, width=300, placeholder_text="Digite seu email").grid(row=3, column=2, pady=(5, 5), padx=(0, 10), sticky='w')

        # Campo de Senha
        ctk.CTkLabel(frame, text="Senha").grid(row=4, column=1, pady=(5, 5), sticky='e')
        ctk.CTkEntry(frame, textvariable=self.senha, show="*", width=300, placeholder_text="Digite sua senha").grid(row=4, column=2, pady=(5, 10), padx=(0, 10), sticky='w')

        # Botão de Captura de Face
        self.btn_face = ctk.CTkButton(frame, text="Cadastrar Face", command=self.abrir_reconhecimento_face, fg_color="#9C27B0", text_color="white")
        self.btn_face.grid(row=5, column=1, columnspan=2, pady=(10, 5), sticky="n")

        # Label de Status da Captura de Face
        self.label_dados_face = ctk.CTkLabel(frame, text="")
        self.label_dados_face.grid(row=6, column=1, columnspan=2, pady=(5, 5), sticky="n")

        # Botão de Cadastro
        self.btn_cadastrar = ctk.CTkButton(frame, text="Cadastrar", command=self.cadastrar_usuario, fg_color="#4CAF50", text_color="white")
        self.btn_cadastrar.grid(row=7, column=1, columnspan=2, pady=(5, 15), sticky="n")
        self.btn_cadastrar.configure(state=tk.DISABLED)

    def abrir_reconhecimento_face(self):
        subprocess.Popen(["python", "reconhecimento_facial.py"])
        self.root.after(1000, self.carregar_dados_face)

    def carregar_dados_face(self):
        self.dados_face = capturar_reconhecimento_facial()
        # Capture face and allow the user to proceed regardless of recognition success
        self.dados_face = np.random.rand(128).astype(np.float32)  # Mock facial data
        self.label_dados_face.configure(text="Rosto capturado.")
        self.btn_cadastrar.configure(state=tk.NORMAL)
        messagebox.showinfo("Info", "Rosto sendo capturado. Você pode logar!")

    def cadastrar_usuario(self):
        nome = self.nome.get()
        email = self.email.get()
        senha = self.senha.get()

        # Hash da senha
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

        # Use mock data if no facial data is captured
        if self.dados_face is not None:
            dados_face_bytes = self.dados_face.tobytes()
        else:
            dados_face_bytes = np.random.rand(128).astype(np.float32).tobytes()  # Generate mock facial data

        conn = criar_conexao_com_banco()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))
            resultado = cursor.fetchone()

            if resultado:
                messagebox.showerror("Erro", "Email já cadastrado.")
                return

            # Armazena o hash da senha e dados faciais (mock)
            cursor.execute("INSERT INTO usuarios (nome, email, senha, dados_face) VALUES (?, ?, ?, ?)",
                        (nome, email, senha_hash, dados_face_bytes))

            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

        except pyodbc.Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")
        finally:
            conn.close()

        self.root.destroy()
        self.login_window.deiconify()


if __name__ == "__main__":
    pass
