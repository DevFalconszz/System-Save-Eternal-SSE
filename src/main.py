#!/usr/bin/env python3
import sys
import os
import platform

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _ensure_config():
    from src.utils.config import ensure_config_dir
    ensure_config_dir()


def _print_transparency_header(action_name, details):
    print()
    print("  " + "=" * 56)
    print(f"  ⚠  SSE — {action_name}")
    print("  " + "=" * 56)
    for line in details:
        print(f"    • {line}")
    print("  " + "=" * 56)
    print()


def _confirm_action(prompt="Deseja continuar? (s/N): ") -> bool:
    resp = input(f"  {prompt}").strip().lower()
    return resp == "s"


def main():
    _ensure_config()
    try:
        import tkinter
        from src.ui.app import run_gui
        run_gui()
    except ImportError:
        print("  Tkinter não disponível — usando modo terminal.")
        cli_main()


def cli_main():
    from src.console.menu import (
        print_banner, select_game, select_saves, select_destinations,
        configure_destination, get_repo_path, sync_to_repo, get_timestamp,
        detect_launchers_menu, sync_worlds_to_launcher, sync_worlds_to_repo,
    )
    from src.utils import config as cfg

    print_banner()

    saves_repo_path = get_repo_path()
    if not saves_repo_path:
        sys.exit(1)

    game_choice = select_game()

    if game_choice == "play_minecraft":
        _cli_play_minecraft(saves_repo_path)
    else:
        _cli_backup(game_choice, saves_repo_path)


def _cli_backup(game_choice, saves_repo_path):
    from src.console.menu import (
        print_banner, print_step, print_ok, print_fail, print_info,
        select_saves, select_destinations, configure_destination,
        sync_to_repo, get_timestamp,
    )

    saves = []
    if game_choice == "minecraft":
        from src.games.minecraft import MinecraftFinder
        finder = MinecraftFinder()
        print_info("Buscando saves do Minecraft...")
        saves = finder.find_saves()
    elif game_choice == "pokemon":
        from src.games.pokemon import PokemonFinder
        finder = PokemonFinder(system_wide_search=True)
        print_info("Buscando saves de Pokémon...")
        saves = finder.find_saves()

    if not saves:
        print_fail("Nenhum save encontrado para este jogo.")
        sys.exit(1)

    selected_saves = select_saves(saves)
    if not selected_saves:
        print_fail("Nenhum save selecionado.")
        sys.exit(1)

    print_ok(f"{len(selected_saves)} save(s) selecionado(s).")

    destinations = select_destinations()
    if not destinations:
        print_fail("Nenhum destino selecionado.")
        sys.exit(1)

    print_ok(f"Destinos: {', '.join(destinations)}")

    if not sync_to_repo(selected_saves, saves_repo_path):
        print_fail("Falha ao sincronizar saves para o repositório local.")
        sys.exit(1)

    timestamp = get_timestamp()

    for dest_name in destinations:
        configure_destination(dest_name)

        saver = None
        if dest_name == "GitHub":
            from src.savers.github_saver import GitHubSaver
            saver = GitHubSaver()
        elif dest_name == "Google Drive":
            from src.savers.googledrive_saver import GoogleDriveSaver
            saver = GoogleDriveSaver()
        elif dest_name == "Telegram":
            from src.savers.telegram_saver import TelegramSaver
            saver = TelegramSaver()

        if not saver:
            print_fail(f"Destino inválido: {dest_name}")
            continue

        all_files = []
        for save in selected_saves:
            if os.path.isdir(save.path):
                all_files.append(save.path)
            else:
                all_files.append(save.path)

        metadata = {
            "repo_path": saves_repo_path,
            "save_dir": game_choice,
            "game": selected_saves[0].game,
            "timestamp": timestamp,
        }

        print(f"\n  [{saver.name()}] Iniciando backup...")
        success = saver.save(all_files, metadata)

        if success:
            print_ok(f"Backup para {saver.name()} concluído!")
        else:
            print_fail(f"Backup para {saver.name()} falhou.")

    print()
    from src.console.menu import print_banner
    print_banner()
    print(f"  {cfg.Fore.GREEN}Processo finalizado!{cfg.Style.RESET_ALL} Seus saves estão seguros.")
    print()


