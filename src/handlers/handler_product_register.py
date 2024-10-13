from rich.prompt import Prompt
from models.model_product import Product
from services.service_register_product import register_product_service
from views.show_new_product_register import show_new_product_register
import time

def product_register_handler(console):
    
    # Cria um objeto Product
    product = Product()
   
    while True:

        # Retornar um dicionario dos atributos do Produto
        data = product.attributes()
        
        # Print products fields
        show_new_product_register(console, data)

        """Processo de Captura de Dados"""          
        # Conta campos que já foram solicitados
        filled_fields = sum(1 for tuple in data.values() if tuple[1] == '*') < len(data)        
        
        if filled_fields:
            # Itera sobre os campos para solicitar entradas
            for attr, tuple in data.items():
                # tuple = getattr(product, attr)
                if 'f' in tuple[0]:  # Verifica se o usuário finalizou
                    return 'back'

                elif 'q' in tuple[0]:  # Verifica se o usuário deseja sair
                    return -1
                
                elif not tuple[0] and '*' in tuple[2]:  # Campo obrigatório
                    input_user = Prompt.ask(f'[bold]{tuple[2].capitalize()}[/bold]')
                    setattr(product, attr, (input_user, '*', tuple[2]))           
                    break

                elif '*' not in tuple[2] and not tuple[1]:  # Campo opcional e ainda nao solicitado
                    input_user = Prompt.ask(f'[bold]{tuple[2].capitalize()}[/bold]')
                    setattr(product, attr, (input_user, '*', tuple[2]))
                    break
        
        else:
            # Pergunta ao usuário para confirmar o cadastro
            choice = Prompt.ask(f'[bold]Confirmar cadastro (y/N)?[/bold]')

            if choice.lower() == 'y':

                # Chama a função para registrar a entrada no banco de dados
                register = register_product_service(product)
                
                if register:
                    product = Product()
                    continue
            else:
                print('Cadastro cancelado.')
                time.sleep(2)
                continue

# console = Console()
# cadastrar_produto(console)