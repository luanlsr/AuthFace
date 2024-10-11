import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import pickle

class CadastroUsuario:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Usuário")
        self.root.geometry("400x400")

        self.nome = tk.StringVar()
        self.email = tk.StringVar()
        self.senha = tk.StringVar()
        self.reconhecimento_face_realizado = False
        self.dados_face = ""

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Nome").pack(pady=5)
        tk.Entry(self.root, textvariable=self.nome).pack(pady=5)

        tk.Label(self.root, text="Email").pack(pady=5)
        tk.Entry(self.root, textvariable=self.email).pack(pady=5)

        tk.Label(self.root, text="Senha").pack(pady=5)
        tk.Entry(self.root, textvariable=self.senha, show="*").pack(pady=5)

        self.btn_face = tk.Button(self.root, text="Cadastrar Face", command=self.abrir_reconhecimento_face)
        self.btn_face.pack(pady=10)

        self.label_dados_face = tk.Label(self.root, text="")
        self.label_dados_face.pack(pady=10)

        self.btn_cadastrar = tk.Button(self.root, text="Cadastrar", state=tk.DISABLED, bg="green", fg="white", command=self.cadastrar_usuario)
        self.btn_cadastrar.pack(pady=10)

        self.root.bind('<KeyRelease>', self.verificar_campos_preenchidos)

    def verificar_campos_preenchidos(self, event=None):
        if self.nome.get() and self.email.get() and self.senha.get() and self.reconhecimento_face_realizado:
            self.btn_cadastrar.config(state=tk.NORMAL)
        else:
            self.btn_cadastrar.config(state=tk.DISABLED)

    def abrir_reconhecimento_face(self):
        self.label_dados_face.config(text="Reconhecendo rosto...")  # Mantém a mensagem

        # Desabilita o botão enquanto reconhece o rosto
        self.btn_face.config(state=tk.DISABLED)

        # Verifique o caminho correto do Python no ambiente virtual
        python_path = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")

        # Executar o script de reconhecimento facial usando o Python do venv
        subprocess.Popen([python_path, "reconhecimento_facial.py"])

        # Aguarda um tempo para o reconhecimento
        self.root.after(5000, self.carregar_dados_face)

    def carregar_dados_face(self):
        # Carrega os dados biométricos do arquivo
        if os.path.exists('dados_face.pkl'):
            with open('dados_face.pkl', 'rb') as f:
                self.dados_face = pickle.load(f)  # Carrega a codificação do rosto
            self.reconhecimento_face_realizado = True
            print(f"Dados Biométricos: {self.dados_face}")  # Exibe apenas no log
            self.verificar_campos_preenchidos()
            self.label_dados_face.config(text="Rosto reconhecido com sucesso!")  # Atualiza mensagem
        else:
            messagebox.showerror("Erro", "Dados biométricos não encontrados.")
            self.label_dados_face.config(text="Erro no reconhecimento.")  # Atualiza mensagem de erro
            self.btn_face.config(state=tk.NORMAL)  # Reabilita o botão

    def cadastrar_usuario(self):
        nome = self.nome.get()
        email = self.email.get()
        senha = self.senha.get()

        print(f"Usuário: {nome}, Email: {email}, Senha: {senha}, Dados Face: {self.dados_face}")  # Exibe no log

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

root = tk.Tk()
app = CadastroUsuario(root)
root.mainloop()
