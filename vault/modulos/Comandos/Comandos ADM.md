# Sobre os Arquivos

`Cog_ADM/apagar.py` e `Cog_ADM/reload.py` são os **comandos de administração**. Ambos têm `@app_commands.default_permissions(administrator=True)`: por padrão, o Discord só mostra o comando a administradores (o dono do servidor pode mudar isso nas integrações).
# Funcionalidades

## /apagar

1. Confere se o usuário tem o **cargo de ID fixo**; senão, responde "❌ Tu não tem cargo pra isso não".
2. Publica a história no canal de histórias (com `@everyone`) e zera a lista, como a tarefa diária ([[História Colaborativa]]).
3. Responde "Historias apagadas" de forma efêmera.

## /reload

Percorre `Comandos/` e faz `reload_extension` em cada módulo.

> [!warning] Defeitos
> - `send_message` está **dentro do laço**: a primeira extensão recarregada responde, e as seguintes lançam `InteractionResponded` (capturado e impresso como "Falha ao carregar").
> - Se nenhuma extensão recarregar, a interação fica sem resposta.
> - Não recarrega os command groups nem faz `tree.sync()`.
> - O canal `ID` é lido e não é usado.
> - No `/apagar`, `db("historia:", [])` é um erro (chama o dicionário), e o canal vem do `DB` lido na importação do módulo.
