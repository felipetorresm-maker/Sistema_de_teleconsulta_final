import unittest
import json
from funcion import crear_consulta

def addAppointment(user_id, doctor_id, date, time):
    return crear_consulta(user_id, doctor_id, date, time)

class TestAddAppointment(unittest.TestCase):

    def test_agendar_consulta(self):
        resultado = addAppointment("5", "dr001", "2025-11-10", "09:00")
        self.assertEqual(resultado, "Consulta agendada.")

    def test_verificar_registro_en_archivo(self):
        encontrado = False
        with open("consultas.json", "r") as f:
            for line in f:
                cita = json.loads(line)
                if (
                    cita["identificacion"] == "555" and
                    cita["doctor"] == "dr001" and
                    cita["fecha"] == "2025-11-10" and
                    cita["hora"] == "09:00"
                ):
                    encontrado = True
                    break
        self.assertTrue(encontrado)

if __name__ == '__main__':
    unittest.main()