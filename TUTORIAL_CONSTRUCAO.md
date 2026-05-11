# Tutorial: construindo o projeto manualmente

Este guia reconstrói o projeto **passo a passo**, no mesmo espírito do repositório: consumir a API [Open-Meteo](https://open-meteo.com/), organizar dados com **Pandas**, visualizar com **Matplotlib** e, nos scripts de mapa, gerar HTML interativo com **Folium**.

Em cada seção, a **explicação vem antes** do código correspondente.

---

## 0. O que você vai montar

| Artefato | Função |
|----------|--------|
| `requirements.txt` | Lista bibliotecas e versões para `pip install`. |
| Pasta `output/` | Destino de gráficos PNG, CSV e mapas HTML (evita poluir a raiz). |
| `analise_clima.py` | Previsão horária (7 dias), agregação diária e três gráficos. |
| `mapa_calor.py` | Temperatura atual em várias cidades + mapa de calor no Brasil. |
| `mapa_calor_temperatura_anual.py` | Média anual via API de arquivo + CSV + mapa de calor. |

Opcional: um `.gitignore` simples (venv, `.env`, `__pycache__`, etc.) para não versionar lixo local.

---

## 1. Ambiente Python e pasta do projeto

**Passo 1.1 — Criar a pasta do projeto**  
Crie uma pasta (por exemplo `projeto-clima-python`) e abra nela o terminal.

**Passo 1.2 — (Recomendado) ambiente virtual**  
Isola as bibliotecas do restante do sistema.

```bash
python3 -m venv venv
source venv/bin/activate
```

No Windows (PowerShell): `venv\Scripts\Activate.ps1`.

**Passo 1.3 — Pasta de saída**  
Os scripts salvam arquivos em `output/`. Crie a pasta uma vez:

```bash
mkdir -p output
```

---

## 2. Arquivo de dependências

**Passo 2.1 — Por que `requirements.txt`?**  
Documenta exatamente o que instalar com `pip install -r requirements.txt`, garantindo que **requests**, **pandas**, **matplotlib** e **folium** (e dependências transitivas como **numpy**, **Jinja2**) fiquem disponíveis.

**Passo 2.2 — Conteúdo do arquivo**  
Salve na raiz do projeto como `requirements.txt`:

```text
branca==0.8.2
certifi==2026.4.22
charset-normalizer==3.4.7
contourpy==1.3.3
cycler==0.12.1
folium==0.20.0
fonttools==4.62.1
idna==3.14
Jinja2==3.1.6
kiwisolver==1.5.0
MarkupSafe==3.0.3
matplotlib==3.10.9
numpy==2.4.4
packaging==26.2
pandas==3.0.2
pillow==12.2.0
pyparsing==3.3.2
python-dateutil==2.9.0.post0
requests==2.33.1
six==1.17.0
urllib3==2.7.0
xyzservices==2026.3.0
```

**Passo 2.3 — Instalar**  

```bash
pip install -r requirements.txt
```

---

## 3. Script `analise_clima.py`

Fluxo geral: montar a URL da API de **previsão** → `GET` com **requests** → validar status → ler JSON → montar **DataFrame** com Pandas → tratar datas → estatísticas e agregação diária → três figuras com **Matplotlib** salvas em `output/`.

### 3.1 Imports e URL da API

**Explicação**  
- `requests`: HTTP.  
- `pandas`: tabelas e agregações.  
- `matplotlib.pyplot`: gráficos.  
A URL aponta para o endpoint `v1/forecast` da Open-Meteo, com latitude/longitude do Rio de Janeiro, variáveis horárias (`temperature_2m`, `relative_humidity_2m`, `precipitation`) e `forecast_days=7`.

```python
import requests
import pandas as pd
import matplotlib.pyplot as plt


url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=-22.9068"
    "&longitude=-43.1729"
    "&hourly=temperature_2m,relative_humidity_2m,precipitation"
    "&forecast_days=7"
)
```

### 3.2 Requisição e checagem de erro

**Explicação**  
Só seguimos se `status_code == 200`; caso contrário, avisamos e encerramos o script para não processar corpo inválido.

```python
resposta = requests.get(url)

if resposta.status_code == 200:
    print("Dados acessados com sucesso!")
else:
    print("Erro ao acessar a API:", resposta.status_code)
    exit()
```

### 3.3 JSON e inspeção das chaves

**Explicação**  
`.json()` transforma o corpo da resposta em dicionário Python. Imprimir `keys()` ajuda em aula a ver a estrutura típica (`hourly`, `daily`, etc.).

```python
dados_json = resposta.json()

print("\nChaves principais do JSON:")
print(dados_json.keys())
```

### 3.4 DataFrame a partir da série horária

**Explicação**  
Em previsões Open-Meteo, os arrays paralelos (`time`, `temperature_2m`, …) vêm dentro de `dados_json["hourly"]`. `pd.DataFrame` alinha automaticamente por nome de chave.

```python
dados_horarios = dados_json["hourly"]

df = pd.DataFrame(dados_horarios)

print("\nPrimeiras linhas do DataFrame:")
print(df.head())
```

### 3.5 Coluna de tempo e coluna só com a data

**Explicação**  
`time` vira `datetime64`; extrair `.dt.date` permite agrupar por dia civil.

```python
df["time"] = pd.to_datetime(df["time"])
df["data"] = df["time"].dt.date
```

### 3.6 Resumo estatístico

**Explicação**  
`describe()` mostra contagem, média, desvio, quartis e extremos das colunas numéricas.

```python
print("\nResumo estatístico:")
print(df.describe())
```

### 3.7 Agregação diária

**Explicação**  
`groupby("data")` + `agg`: média de temperatura e umidade, soma da precipitação (chuva acumulada no dia).

```python
df_diario = df.groupby("data").agg({
    "temperature_2m": "mean",
    "relative_humidity_2m": "mean",
    "precipitation": "sum"
}).reset_index()

print("\nDados agrupados por dia:")
print(df_diario)
```

### 3.8 Gráfico de barras (temperatura média por dia)

**Explicação**  
Datas no eixo X como string para o matplotlib rotular sem surpresas; `tight_layout()` e `savefig` para arquivo; `show()` abre a janela interativa se o ambiente permitir.

```python
plt.figure(figsize=(10, 5))
plt.bar(df_diario["data"].astype(str), df_diario["temperature_2m"])
plt.title("Temperatura média por dia - Rio de Janeiro")
plt.xlabel("Data")
plt.ylabel("Temperatura média (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/grafico_barras_temperatura.png")
plt.show()
```

### 3.9 Gráfico de pizza (participação da chuva por dia)

**Explicação**  
Cada fatia é a precipitação total daquele dia; `autopct` mostra percentual no gráfico.

```python
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
```

### 3.10 Gráfico de dispersão (temperatura × umidade)

**Explicação**  
Usa os dados **horários** (`df`), não o diário, para mais pontos e ver correlação visual.

```python
plt.figure(figsize=(8, 5))
plt.scatter(df["temperature_2m"], df["relative_humidity_2m"])
plt.title("Relação entre temperatura e umidade")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Umidade relativa (%)")
plt.tight_layout()
plt.savefig("output/grafico_dispersao_temperatura_umidade.png")
plt.show()
```

**Passo final desta parte**  
Junte todos os blocos na ordem acima em um único arquivo `analise_clima.py`.

---

## 4. Script `mapa_calor.py`

Fluxo: lista fixa de cidades com coordenadas → para cada uma, chamar a API de **previsão** pedindo só `current=temperature_2m` → montar lista de dicts → `DataFrame` → mapa Folium centrado no Brasil → camada **HeatMap** (peso normalizado entre mínimo e máximo do conjunto) → círculos invisíveis com **tooltip** + **DivIcon** com o valor em °C → salvar HTML.

### 4.1 Imports, lista de cidades e acumulador

**Explicação**  
`HeatMap` do pacote `folium.plugins` espera lista de `[lat, lon, peso]` (peso opcional mas aqui usamos para intensidade relativa).

```python
import requests
import pandas as pd
import folium

from folium.plugins import HeatMap


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
```

### 4.2 Loop: requisição por cidade e extração da temperatura atual

**Explicação**  
A URL é montada com f-strings a partir de `lat`/`lon`. Em sucesso, lê-se `json_dados["current"]["temperature_2m"]`.

```python
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
```

### 4.3 DataFrame e mapa base

**Explicação**  
`folium.Map(location=..., zoom_start=4)` centraliza aproximadamente o Brasil para ver todas as cidades.

```python
df = pd.DataFrame(dados)

print(df)

mapa = folium.Map(
    location=[-15.00, -55.00],
    zoom_start=4
)
```

### 4.4 Normalização dos pesos para o HeatMap

**Explicação**  
Temperaturas absolutas (ex.: 22 °C vs 28 °C) gerariam intensidades parecidas no plugin. Por isso normalizamos entre `t_min` e `t_max` do **conjunto** e mapeamos para um peso entre ~0,18 e 1,0; se todas forem iguais, peso fixo 1,0.

```python
t_min = df["temperatura"].min()
t_max = df["temperatura"].max()
faixa = t_max - t_min

heat_data = []

for _, row in df.iterrows():

    if faixa > 0:
        rel = (row["temperatura"] - t_min) / faixa
        peso = 0.18 + 0.82 * rel
    else:
        peso = 1.0

    heat_data.append([
        row["latitude"],
        row["longitude"],
        peso
    ])
```

### 4.5 HeatMap e camadas de rótulo / tooltip

**Explicação**  
- `HeatMap(...).add_to(mapa)` adiciona a camada de calor.  
- `CircleMarker` quase transparente captura hover para tooltip com nome e temperatura.  
- `Marker` + `DivIcon` desenha o texto em °C sem ser o pin padrão (HTML/CSS inline).

```python
HeatMap(
    heat_data,
    radius=30,
    blur=18,
    min_opacity=0.35,
).add_to(mapa)

for _, row in df.iterrows():

    lat, lon = row["latitude"], row["longitude"]
    cidade = row["cidade"]
    temp = row["temperatura"]
    temp_txt = f"{temp:g}°C"

    folium.CircleMarker(
        location=[lat, lon],
        radius=58,
        stroke=False,
        fill=True,
        fill_color="#ffffff",
        fill_opacity=0.012,
        tooltip=folium.Tooltip(
            f"<b>{cidade}</b><br>{temp_txt}",
            sticky=True,
        ),
    ).add_to(mapa)

    folium.Marker(
        location=[lat, lon],
        icon=folium.DivIcon(
            icon_size=(80, 22),
            icon_anchor=(40, 11),
            html=(
                "<div style=\""
                "font-size:13px;font-weight:700;color:#fff;"
                "text-align:center;line-height:22px;width:80px;"
                "text-shadow:0 0 4px #000,0 0 10px #000;"
                "pointer-events:none;\">"
                f"{temp_txt}</div>"
            ),
        ),
    ).add_to(mapa)
```

### 4.6 Salvar o HTML

**Explicação**  
`mapa.save(...)` grava um arquivo autossuficiente que você abre no navegador.

```python
mapa.save("output/mapa_calor_temperaturas.html")

print("\nMapa gerado com sucesso!")
```

---

## 5. Script `mapa_calor_temperatura_anual.py`

Diferenças principais em relação ao `mapa_calor.py`:

- Usa o endpoint de **arquivo histórico** `https://archive-api.open-meteo.com/v1/archive` com `start_date`, `end_date` e `daily=temperature_2m_mean`.
- Define um **ano** (no projeto, `2025`) e calcula a **média anual** por cidade a partir das médias diárias.
- Exporta `output/temperatura_media_anual_cidades.csv`.
- Gera `output/mapa_calor_temperatura_media_anual.html` com a mesma lógica visual (HeatMap + tooltips + rótulos), mas com valores anuais e formatação `f"{temp:.1f}°C"`.

### 5.1 Imports e cidades (inclui Bangu)

**Explicação**  
Mesma ideia da lista anterior, com uma cidade extra para o exemplo em sala.

```python
import requests
import pandas as pd
import folium
from folium.plugins import HeatMap


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
```

### 5.2 Ano, intervalo de datas e lista de resultados

**Explicação**  
`data_inicio` / `data_fim` no formato `YYYY-MM-DD` exigido pela API. `timezone=America/Sao_Paulo` alinha “dias” ao fuso brasileiro.

```python
ano = 2025

data_inicio = f"{ano}-01-01"
data_fim = f"{ano}-12-31"

resultados = []
```

### 5.3 Loop: archive API, DataFrame diário, média anual

**Explicação**  
Se `status_code != 200`, imprime erro e `continue` para a próxima cidade. Caso contrário, monta `DataFrame` com `time` e `temperature_2m_mean`, converte datas e faz `.mean()` na coluna de temperatura.

```python
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

    df = pd.DataFrame({
        "data": dados_json["daily"]["time"],
        "temperatura_media_diaria": dados_json["daily"]["temperature_2m_mean"]
    })

    df["data"] = pd.to_datetime(df["data"])

    temperatura_media_anual = df["temperatura_media_diaria"].mean()

    resultados.append({
        "cidade": cidade,
        "latitude": latitude,
        "longitude": longitude,
        "temperatura_media_anual": temperatura_media_anual
    })
```

### 5.4 DataFrame final, CSV e mapa base

**Explicação**  
`to_csv(..., index=False)` evita coluna extra de índice. O mapa Folium replica o do script anterior (mesmo centro e zoom).

```python
df_resultado = pd.DataFrame(resultados)

print("\nTemperatura média anual por cidade:")
print(df_resultado)

df_resultado.to_csv("output/temperatura_media_anual_cidades.csv", index=False)

mapa = folium.Map(
    location=[-15.0, -55.0],
    zoom_start=4
)
```

### 5.5 HeatMap a partir da média anual

**Explicação**  
Mesma normalização min–max sobre `temperatura_media_anual`.

```python
t_min = df_resultado["temperatura_media_anual"].min()
t_max = df_resultado["temperatura_media_anual"].max()
faixa = t_max - t_min

heat_data = []

for _, linha in df_resultado.iterrows():

    temp = linha["temperatura_media_anual"]

    if faixa > 0:
        rel = (temp - t_min) / faixa
        peso = 0.18 + 0.82 * rel
    else:
        peso = 1.0

    heat_data.append([
        linha["latitude"],
        linha["longitude"],
        peso
    ])

HeatMap(
    heat_data,
    radius=30,
    blur=18,
    min_opacity=0.35,
).add_to(mapa)
```

### 5.6 Tooltips, rótulos e salvamento

**Explicação**  
`temp_txt` usa uma casa decimal por ser agregado anual. O arquivo final fica em `output/`.

```python
for _, linha in df_resultado.iterrows():

    lat = linha["latitude"]
    lon = linha["longitude"]
    cidade = linha["cidade"]
    temp = linha["temperatura_media_anual"]
    temp_txt = f"{temp:.1f}°C"

    folium.CircleMarker(
        location=[lat, lon],
        radius=58,
        stroke=False,
        fill=True,
        fill_color="#ffffff",
        fill_opacity=0.012,
        tooltip=folium.Tooltip(
            f"<b>{cidade}</b><br>{temp_txt}",
            sticky=True,
        ),
    ).add_to(mapa)

    folium.Marker(
        location=[lat, lon],
        icon=folium.DivIcon(
            icon_size=(80, 22),
            icon_anchor=(40, 11),
            html=(
                "<div style=\""
                "font-size:13px;font-weight:700;color:#fff;"
                "text-align:center;line-height:22px;width:80px;"
                "text-shadow:0 0 4px #000,0 0 10px #000;"
                "pointer-events:none;\">"
                f"{temp_txt}</div>"
            ),
        ),
    ).add_to(mapa)

mapa.save("output/mapa_calor_temperatura_media_anual.html")

print("\nMapa de calor gerado com sucesso!")
print("Arquivo criado: mapa_calor_temperatura_media_anual.html")
```

**Nota**  
A última mensagem de `print` cita só o nome do arquivo; o caminho real no disco é `output/mapa_calor_temperatura_media_anual.html`.

---

## 6. Arquivo `.gitignore` (opcional)

**Explicação**  
Evita commit acidental de credenciais (`.env`), ambiente virtual (`venv/`), cache Python e arquivos do editor.

```gitignore
.env
__pycache__/

.vscode/
.DS_Store
venv/
```

---

## 7. Executar e verificar

Com o venv ativo e dependências instaladas, a partir da raiz do projeto:

```bash
python analise_clima.py
python mapa_calor.py
python mapa_calor_temperatura_anual.py
```

Confira em `output/`:

- `grafico_barras_temperatura.png`, `grafico_pizza_chuva.png`, `grafico_dispersao_temperatura_umidade.png`
- `mapa_calor_temperaturas.html`
- `temperatura_media_anual_cidades.csv` e `mapa_calor_temperatura_media_anual.html`

---

## 8. Referência rápida das APIs

| Objetivo | Base URL | Parâmetros típicos |
|----------|----------|-------------------|
| Previsão recente | `https://api.open-meteo.com/v1/forecast` | `latitude`, `longitude`, `hourly=...` ou `current=...`, `forecast_days` |
| Série histórica / arquivo | `https://archive-api.open-meteo.com/v1/archive` | `start_date`, `end_date`, `daily=...`, `timezone` |

Documentação oficial: [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs).

---

*Tutorial alinhado ao estado do repositório para uso em aula. Ajuste coordenadas, ano (`ano = ...`) e listas de cidades conforme o exercício desejado.*
