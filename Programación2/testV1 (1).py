import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from project_client import Client
import re
import new_window_doctor
import new_window_patient
client = Client("http://localhost:80")

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        screen = QGuiApplication.primaryScreen()
        size = screen.size()
        self.resize(size.width(), size.height())
        self.setWindowTitle("TeleSaludUQ - PyQt5")

        self.l1 = QLabel('Bienvenido a TeleSaludUQ')
        self.b1 = QPushButton('Registrar usuario')
        self.b2 = QPushButton('Iniciar Sesión')

        font = QFont("Times New Roman", 24)
        self.l1.setFont(font)
        self.b1.setFont(font)
        self.b2.setFont(font)

        self.b1.clicked.connect(lambda: self.onClick(registro=True))
        self.b2.clicked.connect(lambda: self.onClick(registro=False))

        gridLayout = QGridLayout()
        gridLayout.addWidget(self.l1, 0, 0, alignment=Qt.AlignCenter)
        gridLayout.addWidget(self.b1, 1, 0, alignment=Qt.AlignCenter)
        gridLayout.addWidget(self.b2, 2, 0, alignment=Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(gridLayout)
        self.setCentralWidget(widget)

        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

    def onClick(self, registro=False):
        dialog = QDialog(self)
        dialog.setWindowTitle("Registro" if registro else "Inicio de sesión")
        dialog.resize(400, 200)

        font = QFont("Times New Roman", 18)

        l1 = QLabel('Identificación:')
        l2 = QLabel('Contraseña:')
        l1.setFont(font)
        l2.setFont(font)

        e1 = QLineEdit()
        e2 = QLineEdit()
        e2.setEchoMode(QLineEdit.Password)

        bAceptar = QPushButton("Aceptar")
        bCancelar = QPushButton("Cancelar")
        bAceptar.setFont(font)
        bCancelar.setFont(font)

        gridLayout = QGridLayout()
        gridLayout.addWidget(l1, 0, 0)
        gridLayout.addWidget(e1, 0, 1)
        gridLayout.addWidget(l2, 1, 0)
        gridLayout.addWidget(e2, 1, 1)
        gridLayout.addWidget(bAceptar, 2, 0)
        gridLayout.addWidget(bCancelar, 2, 1)

        dialog.setLayout(gridLayout)
        

        if registro:
            l0 = QLabel('Nombre:')
            l3 = QLabel('Rol:')
            l0.setFont(font)
            l3.setFont(font)

            e0 = QLineEdit()
            e0.setFont(font)

            radioPaciente = QRadioButton("Paciente")
            radioMedico = QRadioButton("Medico")
            radioPaciente.setFont(font)
            radioMedico.setFont(font)
            radioPaciente.setChecked(True)

            rolLayout = QHBoxLayout()
            rolLayout.addWidget(radioPaciente)
            rolLayout.addWidget(radioMedico)

            gridLayout.addWidget(l0, 0, 0)
            gridLayout.addWidget(e0, 0, 1)
            gridLayout.addWidget(l1, 1, 0)
            gridLayout.addWidget(e1, 1, 1)
            gridLayout.addWidget(l2, 2, 0)
            gridLayout.addWidget(e2, 2, 1)
            gridLayout.addWidget(l3, 3, 0)
            gridLayout.addLayout(rolLayout, 3, 1)
            gridLayout.addWidget(bAceptar, 4, 0)
            gridLayout.addWidget(bCancelar, 4, 1)

            bAceptar.clicked.connect(lambda: self.registrarUsuario(
                e0.text(), e1.text(), e2.text(),
                "paciente" if radioPaciente.isChecked() else "Medico",
                dialog
            ))
        else:
            bAceptar.clicked.connect(lambda: self.iniciarSesion(e1.text(), e2.text(), dialog))

        bCancelar.clicked.connect(dialog.reject)
        dialog.exec_()

    def iniciarSesion(self, identificacion, contrasena, dialog):
        try:
            resultado = client.openSession(identificacion, contrasena)

            if resultado == "Medico":
                QMessageBox.information(self, "Inicio de sesión", "Bienvenido, médico.")
                dialog.accept()
                self.mostrarPanelMedico(identificacion)
            elif resultado == "paciente":
                QMessageBox.information(self, "Inicio de sesión", "Bienvenido, paciente.")
                dialog.accept()
                self.mostrarAgendamiento(identificacion)
            else:
                QMessageBox.warning(self, "Inicio de sesión", f"No se pudo identificar el rol:\n{resultado}")
                dialog.reject()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al conectar con el servidor:\n{str(e)}")
            dialog.reject()

    def registrarUsuario(self, nombre, identificacion, contrasena, rol, dialog):
        try:
            resultado = client.registerUser(nombre, identificacion, rol, contrasena)
            QMessageBox.information(self, "Resultado de registro", f"Respuesta del servidor:\n{resultado}")
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al conectar con el servidor:\n{str(e)}")
            dialog.reject()

    def mostrarAgendamiento(self, id_usuario):
        lista_medicos_raw = client.getDoctorsList(id_usuario)
        if isinstance(lista_medicos_raw, str):
            if not lista_medicos_raw.strip():
                QMessageBox.critical(self, "Error", "No se pudo obtener la lista de médicos.")
                return
            try:
                lista_medicos = json.loads(lista_medicos_raw)
            except json.JSONDecodeError:
                QMessageBox.critical(self, "Error", "La respuesta del servidor no es válida.")
                return
        else:
            lista_medicos = lista_medicos_raw

        if not isinstance(lista_medicos, list):
            QMessageBox.critical(self, "Error", "La respuesta del servidor no es una lista válida.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Agendar Cita Médica")
        dialog.resize(400, 400)

    # Botones de cerrar, minimizar y maximizar como una ventana normal
        dialog.setWindowFlags(Qt.Window)  
    

        font = QFont("Times New Roman", 18)

        labelMedico = QLabel("Seleccione un médico:")
        labelMedico.setFont(font)

        comboMedico = QComboBox()
        comboMedico.setFont(font)

            
        
        comboMedico.addItems(lista_medicos)

        labelFecha = QLabel("Seleccione la fecha:")
        labelFecha.setFont(font)

        dateEdit = QDateEdit()
        dateEdit.setFont(font)
        dateEdit.setCalendarPopup(True)
        dateEdit.setDate(QDate.currentDate())

        labelHora = QLabel("Seleccione la hora:")
        labelHora.setFont(font)

        timeEdit = QTimeEdit()
        timeEdit.setFont(font)
        timeEdit.setTime(QTime.currentTime())

        bAgendar = QPushButton("Agendar Cita")
        bAgendar.setFont(font)
        bAgendar.clicked.connect(lambda: self.agendarCita(
            id_usuario,
            comboMedico.currentText(),
            dateEdit.date().toString("yyyy-MM-dd"),
            timeEdit.time().toString("HH:mm"),
            dialog
        ))

        bConectar = QPushButton("Conectar a Cita")
        bConectar.setFont(font)
        bConectar.clicked.connect(lambda: self.getdoct(id_usuario))

        bCerrarSesion = QPushButton("Cerrar Sesión")
        bCerrarSesion.setFont(font)
        bCerrarSesion.clicked.connect(lambda: self.cerrarSesion(id_usuario, dialog))

        layout = QVBoxLayout()
        layout.addWidget(labelMedico)
        layout.addWidget(comboMedico)
        layout.addWidget(labelFecha)
        layout.addWidget(dateEdit)
        layout.addWidget(labelHora)
        layout.addWidget(timeEdit)
        layout.addWidget(bAgendar)
        layout.addWidget(bConectar)
        layout.addWidget(bCerrarSesion)

        dialog.setLayout(layout)
        dialog.exec_()


    def getdoct(self, id_usuario):
        try:
            ip_raw = client.getDoctorIP(id_usuario)

            if not isinstance(ip_raw, str) or not ip_raw.strip():
                QMessageBox.critical(self, "Error", "No se recibió IP del doctor.")
                return

            # Extraer la IP usando expresión regular
            match = re.search(r"La IP del doctor activo es:\s*(\S+)", ip_raw)
            if match:
                ip = match.group(1)
            else:
                QMessageBox.critical(self, "Error", "No se pudo extraer la IP del mensaje recibido.")
                return

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al procesar la IP: {str(e)}")
            return
        
        self.nw=new_window_patient.NewWindow(ip_raw)
        self.nw.show()
 

        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Conexión a Cita")
        dialog.resize(300, 150)

        font = QFont("Times New Roman", 16)

        label = QLabel(f"Conectando al doctor...\nIP del doctor: {ip}")
        label.setFont(font)
        label.setWordWrap(True)

        bCerrar = QPushButton("Cerrar")
        bCerrar.setFont(font)
        bCerrar.clicked.connect(dialog.close)
        

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(bCerrar)

        dialog.setLayout(layout)
        dialog.exec_()
        """

    def agendarCita(self, id_usuario, doctorid, fecha, hora, dialog):
        try:
            resultado = client.addAppointment(id_usuario, doctorid, fecha, hora)
            QMessageBox.information(self, "Cita Agendada", f"Cita con {doctorid} el {fecha} a las {hora} registrada exitosamente.\n{resultado}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agendar la cita:\n{str(e)}")

    def cerrarSesion(self, user_id, dialog):
        try:
            resultado = client.closeSession(user_id)
            QMessageBox.information(self, "Sesión cerrada", f"Sesión finalizada correctamente.\n{resultado}")
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cerrar la sesión:\n{str(e)}")
            dialog.reject()

    def mostrarPanelMedico(self, id_medico):
        dialog = QDialog(self)
        dialog.setWindowTitle("Panel del Médico")
        dialog.resize(500, 400)

        font = QFont("Times New Roman", 18)

        label = QLabel(f"Bienvenido, Dr. {id_medico}")
        label.setFont(font)

        # Obtener citas del médico (sin validaciones)
        citas_raw = client.getAppointmentsList(id_medico)
        citas_decodificadas = json.loads(citas_raw)
        if isinstance(citas_decodificadas, dict):
            citas = citas_decodificadas.get("citas", [])
        else:
            citas = citas_decodificadas

        # Mostrar citas en una lista
        listaCitas = QListWidget()
        listaCitas.setFont(font)

        for cita in citas:
            fecha = cita.get("fecha", "Sin fecha")
            hora = cita.get("hora", "Sin hora")
            paciente = cita.get("paciente_id", "Sin paciente")
            texto = f"{fecha} a las {hora} con paciente {paciente}"
            listaCitas.addItem(texto)

        bAtenderCitas = QPushButton("cerrar sesión")
        bAtenderCitas.setFont(font)
        bAtenderCitas.clicked.connect(lambda: self.cerrarSesion(id_medico, dialog))

        bCerrarSesion = QPushButton("Atender citas")
        bCerrarSesion.setFont(font)
        bCerrarSesion.clicked.connect(lambda: self.abrirVentanaVideo(dialog))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(QLabel("Citas agendadas:"))
        layout.addWidget(listaCitas)
        layout.addWidget(bAtenderCitas)
        layout.addWidget(bCerrarSesion)

        dialog.setLayout(layout)
        dialog.exec_()
    def abrirVentanaVideo(self, dialog):
        dialog.close() 
        self.ventanaVideo = new_window_doctor.NewWindow()
        self.ventanaVideo.show()

# Lanzar la aplicación
app = QApplication([])
ex = MainWindow()
ex.show()
app.exec()