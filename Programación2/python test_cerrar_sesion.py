import unittest
from funcion import closession

def closeSession(user_id):
    return closession(user_id)

class TestCloseSession(unittest.TestCase):

    def test_cierre_exitoso(self):
        resultado = closeSession("888")
        self.assertEqual(resultado, "sesion cerrada")

    def test_usuario_no_encontrado(self):
        resultado = closeSession("noexiste")
        self.assertEqual(resultado, "Usuario no encontrado.")

if __name__ == '__main__':
    unittest.main()