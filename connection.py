import pyodbc


def criar_conexao_inicial():
    try:
        # Usando ODBC Driver 18 explicitamente e especificando o banco identity_auth_db
        conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                              'Server=(localdb)\\MSSQLLocalDB;'
                              'Integrated Security=True;'
                              'TrustServerCertificate=yes;')
        print("Conexão ao SQL Server estabelecida com sucesso.")
        return conn
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao SQL Server: {e}")
        return None


def criar_conexao_com_banco():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'Server=(localdb)\\MSSQLLocalDB;'
            'Database=identity_auth_db;'
            'Integrated Security=True;'
            'TrustServerCertificate=yes;'
        )
        print("Conexão ao banco de dados 'identity_auth_db' estabelecida com sucesso.")
        return conn
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def criar_banco_dados(nome_banco):
    conn = criar_conexao_inicial()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        # Desabilitar transações explícitas para o comando CREATE DATABASE
        conn.autocommit = True
        cursor.execute(f'IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = \'{nome_banco}\') CREATE DATABASE {nome_banco}')
        print(f"Banco de dados '{nome_banco}' criado ou já existe.")
    except pyodbc.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        conn.close()


def criar_tabela(nome_banco):
    conn = None
    try:
        # Conectar diretamente ao banco recém-criado
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};'
                              f'Server=(localdb)\\MSSQLLocalDB;'
                              f'Database={nome_banco};'  # Certifique-se de especificar o banco correto
                              'Integrated Security=True;'
                              'TrustServerCertificate=yes;')
        cursor = conn.cursor()

        # Criar tabela de usuários se ela não existir
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[usuarios]') AND type in (N'U'))
            CREATE TABLE usuarios (
                id INT PRIMARY KEY IDENTITY(1,1),
                nome NVARCHAR(100) NOT NULL,
                email NVARCHAR(100) NOT NULL UNIQUE,
                senha NVARCHAR(100) NOT NULL,
                dados_face VARBINARY(MAX)
            )
        ''')
        conn.commit()
        print("Tabela 'usuarios' criada ou já existe.")
    except pyodbc.Error as e:
        print(f"Erro ao criar a tabela: {e}")
    finally:
        if conn:
            conn.close()
            

# Criar o banco de dados e a tabela
nome_banco = 'identity_auth_db'   
criar_banco_dados(nome_banco)
criar_tabela(nome_banco)
