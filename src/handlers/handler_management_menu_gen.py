from rich.panel import Panel
from rich.prompt import Prompt
from views.show_product_register_view import show_product_register_view
from handlers.handler_product_register import product_register_handler
from handlers.handler_product_search import product_search_handler

def management_menu_gen_handler(console, text):

    options = ['Cadastrar', 'Editar', 'Localizar', 'Deletar']

    while True:

        show_product_register_view(console, options, text)

        # Captura de entrada
        choice = Prompt.ask(f"[bold]Escolha uma opção[/bold]")

        if choice == "1":  # Cadastrar
            next_action = product_register_handler(console)
            if next_action == 'back':
                continue
            elif next_action == -1:
                return -1
        
        elif choice == "2":  # Editar
            pass
        
        elif choice == "3":  # Listar
            next_action = product_search_handler(console)
            
        elif choice == "4":  # Localizar
            pass
        
        elif choice.lower() == "r":  # "r" para voltar
            return 'back'

        elif choice == "m":  # "m" para menu principal
            return 'main'
        
        elif choice.lower() == "q":  # "q" para sair
            return -1  # Encerra o programa


