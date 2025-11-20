from project_client import Client

# Intenta registrar un usuario
name="Alexander"
password=""
role="paciente"
id=1111
url="http://localhost:80"

project_client=Client(url)

#print(project_client.registerUser(name,id,role,password))


# Inicia sesión con usuario
#print(project_client.openSession(id,password))


# Obtiene la lista de médicos
print(project_client.getDoctorsList(id))


#date="2025-11-06"
#time="3:00"

#doctorid=4444


# Solicita una cita con un médico
#print(project_client.addAppointment(doctorid,id,date,time))

print(project_client.getDoctorIP(id))


#print(project_client.getAppointmentsList(ii))
# Cierra sesión con usuario
#print(project_client.closeSession(id))
