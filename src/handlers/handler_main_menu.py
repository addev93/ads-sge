
from rich.prompt import Prompt
from handlers.handler_management_menu import management_menu_handler
from handlers.handler_movements_menu import movements_menu_handler
from handlers.handler_purchases_menu import purchases_menu_handler
from views.show_main_menu import show_main_menu

def main_menu_handler(console):
    
    options = [("Cadastros", management_menu_handler), ("Movimentações", movements_menu_handler), ("Compras", purchases_menu_handler)]

    while True:  # Loop para manter o menu ativo até que se decida sair
    
        # Print main menu
        show_main_menu(console, options)

        # Captura de entrada
        choice = Prompt.ask(f"[bold]Escolha uma opção[/bold]")

        if choice.lower() == 'q':
            return -1

        try:
            if 1 <= int(choice) <= len(options):  # Verifica se a escolha é válida
                index = int(choice) - 1
                for i, tuple in enumerate(options):
                    if index == i:
                        function = options[i][1]
                        next_action = function(console)
                        if next_action == 'back':
                            continue
                        elif next_action == -1:                     
                            return -1
            else:
                console.print("[bold red]Escolha inválida! Tente novamente.[/bold red]")
        except ValueError:
            console.print("[bold red]Entrada inválida! Por favor, digite um número ou 'q' para sair.[/bold red]")