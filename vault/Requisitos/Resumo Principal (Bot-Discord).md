### Linguagem Principal

``Python``
### Comandos

| Comando | Quem | O que faz |
|---|---|---|
| `/ping` | todos | responde "PONG😎🔥" |
| `/ajuda` | todos | dois embeds efêmeros com os comandos gerais e ADM |
| `/busca_mod [texto]` | todos | busca no Modrinth e mostra o 1º resultado (título, descrição, autor, downloads, link) |
| `/historia escrever [texto]` | todos | acrescenta a frase e mostra a história inteira |
| `/historia ver_historia` | todos | mostra a história (efêmero) |
| `/blackjack iniciar <aposta>` | todos | começa uma partida; `aposta` = minutos de *timeout* se perder |
| `/blackjack hit` | jogador | compra uma carta |
| `/blackjack stand` | jogador | para e compara com o dealer |
| `/blackjack double_down` | jogador | dobra a aposta, compra uma carta e resolve a partida |
| `/apagar` | ADM | publica e zera a história antes do meio-dia |
| `/reload` | ADM | recarrega as extensões |

> `/apagar` e `/reload` têm `default_permissions(administrator=True)`; o `/apagar` ainda confere um **cargo fixo** pelo ID.

## Fluxo Geral — Inicialização

1. `main.py` carrega o `.env` e o `Json/Data.json` ([[Loader e Data.json]]).
2. No `setup_hook`, todo `.py` de `Comandos/` vira extensão, e os groups são adicionados ([[Carregamento de Cogs e Groups]]).
3. `tree.sync()` registra os slash commands no Discord (globalmente).
4. No `on_ready`, começa a tarefa diária, o bot avisa no canal de início, e os cogs de canais criam o que faltar ([[Criação de Canais]]).

## Fluxo Geral — História

1. `/historia escrever` adiciona a frase em `Data.json["historia"]` ([[História Colaborativa]]).
2. Ao meio-dia (ou por `/apagar`), a história é enviada ao canal `historias` com `@everyone` e a lista é zerada.

## Fluxo Geral — Blackjack

1. `/blackjack iniciar` embaralha um baralho, dá 2 cartas a cada um e guarda a mesa em memória por `user_id` ([[Regras do Blackjack]]).
2. `hit`, `stand` ou `double_down` continuam a partida; ao perder, o jogador leva *timeout* de `aposta` minutos (o dobro no `double_down`).
