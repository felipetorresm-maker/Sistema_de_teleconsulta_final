# users.py
from funcion import iniseccion, registro, crear_consulta, closession, filtrar_doctores,obtener_ip_doctor_activo
from datetime import date
from datetime import datetime
from funcion import citas_del_doctor
# This function must return the list of doctors, user with user_id must be a patient and have an open session
def doctorsList(user_id):
    # Include the code to return the list of doctors

    listOfDoctors=[] 

    listOfDoctors=filtrar_doctores(user_id)

    
    return listOfDoctors


def openSession(user_id, password, ip):
   
 # Include here the call of function you coded to open session. Store ip string in your field for open session.
    # Your function should return a message string.
    msg=iniseccion(user_id, password, ip)
    
    return msg
    
def closeSession(user_id):
    # Include here the call of function you coded to close session. Store an empty string in your field for open session.
    # Your function should return a message string.
    msg=closession(user_id)
    
    return msg

  

def registerUser(name, user_id, role, password):
    # Include here the call of function you coded to register users.
    # Your function should return a message string.

    msg=registro(user_id, name, password, role)

    return msg

def addAppointment(user_id, doctor_id, date, time):
    # Include here the call of function you coded to add appointments.
    # Your function should return a message string.
    msg= crear_consulta(user_id, doctor_id, date, time)
    
    return msg
def getDoctorIP(user_id):
    myDate = date.today()
    myTime = datetime.now().time()
   # msg = f"Mensaje de getDoctorIP para el usuario {user_id}, {myDate}, {myTime}\n"

    resultado = obtener_ip_doctor_activo(user_id)
    return  resultado 

def appointmentsList(doctor_id):
    # Include the code to return the list of appointments
    resultado = citas_del_doctor(doctor_id)
    
    
    return resultado