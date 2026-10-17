# Visão Geral do Sistema

O Bot-Discord é um bot de entretenimento e utilidades para **um servidor Discord específico**. Ele responde a slash commands e mantém uma pequena persistência local em JSON.

## Finalidade

- Montar uma **história coletiva**: cada membro acrescenta uma frase, e ao meio-dia (horário de São Paulo) a história é publicada no canal `historias` e zerada.
- Jogar **Blackjack** contra o dealer; quem perde leva *timeout* de tantos minutos quanto apostou.
- **Buscar mods** no Modrinth e mostrar descrição, autor e downloads.
- Dar aos administradores comandos para **zerar a história** e **recarregar os comandos**.
- Criar automaticamente os canais de que o bot precisa.

## Entrada principal

- [[Main e Bot|main.py]]: cria o bot, carrega os comandos e inicia a tarefa diária.
- Slash commands no Discord: ver [[Resumo Principal (Bot-Discord)]].
## Saída principal

- Mensagens e embeds no Discord; *timeouts* aplicados a membros.
- `Json/Data.json`: frases da história e ID do canal de histórias ([[Loader e Data.json]]).

## Módulos principais

- [[!Modulo Core (Bot-Discord)]]: `main.py`, `loader.py` e o carregamento de cogs/groups.
- [[!Modulo Comandos (Bot-Discord)]]: `/ping`, `/ajuda`, `/busca_mod`, `/apagar`, `/reload`.
- [[!Modulo História (Bot-Discord)]]: grupo `/historia` e publicação diária.
- [[!Modulo Blackjack]]: grupo `/blackjack`.
- [[!Modulo Canais (Bot-Discord)]]: criação dos canais.


[[Dependencias (Bot-Discord)]] · [[Arquitetura (Bot-Discord)]]
