import sys
import os

def set_src_path():
    
    # Obter o diretório do projeto
    cur_dir = os.path.abspath(os.curdir)
 
    # Dividir o caminho em uma lista
    lista = cur_dir.split('/')

    # Construir root_dir
    root_dir = '/'.join(lista) + '/'  # Usar join para construir o caminho

    # Adicionar root_dir ao sys.path na posição 0
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
