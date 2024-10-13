def table_exists(cursor, repository_name, table_name):
    """Verifica se a tabela existe no banco de dados."""
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    try:
        cursor.execute(query)
        return bool(cursor.fetchone())
    except Exception as e:
        print(f'{repository_name}: erro ao verificar existência da tabela {table_name}. Erro: {e}.')