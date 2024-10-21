import logging
logging.basicConfig(level=logging.INFO)
from src.repositories.repos_users import RepositoryUserManager

class ServiceUserManager:
    def __init__(self, connection):
        self.conn = connection
        self.repos_user_manager = RepositoryUserManager(self.conn)
        self.class_name = type(self).__name__

    def get_user_id(self, value, by='Username'):
        """Obtém o ID de usuário pelos campos Username, Name ou Email."""
        valid_fields = ['Name', 'Username', 'Email']
        for i, field in enumerate(valid_fields):
            if field == by:
                user = {tuple[i+1]: tuple[0] for tuple in self.repos_user_manager.search_user(by, value)}
                break
        return user.get(value)

    def create_user(self, user_obj):
        """Cria um novo usuário."""
        try:
            name = user_obj.name
            username = user_obj.username
            email = user_obj.email
            password = user_obj.password

            sucess = self.repos_user_manager.create(name, username, email, password)
            if sucess:
                logging.info(f'{self.class_name}: Usuário {username} criado com sucesso.')

        except Exception as e:
            print(f'{self.class_name}: Erro ao criar usuário. Erro: {e}.')
        
        return sucess

    def edit_user(self, field, current_value, new_value):
        """Edita um campo específico do usuário."""
        # Define os campos válidos
        valid_fields = ['Name', 'Username', 'Email']
        try:
            # Valida o campo informado
            if not field in valid_fields:
                logging.info(f'{self.class_name}: Nome do campo é inválido.')
                return False
            
            # Obtém o ID do usuário pelo campo fornecido
            user_id = self.get_user_id(current_value, by=field)
       
            if not user_id:
                logging.info(f'{self.class_name}: ID do usuário não localizado.')
                return False
            
            # Atualiza o campo
            sucess = self.repos_user_manager.update(user_id, field, new_value)
            if sucess:
                logging.info(f'{self.class_name}: Campo {field} do usuário {new_value} foi atualizado com sucesso.')
            else:
                logging.info(f'{self.class_name}: Campo {field} do usuário {current_value}) não atualizado.')

        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao atualizar campo {field} do usuário {field}. Erro: {e}.')
            
        return sucess

    def search_users(self, field='', value='', all=True):
        """Localizar usuário(s) de acordo com critério escolhido."""
        try:
            # Busca pelo campo específico
            if not all:
                result = self.repos_user_manager.search_user(field, value)
                if result:
                    logging.info(f'{len(result)} Usuário(s) localizado(s).')
                else:
                    logging.info(f'{self.class_name}: Usuário não localizado.')
            # Lista todos os usuários
            else:
                result = self.repos_user_manager.list()
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao localizar usuário(s). Erro: {e}.')
        
        return result
    
    def delete_user(self, user, by='Username'):
        """Deletar um usuário pelo atributo de usuário."""
        try:
            # Obtém o ID do usuário.
            user_id = self.get_user_id(user, by=by)
            if user_id:
                # Deleta o usuário
                self.repos_user_manager.delete(user_id)
                logging.info(f'{self.class_name}: Usuário {user} deletado com sucesso.')
            else:
                logging.info(f'{self.class_name}: Usuário {user} não deletado. ID não localizado.')
        except Exception as e:
            logging.error(f'{self.class_name}: Erro ao deletar usuário. Erro: {e}.')
        
        return True