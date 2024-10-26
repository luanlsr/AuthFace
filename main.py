import customtkinter as ctk
from login import Login
from connection import criar_banco_dados, criar_conexao_inicial, criar_tabela


def iniciar_sistema():
    conn = criar_conexao_inicial()
    if conn is None:
        print("Erro ao estabelecer conexão inicial. Sistema não iniciado.")
        return

    nome_banco = 'identity_auth_db'
    criar_banco_dados(nome_banco)
    criar_tabela(nome_banco)
    conn.close()
    root = ctk.CTk()
    Login(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_sistema()
