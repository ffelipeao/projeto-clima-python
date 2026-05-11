# Tutorial: salvando o projeto no Git (para alunos)

Este guia ensina o **passo a passo** para versionar o projeto de clima com **Git** e, se quiserem, publicar em um repositório remoto (ex.: **GitHub**), usando o próprio computador de cada aluno.

---

## 1. O que você vai conseguir ao final

- Ter uma **pasta do projeto** reconhecida pelo Git (um **repositório** local).
- **Registrar versões** do trabalho (**commits**) com mensagens claras.
- (Opcional) Enviar o projeto para a **nuvem** (`git push`) e acessar de outro lugar ou compartilhar com o professor.

---

## 2. Antes de começar: instalar e conferir o Git

**Passo 2.1** — O Git é um programa separado do Python. Instale-o se ainda não tiver:

- **macOS**: costuma vir com o Xcode Command Line Tools (`xcode-select --install`) ou instale pelo site [git-scm.com](https://git-scm.com/).
- **Windows**: [Git for Windows](https://git-scm.com/download/win).
- **Linux**: por exemplo `sudo apt install git` (Ubuntu/Debian).

**Passo 2.2** — Abra o **Terminal** (macOS/Linux) ou **Git Bash** / **PowerShell** (Windows), entre na pasta do projeto e confira:

```bash
git --version
```

Se aparecer algo como `git version 2.x.x`, está pronto.

**Passo 2.3** — (Recomendado, uma vez só) Informe nome e e-mail que aparecerão nos commits:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

Use o e-mail da sua conta GitHub, se for usar GitHub.

---

## 3. Ideias rápidas (o que é cada coisa)

| Termo | Significado em uma frase |
|--------|---------------------------|
| **Repositório** | Pasta do projeto que o Git está “observando”. |
| **Commit** | Um “retrato” salvo do projeto num instante, com mensagem. |
| **Remoto** (`origin`) | Cópia do repositório na internet (GitHub, GitLab, etc.). |
| **Push** | Enviar seus commits locais para o remoto. |
| **Pull** | Trazer alterações do remoto para sua máquina. |

---

## 4. Entrar na pasta do projeto

**Passo 4.1** — No terminal, vá até a pasta onde está o código (ajuste o caminho se for diferente):

```bash
cd ~/caminho/para/projeto-clima-python
```

**Passo 4.2** — Liste os arquivos para ter certeza de que está no lugar certo:

```bash
ls
```

Você deve ver arquivos como `analise_clima.py`, `requirements.txt`, etc.

---

## 5. Situação A: a pasta ainda **não** é um repositório Git

**Passo 5.1** — Verifique se já existe Git nessa pasta:

```bash
git status
```

- Se aparecer **“not a git repository”**, siga o **Passo 5.2**.
- Se já listar branch e arquivos, pule para a **Seção 6**.

**Passo 5.2** — Inicialize o repositório:

```bash
git init
```

Isso cria a pasta oculta `.git` (não apague essa pasta).

**Passo 5.3** — (Opcional, mas comum) Defina o nome da branch principal como `main`:

```bash
git branch -M main
```

---

## 6. Arquivo `.gitignore`: o que **não** mandar para o Git

**Passo 6.1 — Por que existe?**  
Alguns arquivos não devem ir para o repositório: ambiente virtual grande, segredos em `.env`, cache do Python, configurações pessoais do editor.

**Passo 6.2 — Neste projeto** já existe um `.gitignore` na raiz com, entre outros:

- `venv/` — pasta do ambiente virtual  
- `.env` — variáveis secretas (chaves de API, etc.)  
- `__pycache__/` — cache gerado pelo Python  
- `.vscode/`, `.DS_Store` — lixo local / editor  

Não é obrigatório decorar: o importante é **não** tentar versionar `venv/` nem senhas.

**Passo 6.3 — Arquivos gerados em `output/`**  
Gráficos PNG, CSV e HTML em `output/` podem ser commitados ou não, dependendo da regra da disciplina. Se forem sempre **regenerados** pelos scripts e forem pesados, o professor pode pedir para ignorá-los; nesse caso acrescente uma linha `output/` no `.gitignore` (só se combinado na aula).

---

## 7. Primeiro “retrato”: adicionar arquivos e fazer o primeiro commit

**Passo 7.1** — Veja o que o Git enxerga:

```bash
git status
```

Arquivos “untracked” ou “modified” aparecem em vermelho até serem adicionados.

**Passo 7.2** — Adicione **todos** os arquivos que você quer nesta versão (respeitando o `.gitignore`):

```bash
git add .
```

Ou adicione só alguns:

```bash
git add analise_clima.py mapa_calor.py requirements.txt
```

**Passo 7.3** — Crie o commit com uma **mensagem clara** (o professor e o “você do futuro” agradecem):

```bash
git commit -m "Primeira versão: scripts de clima e dependências"
```

Se o Git disser que não há nada para commitar, talvez nada tenha sido adicionado ou já estava tudo commitado — rode de novo `git status`.

**Passo 7.4** — Confira o histórico:

```bash
git log --oneline
```

---

## 8. Situação B: projeto já tinha Git (ex.: clonado da aula)

Se você **clonou** um repositório do professor:

```bash
git clone https://github.com/ALGUEM/projeto-clima-python.git
cd projeto-clima-python
```

Seu trabalho local já é um repositório Git. Depois de editar arquivos:

```bash
git status
git add .
git commit -m "Descreva o que mudou, ex.: adiciona mapa anual"
```

Para **enviar** para o GitHub do professor, só funciona se você tiver **permissão de escrita**; em muitas aulas cada aluno **forka** ou cria **o próprio** repositório (próxima seção).

---

## 9. Salvar na nuvem: GitHub (criar repositório **vazio**)

**Passo 9.1** — Crie uma conta em [github.com](https://github.com) se ainda não tiver.

**Passo 9.2** — No site: **New repository** (Novo repositório).

- Nome: por exemplo `projeto-clima-python`.
- Deixe **sem** README, **sem** `.gitignore` e **sem** licença **se** você já tem esses arquivos localmente (evita conflito na primeira subida). Se o GitHub oferecer “importar” e você já tem tudo local, prefira repositório vazio.

**Passo 9.3** — Copie a URL HTTPS do repositório (algo como `https://github.com/SEU-USUARIO/projeto-clima-python.git`).

---

## 10. Conectar sua pasta ao GitHub e enviar (`push`)

Execute **na pasta do projeto**, já com pelo menos um commit local (Seção 7).

**Passo 10.1** — Associe o remoto chamado `origin` (troque pela sua URL):

```bash
git remote add origin https://github.com/SEU-USUARIO/projeto-clima-python.git
```

Se der erro “remote origin already exists”, veja o remoto atual:

```bash
git remote -v
```

Para trocar a URL:

```bash
git remote set-url origin https://github.com/SEU-USUARIO/projeto-clima-python.git
```

**Passo 10.2** — Envie a branch `main` pela primeira vez:

```bash
git push -u origin main
```

O terminal pode pedir **login**: no GitHub moderno costuma-se usar um **Personal Access Token** em vez da senha da conta. Siga as instruções do GitHub em *Settings → Developer settings → Personal access tokens*.

**Passo 10.3** — Atualize a página do repositório no navegador: seus arquivos devem aparecer lá.

---

## 11. Rotina depois que tudo está configurado

Sempre que terminar um pedaço útil do trabalho:

```bash
git status
git add .
git commit -m "Mensagem curta dizendo o que mudou"
git push
```

Se **outra pessoa** (ou você em outro PC) alterou o remoto antes:

```bash
git pull
```

Resolva conflitos se o Git avisar, depois `commit` e `push` de novo.

---

## 12. Erros comuns (e o que fazer)

| Mensagem ou situação | O que significa / o que fazer |
|----------------------|--------------------------------|
| `not a git repository` | Você não está na pasta certa ou não rodou `git init`. |
| `nothing to commit, working tree clean` | Tudo já está salvo em commit; não há mudanças novas. |
| `failed to push` / `rejected` | Alguém subiu commits antes; rode `git pull` (com rebase opcional: `git pull --rebase`) e tente `push` de novo. |
| Commitou arquivo grande por engano | Peça ajuda ao professor; dá para corrigir com `git rm` e novo commit ou ferramentas mais avançadas. |
| Subiu `.env` com senha | **Revogue** a chave na API, remova o arquivo do histórico com ajuda (não basta só apagar no próximo commit). |

---

## 13. Checklist rápido para entregar na disciplina

- [ ] `git config` com nome e e-mail corretos  
- [ ] Repositório inicializado ou clonado  
- [ ] `.gitignore` presente e `venv/` **não** versionado  
- [ ] Commits com mensagens legíveis  
- [ ] (Se pedido) Repositório no GitHub com link enviado ao professor  
- [ ] Último `git push` feito antes do prazo  

---

## 14. Onde aprender mais (opcional)

- Documentação oficial: [https://git-scm.com/doc](https://git-scm.com/doc)  
- GitHub: [https://docs.github.com](https://docs.github.com)  

Bom trabalho e bons commits.
