import requests
import pandas as pd
import folium
from folium.plugins import HeatMap


# ------------------------------------------------------
# 1. Lista de cidades com nome, latitude e longitude
# ------------------------------------------------------

cidades = [
    {"cidade": "Rio de Janeiro", "lat": -22.90, "lon": -43.17},
    {"cidade": "São Paulo", "lat": -23.55, "lon": -46.63},
    {"cidade": "Brasília", "lat": -15.79, "lon": -47.88},
    {"cidade": "Salvador", "lat": -12.97, "lon": -38.50},
    {"cidade": "Manaus", "lat": -3.10, "lon": -60.02},
    {"cidade": "Curitiba", "lat": -25.42, "lon": -49.27},
    {"cidade": "Recife", "lat": -8.05, "lon": -34.88},
    {"cidade": "Bangu", "lat": -22.87, "lon": -43.46},
]


# ------------------------------------------------------
# 2. Definir o ano da análise
# ------------------------------------------------------

ano = 2025

data_inicio = f"{ano}-01-01"
data_fim = f"{ano}-12-31"


# ------------------------------------------------------
# 3. Lista para armazenar os resultados
# ------------------------------------------------------

resultados = []


# ------------------------------------------------------
# 4. Percorrer cada cidade e consultar a API histórica
# ------------------------------------------------------

for item in cidades:

    cidade = item["cidade"]
    latitude = item["lat"]
    longitude = item["lon"]

    print(f"Consultando dados de {cidade}...")

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&start_date={data_inicio}"
        f"&end_date={data_fim}"
        "&daily=temperature_2m_mean"
        "&timezone=America/Sao_Paulo"
    )

    resposta = requests.get(url)

    if resposta.status_code != 200:
        print(f"Erro ao consultar {cidade}")
        continue

    dados_json = resposta.json()


    # ------------------------------------------------------
    # 5. Transformar o JSON em DataFrame
    # ------------------------------------------------------

    df = pd.DataFrame({
        "data": dados_json["daily"]["time"],
        "temperatura_media_diaria": dados_json["daily"]["temperature_2m_mean"]
    })

    df["data"] = pd.to_datetime(df["data"])


    # ------------------------------------------------------
    # 6. Calcular a temperatura média anual
    # ------------------------------------------------------

    temperatura_media_anual = df["temperatura_media_diaria"].mean()


    # ------------------------------------------------------
    # 7. Guardar o resultado da cidade
    # ------------------------------------------------------

    resultados.append({
        "cidade": cidade,
        "latitude": latitude,
        "longitude": longitude,
        "temperatura_media_anual": temperatura_media_anual
    })


# ------------------------------------------------------
# 8. Criar DataFrame final com todas as cidades
# ------------------------------------------------------

df_resultado = pd.DataFrame(resultados)

print("\nTemperatura média anual por cidade:")
print(df_resultado)


# ------------------------------------------------------
# 9. Salvar resultado em CSV
# ------------------------------------------------------

df_resultado.to_csv("output/temperatura_media_anual_cidades.csv", index=False)


# ------------------------------------------------------
# 10. Criar mapa centralizado no Brasil
# ------------------------------------------------------

mapa = folium.Map(
    location=[-15.0, -55.0],
    zoom_start=4
)


# ------------------------------------------------------
# 11. Preparar dados para o mapa de calor
# Formato esperado:
# [latitude, longitude, intensidade]
# ------------------------------------------------------

heat_data = []

for _, linha in df_resultado.iterrows():
    heat_data.append([
        linha["latitude"],
        linha["longitude"],
        linha["temperatura_media_anual"]
    ])


# ------------------------------------------------------
# 12. Adicionar camada de mapa de calor
# ------------------------------------------------------

HeatMap(
    heat_data,
    radius=35,
    blur=25,
    max_zoom=6
).add_to(mapa)


# ------------------------------------------------------
# 13. Adicionar marcadores com nome e temperatura
# ------------------------------------------------------

for _, linha in df_resultado.iterrows():

    texto_popup = (
        f"<b>{linha['cidade']}</b><br>"
        f"Temperatura média anual: "
        f"{linha['temperatura_media_anual']:.2f} °C"
    )

    folium.Marker(
        location=[linha["latitude"], linha["longitude"]],
        popup=texto_popup,
        tooltip=linha["cidade"]
    ).add_to(mapa)


# ------------------------------------------------------
# 14. Salvar o mapa em HTML
# ------------------------------------------------------

mapa.save("output/mapa_calor_temperatura_media_anual.html")

print("\nMapa de calor gerado com sucesso!")
print("Arquivo criado: mapa_calor_temperatura_media_anual.html")