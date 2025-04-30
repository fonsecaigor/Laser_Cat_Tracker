import streamlit as st
from streamlit_autorefresh import st_autorefresh
import psycopg2
import pandas as pd
import math
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Atualiza automaticamente a cada 2 segundos
st_autorefresh(interval=2000, limit=None, key="refresh")

# Carrega variáveis do .env
load_dotenv()

# Função para calcular ângulo
def calcular_angulo(x, y):
    angulo = math.degrees(math.atan2(y, x))
    return angulo if angulo >= 0 else angulo + 360

# Conexão com o banco
def conectar():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# Título do app
st.title("📡 Dashboard em Tempo Real - Laser Tracker")
st.caption("Atualiza automaticamente a cada 2 segundos.")

# Botão para apagar todos os dados e resetar o contador de ID
if st.button("🗑️ Apagar todos os movimentos e reiniciar ID"):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("TRUNCATE movimentos_laser RESTART IDENTITY")
        conn.commit()
        cur.close()
        conn.close()
        st.success("Todos os movimentos foram apagados e o contador de ID foi reiniciado.")
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Erro ao apagar e reiniciar: {e}")
        st.stop()

# Consulta os dados (sem movimento_num)
try:
    conn = conectar()
    df = pd.read_sql("SELECT x_pos, y_pos FROM movimentos_laser ORDER BY id ASC", conn)
    conn.close()
except Exception as e:
    st.error(f"Erro ao conectar ao banco: {e}")
    st.stop()

# Calcula o ângulo
df["angulo"] = df.apply(lambda row: calcular_angulo(row["x_pos"], row["y_pos"]), axis=1)

# Exibe os últimos 10 movimentos (sem IDs)
st.subheader("📋 Últimos Movimentos")
st.dataframe(df[["x_pos", "y_pos", "angulo"]].tail(10), use_container_width=True)

# Gráfico de ângulo (usando índice como eixo X)
st.subheader("📈 Evolução dos Ângulos")
st.line_chart(df[["angulo"]])

# Gráfico de trajetória em 2D
st.subheader("🧭 Trajetória do Movimento (Simulação em uma folha)")

fig, ax = plt.subplots()
ax.plot(df["x_pos"], df["y_pos"], marker='o', linestyle='-', color='blue')
ax.set_xlabel("Posição X")
ax.set_ylabel("Posição Y")
ax.set_title("Trajetória do Laser")
ax.grid(True)
ax.set_aspect('equal', adjustable='box')
st.pyplot(fig)
