#!/usr/bin/python
import smbus
import RPi.GPIO as GPIO
import time
from datetime import datetime
import urllib.request
import os
from solarpi_motores_lib import *

ChipConversor = 0x48
cmdConvertirAD = 0x45
# srotacion = 0
# sinclinacion = 0
# vEjeRotacion = 0
# vEjeCabezeo = 0
# oEjeRotacion = 200    #Valor objetivo rotacion (20-200)
# oEjeCabezeo = 40     #Valor objetiuvo cabeceo (40-100)

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(11, GPIO.OUT)  # cable azul: Cabeceo Abajo.
# GPIO.setup(13, GPIO.OUT)  # cable naranja: Cabeceo Arriba.
# GPIO.setup(15, GPIO.OUT)  # cable amarillo: Rotacion anti-horario
# GPIO.setup(16, GPIO.OUT)  # cable verde: Rotacion horario

# GPIO.output(11, True)
# GPIO.output(13, True)
# GPIO.output(16, True)
# GPIO.output(15, True)

bus = smbus.SMBus(1)
time.sleep(1)

def lee_sensores_analogicos():
    global vEjeCabezeo
    global vEjeRotacion
    bus.write_byte(ChipConversor,cmdConvertirAD)
    time.sleep(0.1)
    vAn0 = bus.read_byte(ChipConversor)
    vAn1 = bus.read_byte(ChipConversor)
    vEjeCabezeo = bus.read_byte(ChipConversor)
    vEjeRotacion = bus.read_byte(ChipConversor)


try: 
  while True:

    print("Rotacion horario.....")
    rotacion_continua_horario()
    time.sleep(9)   
    rotacion_parar()
    lee_sensores_analogicos()
    print("    El valor final del sensor del EjeRotacion \t(OESTE)\t: ", vEjeRotacion )

    
    print("Rotacion antihorario")
    rotacion_continua_antihorario()
    time.sleep(9)
    rotacion_parar()
    lee_sensores_analogicos()
    print("    El valor final del sensor del EjeRotacion \t(ESTE)\t: ", vEjeRotacion )

    print("Moviendo la cabeza arriba")
    cabeceo_continuo_arriba()
    time.sleep(5)
    cabeceo_parar()
    lee_sensores_analogicos()
    print("    El valor final del sensor del EjeCabeceo \t(CENIT)\t: ", vEjeCabezeo )

    print("Moviendo la cabeza abajo")
    cabeceo_continuo_abajo()
    time.sleep(5)
    cabeceo_parar()
    lee_sensores_analogicos()
    print("    El valor final del sensor del EjeCabeceo  \t(HORIZ)\t: ", vEjeCabezeo )

    print("\n\b--------------- Repetimos!\n\n")
  # Fin del while True

except KeyboardInterrupt:
    print ("\n\n\t\t AAAUUGGHH!!.... Eso ha dolido!")
finally:
    print ("\t\t Cerrando correctamente el puerot GPIO.\n\n")
    GPIO.cleanup()

# Fin del programa.
