class Auth:
    def __init__(self, service_service_manager):
        self.user_manager = service_service_manager
        self.class_name = type(self).__name__

    def authenticator(self, user, password):

        try:
            # Cria um dicionário de usuario: senha
            users = {tuple[2]: tuple[4] for tuple in self.user_manager.search_users()}
            
            # Verifica a existência do usuário
            if user not in users:
                print('Nome de usuário não cadastrado.')
                return False

            # Verifica a senha
            sucess = users.get(user) == password

            if sucess:
                print(f'Usuário {user} autenticado com sucesso.')
                return {user:True}
            else:
                return False
        except Exception as e:
            print('{self.class_name}: Erro ao autenticar usuário. Erro: {e}.')
            return None