# Sobre os Arquivos

`main.py` (`setup_hook`) e `Comandos/__load_groups.py` são os **Responsáveis por Registrar os Comandos** sem lista manual.
# Funcionalidades

## Cogs

````python
for file in Path("Comandos").rglob("*.py"):
    if file.name.startswith("_"):
        continue
    module = f"Comandos.{relative_path.with_suffix('').as_posix().replace('/', '.')}"
    await self.load_extension(module)
````

- Todo `.py` vira extensão; cada uma precisa de `async def setup(bot)`. Os arquivos dos groups têm um `setup` vazio só para isso.
- `__load_groups.py` começa com `_`, então é pulado pelo laço e não é carregado como extensão (antes do commit `72c1e09` ele se chamava `load_groups.py` e gerava um erro inofensivo no console).

## Groups

Convenção: a pasta `Comandos/Cog_normal/Groups/<Nome>/` tem um `__init__.py` que importa `<nome>_group` e todos os módulos irmãos (cada um decora uma função com `@<nome>_group.command`). O `load_all_groups` importa o pacote e faz `bot.tree.add_command(<nome>_group)`.

````python
group_attr = f"{group_name.lower()}_group"   # Blackjack -> blackjack_group
if hasattr(module, group_attr):
    bot.tree.add_command(getattr(module, group_attr))
````

Para criar um grupo novo: crie a pasta, o `<nome>_group.py` com `app_commands.Group(...)`, os subcomandos e o `__init__.py` no mesmo padrão.

## Sincronização

`tree.sync()` **global** pode levar até ~1 h para aparecer em todos os servidores. Durante o desenvolvimento, `tree.sync(guild=...)` é instantâneo.

> [!warning] /reload
> O `/reload` usa `reload_extension` em todos os arquivos, mas não recarrega os groups (que são adicionados à árvore, não carregados como cog) e não faz `tree.sync()`. Ver [[Comandos ADM]].