def _cli_play_minecraft(saves_repo_path):
    from src.console.menu import (
        print_banner, print_step, print_ok, print_fail, print_info,
        detect_launchers_menu, sync_worlds_to_launcher, sync_worlds_to_repo,
        select_destinations, configure_destination, get_timestamp,
    )

    print_banner()

    print_info("Detectando launcher Minecraft...")
    launcher_info = detect_launchers_menu()
    if not launcher_info:
        sys.exit(1)

    print()
    print_step(1, 4, "Preparando ambiente...")
    print_ok(f"Launcher: {launcher_info['name']}")
    print_info(f"Game dir: {launcher_info['game_dir']}")

    print()
    print_step(2, 4, "Sincronizando saves do GitHub para o repositório local...")
    from src.savers.github_saver import GitHubSaver
    gh_saver = GitHubSaver()
    has_github_config = bool(cfg.get("github.repo_url") and cfg.get("github.token"))
    if has_github_config:
        gh_saver.pull(saves_repo_path)

    print()
    print_step(3, 4, "Copiando saves do repositório para o launcher...")
    sync_worlds_to_launcher(launcher_info, saves_repo_path)

    from src.launcher.minecraft_launcher import launch_and_monitor

    print()
    print(f"  {'=' * 50}")
    print(f"  Iniciando {launcher_info['name']}...")
    print(f"  Jogue normalmente. Quando fechar, os saves serão salvos.")
    print(f"  {'=' * 50}")
    print()

    launch_and_monitor(
        launcher_info["launcher"],
        pre_launch_callback=None,
        post_exit_callback=lambda: _after_game_exit(
            launcher_info, saves_repo_path, gh_saver, has_github_config
        ),
    )

    print()
    print_banner()
    print(f"  {cfg.Fore.GREEN}Ciclo concluído! Seus saves estão seguros.{cfg.Style.RESET_ALL}")
    print()


def _after_game_exit(launcher_info, saves_repo_path, gh_saver, has_github_config):
    from src.console.menu import (
        print_step, print_ok, print_fail, print_info, get_timestamp,
        sync_worlds_to_repo, select_destinations, configure_destination,
    )
    from src.utils import config as cfg

    print()
    print_step(4, 4, "Sincronizando saves após o jogo...")

    print_info("Copiando saves do launcher para o repositório local...")
    if not sync_worlds_to_repo(launcher_info, saves_repo_path):
        print_fail("Falha ao copiar saves do launcher.")
        return

    timestamp = get_timestamp()

    if has_github_config:
        print()
        print_info("Enviando para GitHub...")
        all_files = [os.path.join(saves_repo_path, "Minecraft", "saves")]
        metadata = {
            "repo_path": saves_repo_path,
            "save_dir": "Minecraft",
            "game": "Minecraft",
            "timestamp": timestamp,
        }
        gh_saver.save(all_files, metadata)

    destinations = select_destinations()
    for dest_name in destinations:
        if dest_name == "GitHub":
            continue

        configure_destination(dest_name)

        saver = None
        if dest_name == "Google Drive":
            from src.savers.googledrive_saver import GoogleDriveSaver
            saver = GoogleDriveSaver()
        elif dest_name == "Telegram":
            from src.savers.telegram_saver import TelegramSaver
            saver = TelegramSaver()

        if not saver:
            continue

        all_files = [os.path.join(saves_repo_path, "Minecraft")]
        metadata = {
            "repo_path": saves_repo_path,
            "save_dir": "Minecraft",
            "game": "Minecraft",
            "timestamp": timestamp,
        }
        print(f"\n  [{saver.name()}] Iniciando backup...")
        success = saver.save(all_files, metadata)
        if success:
            print_ok(f"Backup para {saver.name()} concluído!")
        else:
            print_fail(f"Backup para {saver.name()} falhou.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Operação cancelada pelo usuário.")
        sys.exit(0)
