from utils import syspath
syspath.set_src_path()
from rich.console import Console
from utils.db_generator import db_generator
from utils.clear_screen import clear_screen
from handlers.handler_main_menu import main_menu_handler

console = Console()

def main():

    # Create the database (if not exists)
    db_generator()

    while True:
        if main_menu_handler(console) == -1:
            clear_screen()
            console.print("Saindo... Sistema encerrado.", style="bold red")
            break

if __name__ == "__main__":
    main()