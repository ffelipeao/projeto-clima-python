# Projeto de Análise de Dados Climáticos com Python

Projeto pensado para **uso em sala de aula**, com o propósito de **demonstrar possibilidades de uso de bibliotecas em Python** na prática — desde consumo de APIs até visualização e mapas.

**Prof.: Felipe Alves**

## Construção do projeto (tutoriais)

Para **montar o projeto atual do zero** e **versionar o trabalho no Git**, siga os tutoriais em Markdown deste repositório — eles são o roteiro oficial da disciplina:

| Arquivo | Conteúdo |
|---------|----------|
| [`TUTORIAL_CONSTRUCAO.md`](TUTORIAL_CONSTRUCAO.md) | Passo a passo para criar ambiente, dependências, pastas e cada script (API, Pandas, gráficos e mapas). |
| [`TUTORIAL_GIT_ALUNOS.md`](TUTORIAL_GIT_ALUNOS.md) | Passo a passo para salvar o projeto no Git e (opcional) publicar no GitHub. |

### Resumo do que será construído

- **Ambiente**: pasta do projeto, ambiente virtual recomendado, pasta `output/` para arquivos gerados e instalação das bibliotecas via `requirements.txt`.
- **`analise_clima.py`**: consumo da API Open-Meteo (previsão horária), organização em DataFrame, agregação por dia e **três gráficos** (barras, pizza e dispersão) salvos em `output/`.
- **`mapa_calor.py`**: temperatura **atual** em várias cidades brasileiras e **mapa de calor interativo** em HTML com Folium.
- **`mapa_calor_temperatura_anual.py`**: dados **históricos** por ano, **média anual** por cidade, exportação em **CSV** e outro **mapa de calor** em HTML.
- **Git**: repositório local, commits e, se desejado, repositório remoto (ex.: GitHub) com `push`.

Depois de seguir os tutoriais, use a seção **Como executar** abaixo para rodar os scripts já prontos.

## Objetivo didático

Em aula, o material apoia a prática com bibliotecas como:

- Requests
- JSON (módulo da biblioteca padrão)
- Pandas
- Matplotlib
- Folium (mapas interativos), nos scripts de mapa de calor

## Fonte dos dados: Open-Meteo

Os dados deste projeto vêm da API pública **[Open-Meteo](https://open-meteo.com/)**, um serviço de **dados meteorológicos** acessível por **HTTP**, com respostas em **JSON**.

**Resumo para a aula**

- Oferece **previsão** (por exemplo, série **horária** com alguns dias à frente) e **arquivo histórico** (séries **diárias** ou outras granularidades), conforme o endpoint e os parâmetros usados.
- Neste repositório usamos, em geral: **previsão** em `https://api.open-meteo.com/v1/forecast` (temperatura atual ou horária) e **histórico** em `https://archive-api.open-meteo.com/v1/archive` (médias diárias para calcular a média anual).
- Para experimentos em sala costuma bastar **latitude**, **longitude** e os **campos** desejados na URL (temperatura, umidade, precipitação, etc.), sem cadastro obrigatório para o uso básico descrito na documentação oficial.
- A documentação e os parâmetros disponíveis estão em [open-meteo.com — Documentação](https://open-meteo.com/en/docs).

## Funcionalidades

- Acessa dados climáticos online;
- Converte a resposta da API para JSON;
- Organiza os dados com Pandas;
- Gera análise exploratória simples;
- Cria gráficos de barras, pizza e dispersão;
- Gera mapas de calor em HTML (quando aplicável aos scripts do repositório).
