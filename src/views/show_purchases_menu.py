from rich.panel import Panel
from views.header import show_header
from utils.clear_screen import clear_screen

def show_purchases_menu(console, options):
  
    # Limpa a tela toda vez que o menu é exibido
    clear_screen()

    # Exibe o título do menu dentro de um painel
    show_header()

    # Título do menu de opções (fora do painel, com fundo verde)
    menu_title = f'[bold white on green]Movimentações de Estoque[/bold white on green]'

    # Criação das opções numeradas (alinhadas à esquerda e entre colchetes)
    menu_options = "\n".join([f"({i + 1}) {option}" for i, option in enumerate(options)])

    browser_options = "\n[bold blue](r) Voltar[/bold blue] [bold red](q) Sair [/bold red]"

    # Exibe o painel com o menu numerado, alinhado à esquerda
    panel = Panel(f"{menu_options}\n{browser_options}", title=menu_title, style="bold", expand=False, padding=(1, 2))
    console.print(panel)
