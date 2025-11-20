import unittest
import json
from funcion import registro

def registerUser(name, user_id, role, password):
    return registro(user_id, name, password, role)

class TestRegisterUserBaseReal(unittest.TestCase):

    def test_usuario_nuevo(self):
        resultado = registerUser("Ana", "0000", "admin", "clave123")
        self.assertEqual(resultado, "registro exitoso")

    def test_usuario_existente(self):
        registerUser("Ana", "888", "admin", "clave123")
        resultado = registerUser("Ana", "888", "admin", "clave123")
        self.assertEqual(resultado, "ya existe")

    def test_ver_contenido_base(self):
        with open("datos.json", "r") as f:
            print("datos")
            for line in f:
                print(line.strip())

if __name__ == '__main__':
    unittest.main()