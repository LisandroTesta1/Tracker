from typing import Tuple
import pigpio
import numpy as np
import cv2 as cv
import serial,time



class motorPWM:

   def __init__(self, step_pin, dir_pin):
    self.step_pin = step_pin
    self.step_dir = dir_pin
    self.pi = pigpio.pi()
    self.pi.set_mode(self.step_pin, pigpio.OUTPUT)
    self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)

   def mover(self, estado):
    frec = 40000

    if estado == "Derecha Rapido":
     self.pi.write(self.dir_pin, 1)
    if estado == "Izquierda Rapido":
     self.pi.write(self.dir_pin, 0)
    if estado == "Arriba Rapido":
     self.pi.write(self.dir_pin, 1)
    if estado == "Abajo Rapido":
     self.pi.write(self.dir_pin, 0)

    self.pi.hardware_PWM(self.step_pin, frec, 80000)
   
   def detener(self):
    self.pi.hardware_PWM(self.step_pin, 0, 0)


class ControlMotores:

    def __init__(self):
      self.azimut = MotorPWM(step_pin=18, dir_pin=16)
      self.elev = MotorPWM(step_pin=22, dir_pin=24)

    def control(self,x):
      
      
      #------------------------------------------------------------------
      estado_azimut_anterior=self.estado_azimut_actual
      estado_elevacion_anterior=self.estado_elevacion_actual
      #------------------------- ---------------------------- ----------------------------------------------------
      
      #------------------------ Errores en posicion en pixeles ----------------------------------------------------
      error_posicion_azimut = x[0]
      error_posicion_elevacion =x[1]
      #------------------------- ---------------------------- ----------------------------------------------------
      #-------------------------Asignacion de estado -------------------------------------------------------------
      if error_posicion_azimut >= 0:
            if abs(error_posicion_azimut) > 30:
               self.estado_azimut_actual = "Derecha Rapido"
            #elif abs(error_posicion_azimut)<50 and abs(error_posicion_azimut)>30:#nova
            #  estado_azimut_actual = "Derecha Lento"#nova
            else:
               self.estado_azimut_actual = "Frena"
      else:
            if abs(error_posicion_azimut) > 30:#30
               self.estado_azimut_actual = "Izquierda Rapido"
            #elif abs(error_posicion_azimut)<50 and abs(error_posicion_azimut)>30:#nova
            #   estado_azimut_actual = "Izquierda Lento"#nova
            else:
               self.estado_azimut_actual = "Frena"
	
      if error_posicion_elevacion >= 0:
            if abs(error_posicion_elevacion) > 30:#30
               self.estado_elevacion_actual = "Arriba Rapido"
            #elif abs(error_posicion_elevacion)<50 and abs(error_posicion_elevacion)>30:#nova
            #   estado_elevacion_actual = "Arriba Lento"#nova
            else:
               self.estado_elevacion_actual = "Frena"	
      else:
            if abs(error_posicion_elevacion) > 30:#30
               self.estado_elevacion_actual = "Abajo Rapido"
            #elif abs(error_posicion_elevacion)<50 and abs(error_posicion_elevacion)>30:#nova
            #   estado_elevacion_actual = "Abajo Lento"#nova
            else:
               self.estado_elevacion_actual = "Frena"
      		
      #-----------------------------------------------------------------------------------------------------------

      #-----Comprobacion de estado y movimiento de montura--------------------------------------------------------
	
                
      #-----Comprobacion de estado y movimiento de montura--------------------------------------------------------

      if estado_azimut_anterior != self.estado_azimut_actual:
            
            if self.estado_azimut_actual == "Derecha Rapido":
               motorPWM.mover(self.azimut, estado_azimut_actual)
	       #self.montura.write(b'z')
               #elif estado_azimut_actual == "Derecha Lento":#nova
               #self.montura.write(b'zz')#nova            
	       #lista = [0x3A,0x47,0x31,0x33,0x31,0x0D] 
               #montura_tx.write(lista) 
               #time.sleep(0.02) 
               #lista = [0x3A,0x49,0x31,0x30,0x38,0x30,0x35,0x30,0x30,0x0D] 
               #montura_tx.write(lista)
               #time.sleep(0.02)
               #lista = [0x3A,0x4A,0x31,0x0D]
               #montura_tx.write(lista)		
            elif self.estado_azimut_actual == "Izquierda Rapido":
               motorPWM.mover(self.azimut, estado_azimut_actual)
               #self.montura.write(b'u')	
               #elif estado_azimut_actual == "Izquierda Lento":#nova
               #self.montura.write(b'uu')#nova      
               #lista = [0x3A,0x47,0x31,0x33,0x30,0x0D] 
               #montura_tx.write(lista)
               #time.sleep(0.02) 
               #lista = [0x3A,0x49,0x31,0x30,0x38,0x30,0x35,0x30,0x30,0x0D] 
               #montura_tx.write(lista)
               #time.sleep(0.02)
               #lista = [0x3A,0x4A,0x31,0x0D]
               #montura_tx.write(lista)		
            elif self.estado_azimut_actual == "Frena":
               #self.montura.write(b'f')
               motorPWM.detener(self.azimut)
			

      if estado_elevacion_anterior != self.estado_elevacion_actual:
           time.sleep(0.02)
           if self.estado_elevacion_actual == "Arriba Rapido":
           #self.montura.write(b'l')
               motorPWM.mover(self.elev, estado_azimut_actual)
                               		
        #elif estado_elevacion_actual == "Arriba Lento":#nova
           #  self.montura.write(b'll')#nova      
           #lista = [0x3A,0x47,0x32,0x33,0x31,0x0D] 
           #montura_tx.write(lista)
           #time.sleep(0.02) 
           #lista = [0x3A,0x49,0x32,0x30,0x38,0x30,0x35,0x30,0x30,0x0D] 
           #montura_tx.write(lista)
           #time.sleep(0.02)
           #lista = [0x3A,0x4A,0x32,0x0D]
           #montura_tx.write(lista) 	
           elif self.estado_elevacion_actual == "Abajo Rapido":
           #self.montura.write(b'm')
               motorPWM.mover(self.elev, estado_azimut_actual)
        #elif estado_elevacion_actual == "Abajo Lento":#nova
           # self.montura.write(b'mm')#nova      
           #lista = [0x3A,0x47,0x32,0x33,0x30,0x0D] 
           #montura_tx.write(lista)
           #time.sleep(0.02) 
           #lista = [0x3A,0x49,0x32,0x30,0x38,0x30,0x35,0x30,0x30,0x0D] 
           #montura_tx.write(lista)
           #time.sleep(0.02)
           #lista = [0x3A,0x4A,0x32,0x0D]
           #montura_tx.write(lista)		
           elif self.estado_elevacion_actual == "Frena":
           #self.montura.write(b'F') #'f' -> 'F' 24/04/24
               motorPWM.detener(self.elev)				
      #---------------------------------------------------------------------------------------------------------
      
      
      #----------------------------------------------Imprimo en pantalla los datos------------------------------		
      #time.sleep(0.001)      #Tiempo_general
      self.montura.flushInput() # Se borra el buffer del puerto COM
      #---------------------------------------------------------------------------------------------------------
