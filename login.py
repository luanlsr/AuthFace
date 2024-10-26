import tkinter as tk
import bcrypt
import customtkinter as ctk
from tkinter import messagebox
from cadastro import CadastroUsuario
import subprocess
import os
import pickle
import numpy as np


from connection import criar_conexao_com_banco


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.email = tk.StringVar()
        self.senha = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configura o layout centralizado
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        # Título
        title_label = ctk.CTkLabel(frame, text="Login", font=("Arial", 20, "bold"))
        title_label.grid(row=1, column=1, pady=(10, 15), sticky="n")

        # Campo de Email
        ctk.CTkLabel(frame, text="Email").grid(row=2, column=0, pady=(5, 5), sticky='e')
        ctk.CTkEntry(frame, textvariable=self.email, width=300, placeholder_text="Digite seu email").grid(row=2, column=1, pady=(5, 5), padx=(0, 10), sticky='w')

        # Campo de Senha
        ctk.CTkLabel(frame, text="Senha").grid(row=3, column=0, pady=(5, 5), sticky='e')
        ctk.CTkEntry(frame, textvariable=self.senha, show="*", width=300, placeholder_text="Digite sua senha").grid(row=3, column=1, pady=(5, 10), padx=(0, 10), sticky='w')
        
        # Botões
        self.btn_login = ctk.CTkButton(frame, text="Login", command=self.realizar_login, fg_color="#4CAF50", text_color="white")
        self.btn_login.grid(row=4, column=1, pady=(10, 5), sticky="n")

        self.btn_biometria = ctk.CTkButton(frame, text="Login com Biometria", command=self.abrir_reconhecimento_face, fg_color="#9C27B0", text_color="white")
        self.btn_biometria.grid(row=5, column=1, pady=5, sticky="n")

        self.btn_cadastrar = ctk.CTkButton(frame, text="Cadastrar", command=self.abrir_tela_cadastro, fg_color="#2196F3", text_color="white")
        self.btn_cadastrar.grid(row=6, column=1, pady=(5, 10), sticky="n")

        # Configuração do espaçamento para centralizar o formulário
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(7, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(2, weight=1)

    def realizar_login(self):
        email = self.email.get()
        senha = self.senha.get()

        conn = criar_conexao_com_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()

        if usuario and bcrypt.checkpw(senha.encode(), usuario[3]):  # Verifique o hash da senha
            messagebox.showinfo("Sucesso", f"Bem-vindo, {email}!")
            self.abrir_home(usuario)
        else:
            messagebox.showerror("Erro", "Email ou senha inválidos.")
        conn.close()

    def abrir_reconhecimento_face(self):
        subprocess.Popen(["python", "reconhecimento_facial.py"])
        self.root.after(2000, self.verificar_dados_facial)

    def verificar_dados_facial(self):
        conn = criar_conexao_com_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        if os.path.exists('dados_face.pkl'):
            with open('dados_face.pkl', 'rb') as f:
                dados_face = pickle.load(f)
            
            for usuario in usuarios:
                dados_face_banco = np.frombuffer(usuario[4], dtype=dados_face.dtype).reshape(dados_face.shape)

                # Comparar com os dados faciais armazenados no banco de dados
                if np.array_equal(dados_face_banco, dados_face):
                    messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario[1]}!")
                    self.abrir_home(usuario)
                    conn.close()
                    return

            messagebox.showerror("Erro", "Rosto desconhecido ou usuário não cadastrado.")
        else:
            messagebox.showerror("Erro", "Dados faciais não encontrados.")
        
        conn.close()

    def abrir_tela_cadastro(self):
        self.root.withdraw()
        root_cadastro = tk.Toplevel(self.root)
        CadastroUsuario(root_cadastro, self.root)

    def abrir_home(self, usuario):
        self.root.withdraw()
        home = tk.Toplevel(self.root)
        home.title("Home")
        home.geometry("800x600")

        # Acesso usando índices em vez de chaves
        nome_usuario = usuario[1]  # índice para o nome
        email_usuario = usuario[2]  # índice para o email

        ctk.CTkLabel(home, text=f"Bem-vindo, {nome_usuario}!").pack(pady=20)
        ctk.CTkLabel(home, text=f"Email: {email_usuario}").pack(pady=10)
        ctk.CTkLabel(home, text="Dados Biométricos: Capturados").pack(pady=10)

        ctk.CTkButton(home, text="Logout", command=lambda: self.logout(home)).pack(pady=10)

    def logout(self, home_window):
        home_window.destroy()
        self.root.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()
