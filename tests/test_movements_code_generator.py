import syspath
syspath.set_src_path()
import datetime
import unittest
from src.utils.movement_code_generator import generate_movement_code

class TestGenerateMovementCode(unittest.TestCase):
    def test_generate_movement_code(self):
        # Obtém a data atual para simular movimentações
        now = datetime.datetime.now()
        year = now.strftime('%y')  # Últimos dois dígitos do ano
        month = now.strftime('%m')  # Mês no formato "00"
        
        # Simula movimentações existentes para o mês e ano atuais
        movements = [
            ('1', f'MOV{year}{month}0001', '1', 10, 'Entrada', 'INV001'),
            ('2', f'MOV{year}{month}0002', '1', 5, 'Saída', 'INV002'),
        ]

        # Gera o código de movimentação
        generated_code = generate_movement_code(movements)

        # Verifica se o código gerado está no formato correto
        self.assertTrue(generated_code.startswith(f'MOV{year}{month}'))
        self.assertEqual(len(generated_code), 13)  # Verifica o comprimento total

        # Verifica se a parte sequencial é '0003'
        sequence_number = int(generated_code[6:])  # Obtém o número sequencial
        self.assertEqual(sequence_number, 3)  # Deveria ser 3, pois já existem duas movimentações

if __name__ == '__main__':
    unittest.main()