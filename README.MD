# 🐱 Laser Cat Tracker

Projeto que integra **Arduino**, **Python** e **PostgreSQL** para controlar e rastrear os movimentos de um laser para gatos.

Cada movimentação completa do laser é capturada e salva em um banco de dados relacional para posterior análise de comportamento.

---

## 📆 Estrutura do Projeto

```
laser-cat-tracker/
├── README.md
├── requirements.txt
├── src/
│   ├── captura_movimentos.py
│   └── arduino/
│       └── laser_tracker.ino
```

---

## 📚 Descrição do Projeto

1. O **Arduino** movimenta dois servos motores controlando um laser.
2. Cada posição `(X, Y)` é enviada via **Serial** para o computador.
3. O **Python** lê essas posições.
4. Quando o Arduino termina o movimento e envia o comando `END`, o Python:
   - Salva a posição final `(X, Y)` no banco **PostgreSQL**.
   - Registra o movimento no histórico.

---

## ⚙️ Requisitos

- Python 3.8+
- PostgreSQL 13+
- Arduino Nano / Deek-Robot (ou similar)
- Arduino IDE
- Git (opcional, para clonar)

**Dependências Python:**

```txt
pyserial
psycopg2
python-dotenv
```

Instale com:

```bash
pip install -r requirements.txt
```

**Criando e ativando um ambiente virtual (venv):**

1. Criar um ambiente virtual:

```bash
python -m venv venv
```

2. Ativar o ambiente virtual:
- **Windows**:

```bash
venv\Scripts\activate
```

- **Linux/MacOS**:

```bash
source venv/bin/activate
```

3. Instalar as dependências dentro da venv:

```bash
pip install -r requirements.txt
```

---

## 🔢 Variáveis de Ambiente (definidas no script)

Configure suas variáveis de ambiente antes de rodar o script. Exemplo:

```dotenv
DB_NAME=Arduino
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
DB_HOST=localhost
DB_PORT=5432
SERIAL_PORT=COM5
```

**Onde:**

| Variável | Descrição |
|----------|------------|
| `DB_NAME` | Nome do banco de dados PostgreSQL |
| `DB_USER` | Usuário do banco |
| `DB_PASSWORD` | Senha do banco |
| `DB_HOST` | Endereço do servidor (normalmente localhost) |
| `DB_PORT` | Porta do PostgreSQL (padrão 5432) |
| `SERIAL_PORT` | Porta serial do Arduino |

**Importante:**
- As variáveis devem ser carregadas com `dotenv` no script Python.

---

## 📅 Ciclo Completo de Execução

### 1. Programar o Arduino

- Abra a **Arduino IDE**.
- Carregue o arquivo `src/arduino/laser_tracker.ino` para o Arduino.
- Certifique-se que a porta Serial está correta (ex: COM5).

### 2. Rodar o script Python

- Ative seu ambiente virtual (se criado):

```bash
# Windows
venv\Scripts\activate

# Linux/MacOS
source venv/bin/activate
```

- Execute o script:

```bash
python src/captura_movimentos.py
```

O script irá:

- Verificar se o banco de dados existe (e criar se não existir).
- Criar a tabela `movimentos_laser` se não existir.
- Capturar dados `(X, Y)` do Arduino.
- Salvar o último `(X, Y)` de cada movimento completo após `END`.

### 3. Visualizar os dados

Cada movimento será mostrado no terminal, e salvo no PostgreSQL.


---

## 💾 Estrutura da Tabela no PostgreSQL

Tabela `movimentos_laser`:

| Campo         | Tipo         | Descrição |
|---------------|--------------|-----------|
| `id`          | SERIAL        | ID único |
| `timestamp`   | TIMESTAMP     | Data/hora da gravação |
| `movimento_num` | INTEGER     | Número sequencial do movimento |
| `x_pos`       | INTEGER       | Posição X no final do movimento |
| `y_pos`       | INTEGER       | Posição Y no final do movimento |

---

## 👥 Sobre

Este projeto foi desenvolvido para demonstrar a integração entre dispositivos físicos (Arduino) e bancos de dados relacionais (PostgreSQL) usando Python como ponte.

Ideal para projetos de IoT, automação e estudo de comunicação Serial!


---

## 💡 Comandos Rápidos

```bash
# Clonar o repositório
git clone https://github.com/SamuelLucasVieira/laser-cat-tracker.git
cd laser-cat-tracker

# Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/MacOS

# Instalar dependências
pip install -r requirements.txt

# Executar\python src/captura_movimentos.py
```