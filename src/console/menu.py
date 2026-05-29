import os
import shutil
import subprocess
import time
from datetime import datetime
from typing import List, Optional

from src.games.base import SaveEntry
from src.utils import config
from src.utils.file_utils import human_size

try:
    from colorama import init, Fore, Style
    init()
except ImportError:
    class Fore:
        GREEN = ""
        YELLOW = ""
        CYAN = ""
        RED = ""
        BLUE = ""
        MAGENTA = ""
    class Style:
        BRIGHT = ""
        RESET_ALL = ""


def print_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
   ╔══════════════════════════════════════════════╗
   ║          SYSTEM SAVE ETERNAL - SSE           ║
   ║     Backup Inteligente de Saves de Jogos     ║
   ╚══════════════════════════════════════════════╝
{Style.RESET_ALL}
    """
    print(banner)


def print_step(step: int, total: int, msg: str):
    print(f"\n{Fore.YELLOW}[{step}/{total}]{Style.RESET_ALL} {msg}")


def print_ok(msg: str):
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {msg}")


def print_fail(msg: str):
    print(f"  {Fore.RED}✗{Style.RESET_ALL} {msg}")


def print_info(msg: str):
    print(f"  {Fore.CYAN}i{Style.RESET_ALL} {msg}")


def print_transparency(action: str, details: list):
    print(f"\n  {Fore.YELLOW}{'═' * 52}{Style.RESET_ALL}")
    print(f"  {Fore.RED}⚠{Style.RESET_ALL} {Fore.YELLOW}SSE — {action}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'═' * 52}{Style.RESET_ALL}")
    for line in details:
        print(f"    {Fore.CYAN}•{Style.RESET_ALL} {line}")
    print(f"  {Fore.YELLOW}{'═' * 52}{Style.RESET_ALL}")
    print()


def confirm_action(prompt: str = "Deseja continuar? (s/N): ") -> bool:
    resp = input(f"  {Fore.CYAN}›{Style.RESET_ALL} {prompt}").strip().lower()
    return resp == "s"


def select_game() -> str:
    print()
    print(f"  {Fore.YELLOW}O que você deseja fazer?{Style.RESET_ALL}")
    print()
    print("  1) Fazer backup de saves (Minecraft / Pokémon)")
    print("  2) Jogar Minecraft com sincronização automática")
    print()
    while True:
        choice = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Escolha (1 ou 2): ").strip()
        if choice == "1":
            return _select_backup_game()
        elif choice == "2":
            return "play_minecraft"
        print_fail("Opção inválida. Digite 1 ou 2.")


def _select_backup_game() -> str:
    print_step(1, 3, "Selecione o jogo para fazer backup:")
    print()
    print("  1) Minecraft")
    print("  2) Pokémon Black & White")
    print()
    while True:
        choice = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Escolha (1 ou 2): ").strip()
        if choice == "1":
            return "minecraft"
        elif choice == "2":
            return "pokemon"
        print_fail("Opção inválida. Digite 1 ou 2.")


def select_saves(saves: List[SaveEntry]) -> List[SaveEntry]:
    if not saves:
        print_fail("Nenhum save encontrado!")
        return []

    print(f"\n  {Fore.CYAN}Saves encontrados:{Style.RESET_ALL}")
    print()
    for i, save in enumerate(saves, 1):
        size_str = human_size(save.size_bytes)
        print(f"  [{i:2d}] {Fore.GREEN}{save.name}{Style.RESET_ALL}")
        print(f"       Game: {save.game}")
        print(f"       Path: {save.path}")
        if save.platform:
            print(f"       Plataforma: {save.platform}")
        print(f"       Tamanho: {size_str}")
        print()

    print(f"  {Fore.YELLOW}Use os números separados por vírgula.{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Ex: 1,3,5  ou  'all' para todos  ou ENTER para cancelar{Style.RESET_ALL}")
    print()
    while True:
        choice = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Selecione: ").strip().lower()
        if not choice:
            return []
        if choice == "all":
            return saves[:]
        try:
            indices = [int(x.strip()) for x in choice.split(",")]
            selected = []
            for idx in indices:
                if 1 <= idx <= len(saves):
                    selected.append(saves[idx - 1])
            if selected:
                return selected
        except ValueError:
            pass
        print_fail("Entrada inválida. Use números separados por vírgula.")


def select_destinations() -> List[str]:
    print_step(2, 3, "Escolha o(s) destino(s) do backup:")
    print()
    print("  Destinos disponíveis:")
    dests = {
        "1": "GitHub",
        "2": "Google Drive",
        "3": "Telegram"
    }
    for k, v in dests.items():
        print(f"  [{k}] {v}")
    print()
    print(f"  {Fore.YELLOW}Use os números separados por vírgula.{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Ex: 1,3  (backup no GitHub E no Telegram){Style.RESET_ALL}")
    print()
    while True:
        choice = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Selecione: ").strip()
        if not choice:
            return []
        try:
            indices = [x.strip() for x in choice.split(",")]
            selected = []
            for idx in indices:
                if idx in dests:
                    selected.append(dests[idx])
            if selected:
                return selected
        except ValueError:
            pass
        print_fail("Entrada inválida.")


def configure_destination(dest_name: str):
    if dest_name == "GitHub":
        configure_github()
    elif dest_name == "Google Drive":
        configure_google_drive()
    elif dest_name == "Telegram":
        configure_telegram()


def configure_github():
    print_transparency("Configuração GitHub", [
        "O SSE irá usar um token de acesso para enviar saves ao seu repositório.",
        "O token será armazenado em ~/.config/sse/config.json (apenas local).",
        "Escopo necessário: 'repo' (controle total de repositórios privados).",
        "Nunca compartilhe este token — ele dá acesso ao seu repositório.",
    ])
    if not confirm_action("Deseja configurar o GitHub? (s/N): "):
        print_info("Configuração do GitHub cancelada.")
        return
    print(f"\n  {Fore.CYAN}--- Configuração: GitHub ---{Style.RESET_ALL}")
    print()

    repo_url = config.get("github.repo_url", "")
    if repo_url:
        print_info(f"Repositório atual: {repo_url}")
        change = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Deseja alterar? (s/N): ").strip().lower()
        if change != "s":
            return

    print()
    print(f"  {Fore.YELLOW}Você já tem um repositório no GitHub para salvar os saves?{Style.RESET_ALL}")
    print("  1) Sim, já tenho um repositório")
    print("  2) Não, quero criar um novo")
    print()

    has_repo = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Escolha (1 ou 2): ").strip()

    if has_repo == "2":
        print()
        print(f"  {Fore.CYAN}--- Guia para criar repositório no GitHub ---{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Siga os passos abaixo:{Style.RESET_ALL}")
        print("  1. Acesse https://github.com/new")
        print("  2. Dê um nome ao repositório (ex: system-save-eternal-backup)")
        print("  3. Marque a opção 'Private' (repositório privado)")
        print("  4. NÃO marque 'Add a README file'")
        print("  5. Clique em 'Create repository'")
        print("  6. Copie a URL HTTPS do repositório criado")
        print()

    repo_url = input(f"  {Fore.CYAN}›{Style.RESET_ALL} URL do repositório GitHub: ").strip()
    if not repo_url:
        print_fail("URL não informada.")
        return

    print()
    print(f"  {Fore.CYAN}--- Token de Acesso ---{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Configure um Personal Access Token (PAT):{Style.RESET_ALL}")
    print("  Settings → Developer Settings → Personal Access Tokens → Tokens (classic)")
    print("  → Generate New Token → Marcar escopo: 'repo' → Generate")
    print()

    token = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Token de acesso: ").strip()
    if not token:
        print_fail("Token não informado.")
        return

    config.set_key("github.repo_url", repo_url)
    config.set_key("github.token", token)
    print_ok("GitHub configurado com sucesso!")


def configure_google_drive():
    print_transparency("Configuração Google Drive", [
        "O SSE irá autenticar com sua conta Google via OAuth 2.0.",
        "Será aberto um navegador para você autorizar o acesso.",
        "O SSE poderá criar pastas e fazer upload de arquivos no seu Drive.",
        "As credenciais serão armazenadas em ~/.config/sse/.",
        "Você pode revogar o acesso a qualquer momento em:",
        "  https://myaccount.google.com/permissions",
    ])
    if not confirm_action("Deseja configurar o Google Drive? (s/N): "):
        print_info("Configuração do Google Drive cancelada.")
        return
    print(f"\n  {Fore.CYAN}--- Configuração: Google Drive ---{Style.RESET_ALL}")
    print()
    print_info("Para usar o Google Drive, você precisa das credenciais da API do Google.")
    print(f"  {Fore.YELLOW}Passos:{Style.RESET_ALL}")
    print("  1. Acesse https://console.cloud.google.com/")
    print("  2. Crie um projeto e habilite a API 'Google Drive API'")
    print("  3. Crie credenciais → 'OAuth 2.0 Client IDs' → 'Desktop app'")
    print("  4. Baixe o JSON e cole os valores abaixo")
    print()

    client_id = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Client ID: ").strip()
    client_secret = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Client Secret: ").strip()

    if client_id and client_secret:
        config.set_key("google_drive.client_id", client_id)
        config.set_key("google_drive.client_secret", client_secret)
        print_ok("Google Drive configurado com sucesso!")
    else:
        print_fail("Credenciais não informadas.")


def configure_telegram():
    print_transparency("Configuração Telegram", [
        "O SSE usará a API MTProto do Telegram para enviar mensagens.",
        "Será necessário informar seu número de telefone e código de verificação.",
        "Os saves serão enviados para Saved Messages (ou chat específico).",
        "A sessão será salva em ~/.config/sse/telegram.session.",
        "Nunca compartilhe seu api_hash — ele é sua chave secreta.",
    ])
    if not confirm_action("Deseja configurar o Telegram? (s/N): "):
        print_info("Configuração do Telegram cancelada.")
        return
    print(f"\n  {Fore.CYAN}--- Configuração: Telegram ---{Style.RESET_ALL}")
    print()
    print_info("Para usar o Telegram, você precisa do API ID e API Hash.")
    print(f"  {Fore.YELLOW}Passos:{Style.RESET_ALL}")
    print("  1. Acesse https://my.telegram.org")
    print("  2. Faça login e vá em 'API development tools'")
    print("  3. Crie um novo aplicativo para obter api_id e api_hash")
    print()

    api_id_str = input(f"  {Fore.CYAN}›{Style.RESET_ALL} API ID: ").strip()
    api_hash = input(f"  {Fore.CYAN}›{Style.RESET_ALL} API Hash: ").strip()
    phone = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Telefone (com código do país, ex: +5511999999999): ").strip()

    if api_id_str and api_hash:
        config.set_key("telegram.api_id", int(api_id_str))
        config.set_key("telegram.api_hash", api_hash)
        config.set_key("telegram.phone", phone)

        chat_id = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Chat ID (opcional, ENTER para 'Saved Messages'): ").strip()
        if chat_id:
            config.set_key("telegram.chat_id", chat_id)

        print_ok("Telegram configurado com sucesso!")
    else:
        print_fail("API ID e API Hash são obrigatórios.")


def get_repo_path() -> Optional[str]:
    repo_path = config.get("save_repo_path", "")
    if not repo_path:
        print()
        print(f"  {Fore.YELLOW}Qual o caminho do repositório local de saves?{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Ex: /mnt/dados/System-Save-Eternal{Style.RESET_ALL}")
        repo_path = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Caminho: ").strip()
        if not repo_path:
            print_fail("Caminho não informado.")
            return None
        if not os.path.isdir(repo_path):
            print_fail(f"Diretório não encontrado: {repo_path}")
            return None
        config.set_key("save_repo_path", repo_path)
    return repo_path


def sync_to_repo(selected_saves: List[SaveEntry], repo_path: str) -> bool:
    total_size = sum(s.size_bytes for s in selected_saves)
    print_transparency("Cópia de Saves", [
        f"{len(selected_saves)} save(s) serão copiados para: {repo_path}",
        f"Tamanho total: {human_size(total_size)}",
        "Os saves originais NÃO serão modificados ou deletados.",
        "Apenas uma cópia será feita para o repositório local.",
    ])
    if not confirm_action("Confirmar cópia dos saves? (s/N): "):
        print_info("Operação cancelada.")
        return False
    print()
    print_step(3, 3, "Sincronizando saves para o repositório local...")

    for save in selected_saves:
        game_dir = save.game.replace(" ", "_").replace("(", "").replace(")", "")
        dest_dir = os.path.join(repo_path, game_dir, os.path.basename(save.path))

        try:
            os.makedirs(os.path.dirname(dest_dir), exist_ok=True)
            if os.path.isdir(save.path):
                if os.path.exists(dest_dir):
                    shutil.rmtree(dest_dir)
                shutil.copytree(save.path, dest_dir)
            else:
                shutil.copy2(save.path, dest_dir)
            print_ok(f"{save.name} → {dest_dir}")
        except Exception as e:
            print_fail(f"Erro ao copiar {save.name}: {e}")
            return False

    return True


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def detect_launchers_menu() -> Optional[dict]:
    from src.launcher.minecraft_launcher import detect_launchers

    launchers = detect_launchers()

    if not launchers:
        print_fail("Nenhum launcher Minecraft encontrado no sistema.")
        print_info("Tente configurar manualmente ou baixe um launcher primeiro.")
        print()
        manual = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Deseja configurar manualmente? (s/N): ").strip().lower()
        if manual == "s":
            return _manual_launcher_config()
        return None

    if len(launchers) == 1:
        l = launchers[0]
        print_ok(f"Launcher detectado: {l.icon} {l.name}")
        print_info(f"Binário: {l.binary_path}")
        return {
            "launcher": l,
            "name": l.name,
            "binary": l.binary_path,
            "game_dir": l.game_dir,
        }

    print()
    print(f"  {Fore.YELLOW}Múltiplos launchers detectados. Selecione um:{Style.RESET_ALL}")
    print()
    for i, l in enumerate(launchers, 1):
        print(f"  [{i}] {l.icon} {l.name}")
        print(f"       Binário: {l.binary_path}")
        if l.game_dir:
            print(f"       Game dir: {l.game_dir}")
        print()
    while True:
        choice = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Escolha (1-{len(launchers)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(launchers):
                l = launchers[idx]
                return {
                    "launcher": l,
                    "name": l.name,
                    "binary": l.binary_path,
                    "game_dir": l.game_dir,
                }
        except ValueError:
            pass
        print_fail("Opção inválida.")


def rsync_saves(from_dir: str, to_dir: str, desc: str = "") -> bool:
    if not os.path.isdir(from_dir) and not os.path.isdir(to_dir):
        print_fail(f"Diretório não encontrado: {from_dir if not os.path.isdir(from_dir) else to_dir}")
        return False

    os.makedirs(to_dir, exist_ok=True)

    try:
        result = subprocess.run(
            ["rsync", "-a", "--delete", "--quiet", from_dir + "/", to_dir + "/"],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            if desc:
                print_ok(f"{desc} sincronizado com sucesso")
            return True
        else:
            print_fail(f"Erro no rsync: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        try:
            import shutil
            if os.path.isdir(from_dir):
                if os.path.exists(to_dir):
                    shutil.rmtree(to_dir)
                shutil.copytree(from_dir, to_dir)
            if desc:
                print_ok(f"{desc} copiado com sucesso (sem rsync)")
            return True
        except Exception as e:
            print_fail(f"Erro ao copiar: {e}")
            return False
    except subprocess.TimeoutExpired:
        print_fail("Sincronização excedeu o tempo limite")
        return False
    except Exception as e:
        print_fail(f"Erro inesperado no rsync: {e}")
        return False


def sync_launcher_saves(launcher_info: dict, repo_path: str, direction: str, game_name: str = "Minecraft"):
    game_dir = launcher_info.get("game_dir", "")
    if not game_dir:
        print_fail("Diretório do jogo não encontrado para este launcher.")
        return False

    saves_src = os.path.join(game_dir, "saves")
    saves_dst = os.path.join(repo_path, game_name.replace(" ", "_"), "saves")

    if direction == "to_launcher":
        if not os.path.isdir(saves_dst):
            print_info("Nenhum save no repositório ainda. Iniciando com saves vazios.")
            return True
        return rsync_saves(saves_dst, saves_src, "Saves do repositório → Launcher")
    elif direction == "to_repo":
        if not os.path.isdir(saves_src):
            print_fail("Diretório de saves do launcher não encontrado.")
            return False
        return rsync_saves(saves_src, saves_dst, "Saves do Launcher → Repositório")
    return False


def sync_worlds_to_launcher(launcher_info: dict, repo_path: str):
    return sync_launcher_saves(launcher_info, repo_path, "to_launcher")


def sync_worlds_to_repo(launcher_info: dict, repo_path: str):
    return sync_launcher_saves(launcher_info, repo_path, "to_repo")


def _manual_launcher_config() -> Optional[dict]:
    from src.launcher.minecraft_launcher import LauncherInfo

    print()
    print(f"  {Fore.CYAN}--- Configuração Manual do Launcher ---{Style.RESET_ALL}")
    print()

    name = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Nome do launcher (ex: SKLauncher): ").strip()
    if not name:
        name = "Minecraft Launcher"

    binary = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Caminho completo do binário: ").strip()
    if not binary or not os.path.isfile(binary):
        print_fail("Binário não encontrado no caminho informado.")
        return None

    game_dir = input(f"  {Fore.CYAN}›{Style.RESET_ALL} Diretório do .minecraft (onde fica a pasta saves/): ").strip()
    game_dir = os.path.expanduser(game_dir)
    if not game_dir or not os.path.isdir(game_dir):
        print_fail("Diretório não encontrado.")
        return None

    launcher = LauncherInfo(
        name=name,
        binary_path=binary,
        game_dir=game_dir,
        icon="⚙️",
    )

    print_ok(f"Launcher configurado manualmente: {name}")
    return {
        "launcher": launcher,
        "name": name,
        "binary": binary,
        "game_dir": game_dir,
    }
