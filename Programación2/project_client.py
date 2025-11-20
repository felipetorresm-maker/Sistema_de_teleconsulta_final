# Instalar el módulo requests haciendo desde una terminal: pip install requests
import requests
import socket

class Client:
    def __init__(self, url):
        self.url = url

    # Método para registrar usuario
    def addAppointment(self,id,doctorid,date,time):    
        response=requests.post(self.url+'/addappointment',data=f'id={id}&doctorid={doctorid}&date={date}&time={time}')
        return response.content.decode('utf-8')


    # Función para registrar usuario
    def registerUser(self,name,id,role,password):    
        response=requests.post(self.url+'/register',data=f'name={name}&id={id}&role={role}&password={password}')
        return response.content.decode('utf-8')

    # Funciónn para abrir una sesión
    def openSession(self,id,password):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)    
        response=requests.put(self.url+'/login',data=f'id={id}&password={password}&ip={IPAddr}')
        return response.content.decode('utf-8')

    # Función para cerrar una sesión
    def closeSession(self,id):    
        response=requests.put(self.url+'/logout',data=f'id={id}')
        return response.content.decode('utf-8')

    # Función para obtener la lista de citas del médico
    def getAppointmentsList(self,id):    
        response=requests.get(self.url+'/listappointments',data=f'id={id}')
        return response.content.decode('utf-8')


    # Función para obtener la lista de médicos
    def getDoctorsList(self,id):    
        response=requests.get(self.url+'/listdoctors',data=f'id={id}')
        return response.content.decode('utf-8')
    
    # Función la IP del médicot
    def getDoctorIP(self,id):    
        response=requests.get(self.url+'/getdoctorip',data=f'id={id}')
        return response.content.decode('utf-8')

