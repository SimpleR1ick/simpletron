<p align="center">
  <img src="assets/kebab.png" alt="Simpletron Bot - Kebabtech" width="480" style="border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);" />
</p>

<h1 align="center">🤖 Simpletron (Simple AI)</h1>

<p align="center">
  <b>O bot assistente multifuncional e escalável para o servidor do Discord <i>The Simple Place</i>.</b><br>
  Desenvolvido em Python com <code>discord.py</code>, arquitetura modular de <b>Cogs</b> e inteligência artificial integrada.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Discord.py-v2.7-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord.py" />
  <img src="https://img.shields.io/badge/Hospedagem-Oracle%20Cloud%2024%2F7-F80000?style=for-the-badge&logo=oracle&logoColor=white" alt="Oracle Cloud" />
  <img src="https://img.shields.io/badge/IA-Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini" />
  <img src="https://img.shields.io/badge/Licen%C3%A7a-MIT-green?style=for-the-badge" alt="MIT License" />
</p>

---

## 📖 Sobre o Projeto

O **Simpletron** nasceu para resolver o problema clássico de servidores de amigos: a poluição de bots de terceiros cheios de paywalls e propagandas. Em vez de adicionar vários bots genéricos, o Simpletron centraliza tudo em uma única aplicação leve, privada e modular:

* 🧠 **IA com Google Gemini:** Responde a discussões e perguntas complexas com bom humor.
* ⚔️ **Matchmaking de Times:** Divide a galera em 2 equipes equilibradas para jogos como CS2 e Valorant.
* 🎲 **Roleta da Indecisão:** Sorteia o que jogar quando ninguém consegue escolher.
* 📝 **Caderno de Pérolas:** Registra frases marcantes e engraçadas ditas no servidor ao longo do tempo.
* 🎁 **Rastreador de Jogos Grátis:** Notifica periodicamente novidades gratuitas na Steam e Epic Games.
* 🎬 **Embed Fixer Automático:** Converte links de TikTok, Instagram, Twitter/X e Reddit em players nativos no chat.
* 🥙 **Kebabtech:** Porque todo servidor precisa do ápice da culinária cibernética de Night City.

---

## 🎮 Comandos Disponíveis (Slash Commands & Prefixo `!st`)

Todos os comandos podem ser acionados tanto por comandos de barra (`/`) quanto pelo prefixo **`!st`** (ou mencionando **`@Simple AI`**), servindo como fallback caso a interface do Discord apresente instabilidade:

| Comando Slash | Prefixo Alternativo (`!st`) | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| `/times [canal]` | `!st times [canal]` | Divide os membros conectados na chamada de voz em 2 equipes. | `!st times` |
| `/oquejogar` | `!st oquejogar` | Sorteia aleatoriamente um jogo da roleta do grupo. | `!st oquejogar` |
| `/adicionarjogo <nome>` | `!st adicionarjogo <nome>` | Adiciona um novo título à lista da roleta. | `!st adicionarjogo Lethal Company` |
| `/quote add <autor> <frase>` | `!st quote add @autor frase` | Salva uma pérola histórica no caderno do servidor. | `!st quote add @amigo "não fui eu"` |
| `/quote random` | `!st quote random` | Sorteia e exibe uma frase marcante salva no servidor. | `!st quote random` |
| `/quote listar` | `!st quote listar` | Mostra o total de pérolas acumuladas no caderno. | `!st quote listar` |
| `/jogosgratis` | `!st jogosgratis` | Consulta promoções ativas de jogos 100% gratuitos para PC. | `!st jogosgratis` |
| `/perguntar <pergunta>` | `!st perguntar <dúvida>` | Envia uma dúvida para a IA do Google Gemini. | `!st perguntar quem tem razão?` |
| `/kebab` | `!st kebab` | Invoca a iguaria cibernética Kebabtech de Night City. | `!st kebab` |
| `/boasvindas <ativar/desativar/status/testar>` | `!st boasvindas <comando>` | Gerencia recepção e mensagens automáticas para novos membros. | `/boasvindas ativar #geral` |
| — | `!st ajuda` | Exibe o menu com todos os comandos alternativos. | `!st ajuda` |

