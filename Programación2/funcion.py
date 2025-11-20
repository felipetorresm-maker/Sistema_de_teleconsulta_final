import json


def iniseccion(identificacion, password, ip):
    revision = []
    try:
        with open('datos.json', 'r') as file:
            for line in file:
                revision.append(json.loads(line))
    except FileNotFoundError:
        return "Base de datos no encontrada"

    usuario_encontrado = None
    for usuario in revision:
        if usuario["identificacion"] == identificacion and usuario["password"] == password:
            usuario_encontrado = usuario
            break

    if usuario_encontrado:
        # Actualizar estado con la IP
        usuario_encontrado["estado"] = ip

        # Guardar cambios en el archivo
        with open('datos.json', 'w') as file:
            for usuario in revision:
                file.write(json.dumps(usuario) + '\n')

        # Retornar rol para que la interfaz sepa si es médico o paciente
        return usuario_encontrado["rol"]
    else:
        return "Identificación o clave incorrecta."
def crear_consulta(identificacion, doctor_id,date,time):

    consulta = {
            "identificacion": identificacion,
            "fecha": date,
            "hora": time,
            "doctor": doctor_id
        }

    with open('consultas.json', 'a') as file:
            file.write(json.dumps(consulta) + '\n')

    return "Consulta agendada."
    
def registro(identificacion,name,password,rol):
    
    datos = []

    try:
        with open('datos.json', 'r') as file:
            for line in file:
                datos.append(json.loads(line))
    except FileNotFoundError:
            with open('datos.json', 'w') as f:
               pass


    with open('datos.json', 'a') as file:
        existe_identificacion = False
        for i in datos:
            if i["identificacion"] == identificacion:
                existe_identificacion = True
                break

        if existe_identificacion:
            return "ya existe"
        else:
            try:
                registro = {
                    "identificacion": identificacion,
                    "name": name,
                    "password": password,
                    "rol": rol,
                    "estado": "registrado"
                }

                datos.append(registro)
                file.write(json.dumps(registro) + "\n")
                
            except:
                return "hay un error"
            return "registro exitoso"
    

def closession(identificacion):
    revision = []
    try:
        with open('datos.json', 'r') as file:
            for line in file:
                revision.append(json.loads(line))
    except FileNotFoundError:
        return "Base de datos no encontrada"

    existe_identificacion = False
    for i in revision:
        if i["identificacion"] == identificacion:
            existe_identificacion = True
            break

    if existe_identificacion:
        estado = "inactivo"

        
        actualizado = False
        for i in revision:
            if i["identificacion"] == identificacion:
                i["estado"] = estado
                actualizado = i
                break

        if actualizado:
            with open('datos.json', 'w') as file:
                for usuario in revision:
                    file.write(json.dumps(usuario) + '\n')
                return "sesion cerrada"
            


def filtrar_doctores(user_id):
    revision = []
    try:
        with open('datos.json', 'r') as file:
            for line in file:
                revision.append(json.loads(line))
    except FileNotFoundError:
        return "Base de datos no encontrada"

    for i in revision:
        if i["identificacion"] == user_id:
            break
    else:
        return "Identificación no encontrada"

    # Solo devolver los identificadores de los doctores
    lista_doctores = [
        i["identificacion"]
        for i in revision if i["rol"] == "Medico"
    ]
    return lista_doctores




import json

def obtener_ip_doctor_activo(user_id):
    doctor_nombre = None

    # Paso 1: Buscar el nombre del doctor en 'consultas.json'
    try:
        with open('consultas.json', 'r') as file:
            for linea in file:
                try:
                    consulta = json.loads(linea.strip())
                    if consulta.get('identificacion') == user_id:
                        doctor_nombre = consulta.get('doctor')
                        break
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return "Error: El archivo 'consultas.json' no fue encontrado."

    if not doctor_nombre:
        return "No se encontró ninguna consulta para ese usuario."

    # Paso 2: Buscar al doctor en 'datos.json'
    try:
        with open('datos.json', 'r') as file:
            doctores = []
            for linea in file:
                try:
                    persona = json.loads(linea.strip())
                    if persona.get('rol') == 'Medico':
                        doctores.append(persona)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return "Error: El archivo 'datos.json' no fue encontrado."

    # Primero intentamos con el doctor asignado
    for doctor in doctores:
        if doctor.get('identificacion') == doctor_nombre:
            estado = doctor.get('estado')
            if estado and estado.lower() != "inactivo":
                return estado  # aquí 'estado' es la IP
            break


    return "No se encontró ningún doctor activo."

def citas_del_doctor(nombre_doctor):
    citas = []

    try:
        with open('consultas.json', 'r') as file:
            for linea in file:
                try:
                    consulta = json.loads(linea.strip())
                    if consulta.get('doctor') == nombre_doctor:
                        citas.append({
                            "fecha": consulta.get("fecha"),
                            "hora": consulta.get("hora"),
                            "paciente_id": consulta.get("identificacion")
                        })
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return f"Error: No se encontró el archivo 'consultas.json'."

    if not citas:
        return f"No hay citas registradas para el doctor {nombre_doctor}."

    return citas

