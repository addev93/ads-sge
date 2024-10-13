from rich.prompt import Prompt
from views.show_management_menu import show_management_menu
from handlers.handler_management_menu_gen import management_menu_gen_handler

def management_menu_handler(console):
    
    options = ["Produtos", "Categorias", "Fornecedores", "Usuarios"]

    while True:  # Loop para manter o menu ativo até que se decida sair

        show_management_menu(console, options)

        """Processo de Captura de Dados"""
        # Solicita uma opção
        choice = Prompt.ask(f"[bold]Escolha uma opção[/bold]")
        
        # Valida a escolha
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            
            # Chama o menu correspondente
            next_action = management_menu_gen_handler(console, options[int(choice) - 1])

            # Decide o que fazer de acordo com o retorno da função chamada
            if next_action == 'back':  
                continue  
            if next_action == 'main':
                return 'back'
            elif next_action == -1:
                return -1
        
        elif choice.lower() == "r":
            return 'back'
        
        elif choice.lower() == "q":      
            return -1