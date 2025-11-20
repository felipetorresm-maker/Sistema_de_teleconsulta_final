import unittest
from funcion import filtrar_doctores

def doctorsList(user_id):
    return filtrar_doctores(user_id)

class TestDoctorsList(unittest.TestCase):

    def test_lista_doctores_valida(self):
        resultado = doctorsList("777")
        self.assertIsInstance(resultado, list)
        self.assertTrue(all(isinstance(nombre, str) for nombre in resultado))

    def test_usuario_no_encontrado(self):
        resultado = doctorsList("noexiste")
        self.assertEqual(resultado, "El usuario no es un paciente con sesión abierta.")

    def test_base_datos_inexistente(self):
        import os
        if os.path.exists("datos.json"):
            os.rename("datos.json", "datos_temp.json")

        try:
            resultado = doctorsList("0000")
            self.assertEqual(resultado, "Base de datos no encontrada")
        finally:
            if os.path.exists("datos_temp.json"):
                os.rename("datos_temp.json", "datos.json")

if __name__ == '__main__':
    unittest.main()