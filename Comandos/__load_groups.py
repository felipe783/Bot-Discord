import pkgutil
import importlib
from pathlib import Path

async def load_all_groups(bot, groups_base_path="Comandos.Cog_normal.Groups"):
    """Carrega todos os command groups automaticamente"""
    groups_path = Path("Comandos/Cog_normal/Groups")
    
    if not groups_path.exists():
        print("Pasta de Groups não encontrada")
        return
    
    # Itera sobre cada pasta dentro de Groups
    for item in groups_path.iterdir():
        if item.is_dir() and not item.name.startswith("_"):
            group_name = item.name
            try:
                # Importa o módulo do grupo
                module_name = f"{groups_base_path}.{group_name}"
                module = importlib.import_module(module_name)
                
                # Procura por um objeto chamado f"{group_name}_group"
                group_attr = f"{group_name.lower()}_group"
                if hasattr(module, group_attr):
                    group = getattr(module, group_attr)
                    bot.tree.add_command(group)
                    print(f"Adicionado group: {group_name}")
            except Exception as e:
                print(f"Falha ao carregar group {group_name}: {e}")