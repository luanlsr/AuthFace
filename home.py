import tkinter as tk
import customtkinter as ctk


class Home:
    def __init__(self, root, nome_usuario, email_usuario):
        self.root = root
        self.root.title("Home")
        self.root.geometry("800x600")
        
        # Definindo modo escuro e tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Define a cor de fundo da janela principal
        self.root.configure(bg="#2E2E2E")  # Adicione esta linha para definir a cor de fundo

        self.nome_usuario = nome_usuario
        self.email_usuario = email_usuario

        self.create_widgets()

    def create_widgets(self):
        # Cria um frame com fundo escuro
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Mensagem de boas-vindas
        title_label = ctk.CTkLabel(frame, text="Bem-vindo(a) à sua Home!", font=("Arial", 24, "bold"), text_color="white")
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Exibe o nome do usuário
        nome_label = ctk.CTkLabel(frame, text=f"Usuário: {self.nome_usuario}", font=("Arial", 18, "bold"), text_color="white")
        nome_label.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        # Exibe o email do usuário
        email_label = ctk.CTkLabel(frame, text=f"Email: {self.email_usuario}", font=("Arial", 18, "bold"), text_color="white")
        email_label.grid(row=2, column=0, columnspan=2, pady=(5, 20))

        # Botão para deslogar
        ctk.CTkButton(frame, text="Deslogar", command=self.deslogar, fg_color="#F44336", text_color="white").grid(row=3, column=0, columnspan=2, pady=15)

    def deslogar(self):
        self.root.destroy()
        from login import Login
        login_root = ctk.CTk()
        Login(login_root)
        login_root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()  # Cria a janela principal
    home = Home(root, "Nome do Usuário", "email@exemplo.com")  # Substitua pelos valores adequados
    root.mainloop()
