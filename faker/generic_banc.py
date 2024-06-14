import sqlite3
from faker import Faker
import random

# Configuração do Faker
fake = Faker()

# Função para criar dados fictícios
def generate_fake_data():
    return (
        None,
        fake.name(),
        random.randint(1, 12),  # Número aleatório de parcelas
        random.choice([True, False]),  # Valor aleatório para Check (True/False)
        random.uniform(100, 1000),  # Valor aleatório para A Pagar
        random.uniform(0, 100),  # Valor aleatório para Entrada
        random.uniform(0, 50),  # Valor aleatório para Desconto
        0,  # Valor inicial para Total (será calculado posteriormente)
        random.choice(['Pago', 'Pendente', 'Cancelado'])  # Status aleatório
    )

# Conectar ao banco de dados SQLite (ou criar se não existir)
conn = sqlite3.connect('seu_banco.db')
cursor = conn.cursor()

# Criar tabela
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transacoes (
        Id INTEGER PRIMARY KEY,
        Nome TEXT,
        Parcelas INTEGER,
        Check BOOLEAN,
        A_Pagar REAL,
        Entrada REAL,
        Desconto REAL,
        Total REAL,
        Status TEXT
    )
''')

# Inserir dados fictícios
num_rows = 10  # Número desejado de linhas
fake_data = [generate_fake_data() for _ in range(num_rows)]

# Inserir dados na tabela
cursor.executemany('''
    INSERT INTO transacoes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', fake_data)

# Calcular o valor total (Total) com base nos outros valores
cursor.execute('''
    UPDATE transacoes
    SET Total = A_Pagar - Entrada - Desconto
''')

# Commit e fechar a conexão
conn.commit()
conn.close()

print(f'{num_rows} linhas foram inseridas no banco de dados.')
