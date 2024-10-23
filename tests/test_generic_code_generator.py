import syspath
syspath.set_src_path()
import datetime
import unittest
from src.utils.generic_code_generator import generate_code

class TestGenerateCode(unittest.TestCase):
    def test_generate_code_new_month(self):
        # Testa a geração de código em um mês diferente
        registers = ['REG2402000001', 'REG2402000002']
        code = generate_code(registers, 'REG')
        now = datetime.datetime.now()
        expected_code = f'REG{now.strftime("%y")}{now.strftime("%m")}000001'
        self.assertEqual(code, expected_code)

    def test_generate_code_same_month(self):
        # Testa a geração de código no mesmo mês
        now = datetime.datetime.now()
        registers = [
            f'REG{now.strftime("%y")}{now.strftime("%m")}000001',
            f'REG{now.strftime("%y")}{now.strftime("%m")}000002'
        ]
        code = generate_code(registers, 'REG')
        expected_code = f'REG{now.strftime("%y")}{now.strftime("%m")}000003'
        self.assertEqual(code, expected_code)

    def test_generate_code_empty_registers(self):
        # Testa a geração de código com registros vazios
        now = datetime.datetime.now()
        registers = []
        code = generate_code(registers, 'REG')
        expected_code = f'REG{now.strftime("%y")}{now.strftime("%m")}000001'
        self.assertEqual(code, expected_code)

if __name__ == '__main__':
    unittest.main()