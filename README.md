# 📊 Pipeline de Dados com IoT e Docker

Este projeto tem como objetivo a construção de um pipeline de dados para IoT, utilizando Docker, PostgreSQL e Python (Streamlit e Pandas). O sistema coleta, armazena e exibe leituras de temperatura enviadas por dispositivos IoT.

## 🚀 Tecnologias Utilizadas

Docker para orquestração e execução do PostgreSQL

PostgreSQL como banco de dados relacional

Python 3.10+ para desenvolvimento do pipeline

Streamlit para visualização dos dados

Pandas para manipulação de dados

## 🐳 Configuração do Docker com PostgreSQL

Baixe a imagem oficial do PostgreSQL:

docker pull postgres:latest


Crie e rode o container:

docker run --name postgres-iot -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=iot_db -p 5432:5432 -d postgres


Confirme se o container está ativo:

docker ps

## 🗄️ Estrutura da Tabela

A tabela principal utilizada é temperature_logs:

CREATE TABLE temperature_logs (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50),
    temp NUMERIC,
    noted_date TIMESTAMP
);

## 📥 Populando o Banco com CSV

Os dados de leitura de sensores IoT estão disponíveis em CSV. Para popular o banco, utilize o script inserir_dados.py.

Estrutura esperada do CSV:

device_id → Identificação do dispositivo

temp → Temperatura registrada

noted_date → Data/hora da leitura

Executando a carga de dados:

Certifique-se de que o arquivo CSV está na pasta do projeto.

Rode o script:

python inserir_dados.py


O script conecta ao PostgreSQL e insere os dados automaticamente na tabela temperature_logs.

## 🔍 Views SQL Utilizadas

O projeto utiliza as seguintes views no PostgreSQL para facilitar as análises:
```
-- Média de temperatura por dispositivo
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT device_id, AVG(temp) AS avg_temp
FROM temperature_logs
GROUP BY device_id;

-- Leituras por hora
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT EXTRACT(HOUR FROM noted_date)::int AS hora,
       COUNT(*) AS contagem
FROM temperature_logs
GROUP BY EXTRACT(HOUR FROM noted_date)
ORDER BY hora;

-- Temperaturas máximas e mínimas por dia
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT DATE(noted_date) AS data,
       MAX(temp) AS temp_max,
       MIN(temp) AS temp_min
FROM temperature_logs
GROUP BY DATE(noted_date)
ORDER BY data;
```

## 📊 Visualização dos Dados

Execute o main.py com Streamlit para acessar os gráficos e relatórios:

streamlit run main.py


No dashboard, é possível visualizar:

Temperatura média por dispositivo

Quantidade de leituras por hora

Temperaturas máxima e mínima por dia

## 📂 Estrutura do Projeto
```
Pipeline_IoT_Docker/
│── data/
│   └── IOT-temp.csv          # Arquivo de dados IoT (CSV)
│
│── docker/
│   └── docker-compose.yml    # Configuração do Docker com PostgreSQL
│
│── docs/                     # Prints do funcionamento do projeto
│
│── src/
│   └── main.py               # Dashboard com Streamlit
│
│── inserir_dados.py          # Script para inserir CSV no banco
│── .env                      # Variáveis de ambiente (credenciais do PostgreSQL)
│── requirements.txt          # Dependências do projeto
│── README.md                 # Documentação
```