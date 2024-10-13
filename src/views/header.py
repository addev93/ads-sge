from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

console = Console()

def show_header():
    """Exibe o cabeçalho no terminal dentro de um painel, alinhado à esquerda."""
    header = Text("SGE - Sistema de Gestão de Estoque", style="bold white on blue")
    # Cabeçalho dentro de um painel, alinhado à esquerda
    console.print(Panel(header, style="bold white on blue", expand=False, padding=(0, 2)))
