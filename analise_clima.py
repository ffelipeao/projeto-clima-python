import requests
import pandas as pd
import matplotlib.pyplot as plt


# 1. URL da API Open-Meteo
# Exemplo: dados climáticos do Rio de Janeiro
url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=-22.9068"
    "&longitude=-43.1729"
    "&hourly=temperature_2m,relative_humidity_2m,precipitation"
    "&forecast_days=7"
)


# 2. Requisição com requests
resposta = requests.get(url)

if resposta.status_code == 200:
    print("Dados acessados com sucesso!")
else:
    print("Erro ao acessar a API:", resposta.status_code)
    exit()


# 3. Converter resposta para JSON
dados_json = resposta.json()

print("\nChaves principais do JSON:")
print(dados_json.keys())


# 4. Converter os dados horários para DataFrame
dados_horarios = dados_json["hourly"]

df = pd.DataFrame(dados_horarios)

print("\nPrimeiras linhas do DataFrame:")
print(df.head())


# 5. Ajustar coluna de data/hora
df["time"] = pd.to_datetime(df["time"])


# 6. Criar uma coluna com a data
df["data"] = df["time"].dt.date


# 7. Resumo estatístico
print("\nResumo estatístico:")
print(df.describe())


# 8. Agrupar por dia
df_diario = df.groupby("data").agg({
    "temperature_2m": "mean",
    "relative_humidity_2m": "mean",
    "precipitation": "sum"
}).reset_index()

print("\nDados agrupados por dia:")
print(df_diario)


# 9. Gráfico de barras - temperatura média por dia
plt.figure(figsize=(10, 5))
plt.bar(df_diario["data"].astype(str), df_diario["temperature_2m"])
plt.title("Temperatura média por dia - Rio de Janeiro")
plt.xlabel("Data")
plt.ylabel("Temperatura média (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/grafico_barras_temperatura.png")
plt.show()


# 10. Gráfico de pizza - participação da chuva por dia
plt.figure(figsize=(7, 7))
plt.pie(
    df_diario["precipitation"],
    labels=df_diario["data"].astype(str),
    autopct="%1.1f%%"
)
plt.title("Distribuição da precipitação por dia")
plt.tight_layout()
plt.savefig("output/grafico_pizza_chuva.png")
plt.show()


# 11. Gráfico de dispersão - temperatura x umidade
plt.figure(figsize=(8, 5))
plt.scatter(df["temperature_2m"], df["relative_humidity_2m"])
plt.title("Relação entre temperatura e umidade")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Umidade relativa (%)")
plt.tight_layout()
plt.savefig("output/grafico_dispersao_temperatura_umidade.png")
plt.show()