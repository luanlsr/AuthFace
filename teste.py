import pyodbc

def listar_bancos_localdb():
    try:
        # Conectar ao LocalDB sem especificar um banco de dados
        conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};Server=(localdb)\\MSSQLLocalDB;Integrated Security=True;TrustServerCertificate=yes;')
        cursor = conn.cursor()

        # Consulta para listar todos os bancos de dados na instância
        cursor.execute("SELECT name FROM sys.databases WHERE owner_sid != 0x01")  # Exclui o banco de dados 'master'
        bancos = cursor.fetchall()

        print("Bancos de dados disponíveis na instância LocalDB:")
        for banco in bancos:
            print(banco[0])

        conn.close()

    except pyodbc.Error as e:
        print(f"Erro ao conectar ao LocalDB ou listar bancos: {e}")


# Executar a função
listar_bancos_localdb()
