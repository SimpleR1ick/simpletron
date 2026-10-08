# 🔒 Política de Privacidade — Simpletron (ST-3000)

*Última atualização: Outubro de 2026*

A sua privacidade é fundamental para nós. Esta **Política de Privacidade** descreve quais informações são coletadas, como são utilizadas e como são protegidas pelo bot **Simpletron** (também conhecido como **ST-3000** ou **Simple AI**).

---

## 1. Dados Coletados e Finalidade

O Simpletron opera sob o princípio da **minimização de dados**, coletando e processando estritamente as informações necessárias para a execução de seus comandos:

| Dado Coletado | Finalidade | Armazenamento |
| :--- | :--- | :--- |
| **IDs de Servidor (`Guild ID`)** | Identificar as preferências de cada servidor (ex: status e canal de boas-vindas). | Persistido em arquivo local de configuração. |
| **IDs de Canal (`Channel ID`)** | Enviar alertas automáticos (jogos grátis e mensagens de boas-vindas). | Persistido em arquivo local de configuração. |
| **IDs e Nomes de Usuários (`User ID` / Nickname)** | Registrar autoria de frases no caderno de pérolas (`/quote add`) e marcar membros em boas-vindas. | Persistido no arquivo de pérolas do servidor. |
| **Conteúdo de Mensagens de Comandos** | Processar o prompt enviado pelo usuário para a API do Google Gemini (`/perguntar`) ou converter links de mídias. | Processamento volátil em memória; **não é persistido em disco**. |

---

## 2. O Que NUNCA Coletamos

O Simpletron:
- **NÃO** lê nem armazena mensagens privadas (DMs).
- **NÃO** monitora nem grava áudios ou transmissões em canais de voz.
- **NÃO** coleta dados pessoais sensíveis (senhas, documentos, cartões ou dados financeiros).
- **NÃO** registra o histórico de conversas gerais dos canais de texto em que está presente.

---

## 3. Serviços de Terceiros

Para fornecer certas funcionalidades, o bot se comunica com serviços externos de forma segura:
- **Discord API:** Comunicação fundamental com a plataforma, sujeita à [Política de Privacidade do Discord](https://discord.com/privacy).
- **Google Gemini API:** Utilizada exclusivamente para processar perguntas feitas através do comando `/perguntar` ou menções diretas à IA, de acordo com as [Diretrizes de Privacidade da Google](https://policies.google.com/privacy).
- **CheapShark API:** Utilizada exclusivamente para consultar ofertas e jogos gratuitos para PC (nenhum dado de usuário é enviado).

Nenhum dado pessoal coletado é vendido, compartilhado ou comercializado com terceiros para fins de publicidade ou rastreamento.

---

## 4. Retenção e Exclusão de Dados

- Os dados de configuração e pérolas ficam armazenados no servidor privado do bot em formato JSON estruturado.
- Caso o administrador de um servidor decida remover o bot ou deseje apagar os dados armazenados (como as pérolas ou configurações de boas-vindas), poderá solicitar a exclusão total a qualquer momento.

---

## 5. Contato e Solicitações de Privacidade

Para solicitar a remoção de dados ou esclarecer dúvidas sobre esta Política de Privacidade:
- **Repositório Oficial:** [github.com/SimpleR1ick/simpletron](https://github.com/SimpleR1ick/simpletron)
- Abra uma solicitação ou *Issue* no GitHub endereçada aos mantenedores do projeto.
