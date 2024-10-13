from rich.prompt import Prompt
from views.show_purchases_menu import show_purchases_menu

def purchases_menu_handler(console):
    
    options = ([('Solicitar Compra',None), ('Aprovar Solicitações',None), ('Localizar',None), ('Editar',None), ('Deletar',None)])

    while True:  # Loop para manter o menu ativo até que se decida sair

        show_purchases_menu(console, [opt[0] for opt in options])

        """Processo de Captura de Dados"""
        # Solicita uma opção
        choice = Prompt.ask(f"[bold]Escolha uma opção[/bold]")
        
        # Valida a escolha
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            index = int(choice) - 1
            # Chama a funcao correspondente
            for i, tuple in enumerate(options):
                if i == index:
                    next_action = tuple[index] # << Implementar funções correspondentes ao menu

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