> 💡 **Embed Fixer:** Funciona automaticamente no chat de texto (especialmente em `#memes-e-midia`). Ao postar links do Twitter, Instagram Reels, TikTok ou Reddit, o bot reescreve com o preview corrigido.

---

## 🏗️ Arquitetura do Projeto

O projeto segue as melhores práticas da documentação do `discord.py`, utilizando **Cogs e Extensions**. Cada categoria de funcionalidade vive em um módulo isolado:

```text
simpletron/
├── assets/                    # Imagens e mídias locais (ex: kebab.png)
│   └── kebab.png
├── cogs/                      # Módulos independentes do bot
│   ├── ai.py                  # IA Gemini (/perguntar e menções)
│   ├── fun.py                 # Comandos de memes e diversão (/kebab)
│   ├── games.py               # Matchmaking e roleta (/times, /oquejogar, /adicionarjogo)
│   ├── giveaways.py           # Monitoramento automático de jogos grátis
│   ├── media.py               # Embed Fixer de links de redes sociais
│   ├── quotes.py              # Caderno de Pérolas (/quote)
│   └── welcome.py             # Recepção automática de membros (/boasvindas)
├── config/
│   └── settings.py            # Carregamento e validação das variáveis do .env
├── data/                      # Persistência de dados em JSON
│   ├── games.json
│   ├── giveaways.json
│   ├── quotes.json
│   └── welcome.json
├── utils/
│   └── storage.py             # Funções utilitárias de leitura e gravação
├── .env                       # Segredos locais (NUNCA commitado - listado no .gitignore)
├── .env.example               # Template documentado para configuração
├── .gitignore                 # Filtro de segurança para arquivos sensíveis
├── guide.py                   # Script de configuração do canal de ajuda
├── main.py                    # Inicializador principal (carrega cogs dinamicamente)
├── README.md                  # Documentação do projeto
└── requirements.txt           # Dependências do Python
```

---

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
* Python 3.10 ou superior
* Git instalado

### 2. Clonar o repositório
```bash
git clone https://github.com/SimpleR1ick/simpletron.git
cd simpletron
```

### 3. Configurar o ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente
Copie o template e preencha com o seu token:
```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```env
DISCORD_BOT_TOKEN="seu_token_secreto_aqui"
DISCORD_GUILD_ID=1556868528311636119
GEMINI_API_KEY="sua_chave_gemini_opcional"
```

### 5. Iniciar o Bot
```bash
python main.py
```

---

## ☁️ Hospedagem 24/7 na Oracle Cloud

O bot roda em produção em uma máquina virtual Linux Ubuntu no plano **Always Free** da **Oracle Cloud Infrastructure (OCI)**, gerenciado pelo serviço `systemd`:

### Gerenciamento do Serviço no Servidor:
```bash
# Verificar status em tempo real
sudo systemctl status discord-bot

# Acompanhar logs ao vivo
sudo journalctl -u discord-bot -f

# Reiniciar o serviço
sudo systemctl restart discord-bot
```

Com o `Restart=always` ativado no unit do systemd, se a máquina reiniciar ou o processo falhar, ele se recupera automaticamente em 10 segundos.

---

## 🛡️ Segurança e Variáveis de Ambiente

Nenhum segredo ou chave de API é commitado neste repositório. O arquivo `.gitignore` protege:
* Variáveis de ambiente (`.env`)
* Ambientes virtuais (`.venv/`)
* Chaves privadas SSH (`*.key`)
* Arquivos de cache e logs (`__pycache__/`, `*.log`)

---

## 📝 Licença & Diretrizes

Distribuído sob a licença [MIT](LICENSE). Desenvolvido para a comunidade do **The Simple Place**.

* 📜 [Termos de Serviço](TERMS.md)
* 🔒 [Política de Privacidade](PRIVACY.md)
