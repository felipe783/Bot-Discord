# Arquitetura

## Inicialização

```mermaid
sequenceDiagram
    participant M as main.py
    participant B as Teste (commands.Bot)
    participant C as Comandos/**/*.py
    participant G as __load_groups.py
    participant D as Discord
    M->>M: load_dotenv() + DISCORD_TOKEN + load_db()
    M->>B: bot.run(TOKEN)
    B->>C: setup_hook: load_extension de cada .py (exceto _*)
    B->>G: load_all_groups(bot)
    G->>B: tree.add_command(blackjack_group / historia_group)
    B->>D: tree.sync() (global)
    D-->>B: on_ready
    B->>B: Historias_diaria.start() + mensagem no canal de início
    B->>B: cogs de canais: cria "historias" e "comandos-bot-teste" se faltarem
```

## Componentes

```mermaid
flowchart TD
    MAIN[main.py<br/>Teste + Historias_diaria] --> CL[Cogs: Cog_normal, Cog_ADM, Cogs_channel]
    MAIN --> LG[__load_groups.py]
    LG --> BJ[Groups/Blackjack<br/>iniciar, hit, stand, double_down]
    LG --> HI[Groups/Historia<br/>escrever, ver_historia]
    BJ --> EST[(Estados/estados_Blackjack.jogos<br/>em memória)]
    HI --> JSON[(Json/Data.json)]
    MAIN --> JSON
    CL --> JSON
    CL --> MOD[API Modrinth<br/>api.modrinth.com/v2/search]
```

## Tarefa diária

```mermaid
flowchart LR
    T[tasks.loop 1 min] --> H{12:00 em America/Sao_Paulo?}
    H -->|não| T
    H -->|sim| L[load_db]
    L --> V{historia vazia?}
    V -->|sim| S1[envia 'Sem histórias pra zerar']
    V -->|não| S2[envia história + @everyone] --> Z[historia = [] + save_db]
```

## Tratamento de erros

- Falhas ao carregar um cog ou group são **impressas no console** e o bot segue com os demais.
- A tarefa diária captura exceções e só imprime a mensagem.
- Comandos não tratam erros do Discord (permissão de *timeout*, canal inexistente) nem da API do Modrinth: a exceção sobe para o handler padrão do discord.py, e o usuário vê "O aplicativo não respondeu".
- Logs vão para o `stdout` com `print` (no Docker, `docker logs`).
