import serial
import psycopg2
import time
import re
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
SERIAL_PORT = os.getenv("SERIAL_PORT")

# Conexão com Arduino
arduino = serial.Serial(port=SERIAL_PORT, baudrate=9600, timeout=1)

# Função para verificar e criar o banco de dados se não existir
def create_database_if_not_exists():
    # Conecta ao banco de dados padrão 'postgres'
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Verifica se o banco já existe
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone()

    if not exists:
        print(f"Banco de dados '{DB_NAME}' não encontrado. Criando...")
        cur.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"Banco de dados '{DB_NAME}' criado com sucesso.")
    else:
        print(f"Banco de dados '{DB_NAME}' já existe.")

    cur.close()
    conn.close()

# Função para criar tabela se não existir
def create_table_if_not_exists(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS movimentos_laser (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            movimento_num INTEGER,
            x_pos INTEGER,
            y_pos INTEGER
        )
    ''')

# Função para interpretar linha do Arduino
def parse_data(line):
    match = re.match(r'X:(\d+),Y:(\d+)', line)
    if match:
        x = int(match.group(1))
        y = int(match.group(2))
        return x, y
    return None

# ----------- INÍCIO DO PROGRAMA --------------

# Primeiro garante que o banco existe
create_database_if_not_exists()

# Agora conecta no banco de dados correto
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Cria a tabela se ainda não existir
create_table_if_not_exists(cur)
conn.commit()

# Controle dos movimentos
movimento_counter = 0
ultimo_x = None
ultimo_y = None

try:
    print("Iniciando captura de dados...")
    while True:
        if arduino.in_waiting:
            line = arduino.readline().decode('utf-8').strip()

            if line == "END" and ultimo_x is not None and ultimo_y is not None:
                movimento_counter += 1

                # Insere no banco
                cur.execute('''
                    INSERT INTO movimentos_laser (movimento_num, x_pos, y_pos)
                    VALUES (%s, %s, %s)
                ''', (movimento_counter, ultimo_x, ultimo_y))
                conn.commit()
                # Exibe todos os movimentos salvos
                cur.execute('SELECT movimento_num, x_pos, y_pos FROM movimentos_laser ORDER BY movimento_num ASC')
                movimentos = cur.fetchall()
                print("\n--- Movimentos salvos no banco ---")
                for movimento in movimentos:
                    print(f"Movimento {movimento[0]} -> X={movimento[1]}, Y={movimento[2]}")
                print("----------------------------------\n")

                # Reseta variáveis
                ultimo_x = None
                ultimo_y = None

            else:
                data = parse_data(line)
                if data:
                    x, y = data
                    ultimo_x = x
                    ultimo_y = y

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Encerrando captura...")

finally:
    cur.close()
    conn.close()
    arduino.close()
