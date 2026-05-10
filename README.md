# Projeto de Análise de Dados Climáticos com Python

Projeto pensado para **uso em sala de aula**, com o propósito de **demonstrar possibilidades de uso de bibliotecas em Python** na prática — desde consumo de APIs até visualização e mapas.

**Prof.: Felipe Alves**

## Objetivo didático

Em aula, o material apoia a prática com bibliotecas como:

- Requests
- JSON (módulo da biblioteca padrão)
- Pandas
- Matplotlib
- Folium (mapas interativos), nos scripts de mapa de calor

## Fonte dos dados

Os dados foram obtidos por meio da API pública [Open-Meteo](https://open-meteo.com/).

## Funcionalidades

- Acessa dados climáticos online;
- Converte a resposta da API para JSON;
- Organiza os dados com Pandas;
- Gera análise exploratória simples;
- Cria gráficos de barras, pizza e dispersão;
- Gera mapas de calor em HTML (quando aplicável aos scripts do repositório).

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Em seguida, execute os scripts `.py` do projeto conforme as orientações da aula (por exemplo `analise_clima.py`, `mapa_calor.py` ou `mapa_calor_temperatura_anual.py`).
