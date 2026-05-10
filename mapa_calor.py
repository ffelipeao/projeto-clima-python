import requests
import pandas as pd
import folium

from folium.plugins import HeatMap


# Lista de cidades
cidades = [
    {"cidade": "Rio de Janeiro", "lat": -22.90, "lon": -43.17},
    {"cidade": "São Paulo", "lat": -23.55, "lon": -46.63},
    {"cidade": "Brasília", "lat": -15.79, "lon": -47.88},
    {"cidade": "Salvador", "lat": -12.97, "lon": -38.50},
    {"cidade": "Manaus", "lat": -3.10, "lon": -60.02},
    {"cidade": "Curitiba", "lat": -25.42, "lon": -49.27},
    {"cidade": "Recife", "lat": -8.05, "lon": -34.88},
]


dados = []


# Consulta API para cada cidade
for item in cidades:

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={item['lat']}"
        f"&longitude={item['lon']}"
        "&current=temperature_2m"
    )

    resposta = requests.get(url)

    if resposta.status_code == 200:

        json_dados = resposta.json()

        temperatura = json_dados["current"]["temperature_2m"]

        dados.append({
            "cidade": item["cidade"],
            "latitude": item["lat"],
            "longitude": item["lon"],
            "temperatura": temperatura
        })


# Criar DataFrame
df = pd.DataFrame(dados)

print(df)


# Criar mapa centralizado no Brasil
mapa = folium.Map(
    location=[-15.00, -55.00],
    zoom_start=4
)


# Dados para o HeatMap
heat_data = []

for _, row in df.iterrows():

    heat_data.append([
        row["latitude"],
        row["longitude"],
        row["temperatura"]
    ])


# Adicionar mapa de calor
HeatMap(heat_data).add_to(mapa)


# Adicionar marcadores
for _, row in df.iterrows():

    folium.Marker(
        [row["latitude"], row["longitude"]],
        popup=f"{row['cidade']} - {row['temperatura']}°C"
    ).add_to(mapa)


# Salvar mapa
mapa.save("output/mapa_calor_temperaturas.html")

print("\nMapa gerado com sucesso!")