import os

def get_db_path():
    """
    Returns the path to the SQLite database file.

    The database file is located in the 'data' directory 
    and is named 'sge.db'.
    """
    # Get the directory project
    cur_dir = os.path.abspath(os.curdir)

    # Build database path
    db_path = cur_dir + '/data/sge.db' 

    return db_path