from rich.prompt import Prompt
from models.model_product import Product
from services.service_search_product import search_product_service

import time

def product_search_handler(console):
    
    options = ['Pesquisar por código', 'Pesquisar por descrição', 'Listar tudo']
   
    while True:
        
        """Implementar função de menu de opções"""
        # show_search_product_menu(console, [opt[0] for opt in options])

        """Captura de Entrada de Dados"""
        # Solicita uma opção
        choice = Prompt.ask(f"[bold]Escolha uma opção[/bold]")
        
        # Valida a escolha
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            
            if int(choice) == 1:
                code = Prompt.ask(f"[bold]Digite o código[/bold]")
                data = search_product_service(int(choice), code)
            elif int(choice) == 2:
                desc = Prompt.ask(f"[bold]Digite a descrição[/bold]")
                data = search_product_service(int(choice), desc)
            elif int(choice) == 3:
                data = search_product_service(None)

        for row in data:
            print(row)
            time.sleep(5)
        #     # Decide o que fazer de acordo com o retorno da função chamada
        #     if data == 'back':  
        #         continue  
        #     if data == 'main':
        #         return 'back'
        #     elif data == -1:
        #         return -1
        
        # elif choice.lower() == "r":
        #     return 'back'
        
        # elif choice.lower() == "q":      
        #     return -1