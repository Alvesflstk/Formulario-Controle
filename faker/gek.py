import sqlite3
from faker import Faker

def banco_original():
    fake = Faker()

    # Conectar ao banco de dados (um novo arquivo será criado se não existir)
    conexao = sqlite3.connect('dados.db')
    cursor = conexao.cursor()

    # Criar uma tabela
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS metadados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Descricao TEXT,
        Cliente TEXT,
        Quantidade INTEGER,
        Data TEXT,
        Forma_pg TEXT,
        Q_Parcelas INTEGER,
        Valor_parcelas REAL,
        Desconto REAL,
        Entrada REAL,
        Total REAL,
        Status TEXT
    )
    ''')

    conexao.commit()
    conexao.close()
banco_original