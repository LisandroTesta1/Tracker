from PyQt5 import QtWidgets
from gui.templates.control_con_stop import Ui_MainWindow
import sys
import serial,time



class mywindow(QtWidgets.QMainWindow):
    DEFECTO_MONTURA=serial.Serial("/dev/ttyACM0",9600)	
    
    def __init__(self,montura= DEFECTO_MONTURA):

        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.montura=montura
        

        self.ui.pushButton.clicked.connect(self.btnClicked)     # Conecta la señal de clickeo del boton presionado
        self.ui.pushButton_2.clicked.connect(self.btnClicked_1) # Conecta la señal de clickeo del boton presionado
        self.ui.pushButton_3.clicked.connect(self.btnClicked_2) # Conecta la señal de clickeo del boton presionado
        self.ui.pushButton_4.clicked.connect(self.btnClicked_3) # Conecta la señal de clickeo del boton presionado
        self.ui.pushButton_5.clicked.connect(self.btnClicked_5) # Conecta la señal de clickeo del boton presionado

        self.ui.pushButton.pressed.connect(self.btnReleased)     # Conecta la señal de clickeo del boton cuando se suelta
        self.ui.pushButton_2.pressed.connect(self.btnReleased_1) # Conecta la señal de clickeo del boton cuando se suelta
        self.ui.pushButton_3.pressed.connect(self.btnReleased_2) # Conecta la señal de clickeo del boton cuando se suelta
        self.ui.pushButton_4.pressed.connect(self.btnReleased_3) # Conecta la señal de clickeo del boton cuando se suelta


        

    def btnClicked(self):               # Aca se especifica que funcion va a realizar el boton
       self.montura.write(b'F')	      #24.4.24 modificado antes esta 'f'    
    def btnClicked_1(self):             # Aca se especifica que funcion va a realizar el boton
      self.montura.write(b'f')
    def btnClicked_2(self):            # Aca se especifica que funcion va a realizar el boton
       self.montura.write(b'f')
    def btnClicked_3(self):           # Aca se especifica que funcion va a realizar el boton
      self.montura.write(b'F')        #24.4.24 modificado antes esta 'f'  
    def btnClicked_5(self):           # Aca se especifica que funcion va a realizar el boton
       self.montura.write(b'f')
       self.montura.write(b'F')        # 24.4.24 esta linea no estaba
  

    def btnReleased(self):           # Aca se especifica que funcion va a realizar el boton 
       #print("arriba presionado")
       self.montura.write(b'l')           
    def btnReleased_1(self):         # Aca se especifica que funcion va a realizar el boton
       #print("izquierda presionado")
       self.montura.write(b'z')	     # 24.4.24 antes estaba esta linea  self.montura.write(b'u') 
    def btnReleased_2(self):        # Aca se especifica que funcion va a realizar el boton
       #print("abajo  presionado")
       self.montura.write(b'u')  #24.4.24 modificado porque estaba invertido asi estaba  self.montura.write(b'z') 
    def btnReleased_3(self):        # Aca se especifica que funcion va a realizar el boton
       #print("derecha  presionado")
       self.montura.write(b'm')
       



