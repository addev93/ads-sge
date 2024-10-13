from rich.panel import Panel
from utils.clear_screen import clear_screen
from views.header import show_header

def show_new_product_register(console, data):
    
    # Limpa a tela do console
    clear_screen()
    
    # Exibe o título do menu dentro de um painel
    show_header()

    # Título do painel
    title = '[bold white on green]Cadastrar Novo Produto[/bold white on green]'

    # Adiciona linhas à tabela com os campos e seus valores
    fields = '\n'.join(f'{tuple[2].capitalize()}: {tuple[0]}' for tuple in data.values())

    # Opções de navegação
    browser_options = '[bold yellow](f) Finalizar[/bold yellow] [bold red](q) Encerrar [/bold red] [bold green]\n(c) Confirmar[/bold green]'
    
    # Cria um painel que contém a tabela e as opções de navegação
    panel_content = f'{fields}\n\n{browser_options}'
    panel = Panel(panel_content, title=title, style='bold', expand=False, padding=(1, 2))

    # Exibe o painel combinado
    console.print(panel)
        