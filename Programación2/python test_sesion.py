import unittest
from funcion import iniseccion

def openSession(user_id, password, ip):
    return iniseccion(user_id, password, ip)

class TestOpenSession(unittest.TestCase):

    def test_sesion_exitosa(self):
        resultado = openSession("777", "clave777", "192.168.1.1")
        self.assertEqual(resultado, "sesion iniciada")

    def test_usuario_no_encontrado(self):
        resultado = openSession("noexiste", "clave", "192.168.1.2")
        self.assertEqual(resultado, "Usuario no encontrado.")

    def test_clave_incorrecta(self):
        resultado = openSession("888", "clave_incorrecta", "192.168.1.3")
        self.assertEqual(resultado, "Clave no correcta.")

if __name__ == '__main__':
    unittest.main()