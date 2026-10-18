# Sobre os Arquivos

`historia_group.py`, `historia.py`, `ver_historia.py` e a tarefa `Historias_diaria` de `main.py` implementam a **História Colaborativa**.

Pasta: `Comandos/Cog_normal/Groups/Historia/` (command group `/historia`); o `/apagar` também altera a história.
# Funcionalidades

## /historia escrever [texto]

````python
db = load_db()
db["historia"].append(texto)
save_db(db)
historia_texto = ", ".join(db["historia"])
````

Responde publicamente com a história inteira. O `texto` é opcional, e sem ele uma frase vazia é adicionada.

## /historia ver_historia

Mostra a história de forma **efêmera**.

## Publicação diária

- Às **12:00 em `America/Sao_Paulo`**, a tarefa envia ao canal `historias`: `História antiga: <frases> / Historias zeradas🔥 / ||@everyone||`, e zera a lista.
- Sem frases, envia "Sem histórias pra zerar.😭".
- O canal é `Data.json["ID_Historia"][0]`, gravado pelo [[Criação de Canais|cog de criação de canais]].
- `/apagar` faz o mesmo sob demanda ([[Comandos ADM]]).

> [!warning] Observações
> - O loop só age se o horário for **exatamente** 12:00 no momento da checagem: com o bot fora do ar nesse minuto, a publicação daquele dia não acontece.
> - Sem trava no JSON, frases simultâneas podem se perder.
> - A resposta pública de `escrever` cresce com a história e pode passar do limite de 2000 caracteres do Discord.
> - O conteúdo é escrito pelos usuários e repetido com `@everyone` no canal.
