from rich.panel import Panel
from utils.clear_screen import clear_screen
from views.header import show_header

def show_product_register_view(console, options, text):

    # Limpa a tela toda vez que o menu é exibido
    clear_screen()
    
    # Exibe o título do menu dentro de um painel
    show_header()

    # Título do menu de opções (fora do painel, com fundo verde)
    menu_title = f'[bold white on green]Gerenciar {text}[/bold white on green]'

    # Criação das opções numeradas (alinhadas à esquerda e entre colchetes)
    menu_options = "\n".join([f'({i + 1}) {option}' for i, option in enumerate(options)])

    text1 = f'[bold green](m) Menu principal [/bold green]'
    text2 = f'[bold blue](r) Voltar [/bold blue]'
    text3 = f'[bold red] (q) Sair [/bold red]'
    browser_options = f'\n{text1} {text2} {text3}'

    # Exibe o painel com o menu numerado, alinhado à esquerda
    panel= Panel(f'{menu_options}\n{browser_options}', title = menu_title, style='bold', expand=False, padding=(1, 2))
    console.print(panel)  # Alinhamento natural à esquerda, sem justificativa