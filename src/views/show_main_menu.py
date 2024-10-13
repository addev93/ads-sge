
from rich.panel import Panel
from views.header import show_header
from utils.clear_screen import clear_screen   
 
def show_main_menu(console, options):
    # Limpa a tela
    clear_screen()

    # Exibe o título do menu dentro de um painel
    show_header()

    # Criação do painel do cabeçalho do menu
    menu_title = f'[bold white on green]Menu Principal[/bold white on green]'

    # Criação das opções numeradas (alinhadas à esquerda)
    menu_options = "\n".join([f"({i + 1}) {option[0]}" for i, option in enumerate(options)])

    # Opção "Sair" com comandos entre colchetes
    browser_options = "\n[bold red](q) Sair[/bold red]"

    # Exibe o painel com o menu numerado, alinhado à esquerda
    panel_content = f'{menu_options}\n{browser_options}'     
    panel = Panel(panel_content, title=menu_title, style="bold white", expand=False, padding=(1, 2))
    console.print(panel)
