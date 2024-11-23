#!/usr/bin/python
import smbus
import RPi.GPIO as GPIO
import time
from datetime import datetime
import urllib.request
import os
import ssl
from lib.motores import *
from lib.solarpath import *



# Crear un contexto SSL que no verifique los certificados
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Crear un objeto HTTPSHandler con el contexto SSL personalizado
https_handler = urllib.request.HTTPSHandler(context=context)

# Construir un opener personalizado que use el HTTPSHandler sin verificar los certificados
opener = urllib.request.build_opener(https_handler)

# Instalar el opener globalmente
urllib.request.install_opener(opener)






ChipConversor = 0x48
cmdConvertirAD = 0x45
srotacion = 0
sinclinacion = 0
vEjeRotacion = 0
vEjeCabeceo = 0
oEjeRotacion = 200   #Valor objetivo rotacion (20-200)
oEjeCabeceo = 40     #Valor objetiuvo cabeceo (40-100)

bus = smbus.SMBus(1)
time.sleep(1)


def leer_comandos():
    with open("comandos.txt", "r+") as archivo:
        # Queremos leer la primera linea del fichero.
        comando = archivo.readline()
        resultado = comando.strip()

    with open("comandos.txt", "r+") as archivo:
        # Guardamos el fichero pero sin la primera linea.
        comandos = archivo.readlines()
        archivo.seek(0)
        archivo.truncate()
        for linea in comandos[1:]:
            archivo.write(linea)

    return resultado



def lee_sensores_analogicos():
    global vEjeCabeceo
    global vEjeRotacion
    bus.write_byte(ChipConversor,cmdConvertirAD)
    time.sleep(0.1)
    vAn0 = bus.read_byte(ChipConversor)
    vAn1 = bus.read_byte(ChipConversor)
    vEjeCabeceo = bus.read_byte(ChipConversor)
    vEjeRotacion = bus.read_byte(ChipConversor)


try: 
  modo_automatico = True
  fechaleida = datetime.now()
  mes_actual = fechaleida.month
  dia_actual = fechaleida.day
  hora_actual = fechaleida.hour

  while True:
    traza = " Modo automatico: "
    el_comando = leer_comandos()

    if el_comando.startswith("MANUAL"):
        modo_automatico = False
    if el_comando.startswith("AUTOMATICO"):
        modo_automatico = True

    if modo_automatico == True: 
        fechaleida = datetime.now()
        mes_actual = fechaleida.month
        dia_actual = fechaleida.day
        hora_actual = fechaleida.hour
        print("    Estamos en modo.......: Automatico")
        print("    Este es el mes actual :", mes_actual)
        print("    Este es el dia actual :", dia_actual)
        print("    Esta es la hora actual:", hora_actual)
        oEjeRotacion = Cal_obj_rotacion(hora_actual, dia_actual, mes_actual)
        oEjeCabeceo = Cal_obj_cabeceo(hora_actual, dia_actual, mes_actual)
    else :
        print("    Estamos en modo.......: Manual")
        print("    Este es el mes objetivo :", mes_actual)
        print("    Este es el dia objetivo :", dia_actual)
        print("    Esta es la hora objetivo:", hora_actual)

        if el_comando.startswith("MoverRotacion"):
            # Vamos a partir el valor de la instrucion en dos quedandonos con la parte nuemrica
            _, valor = el_comando.split()
            oEjeRotacion = int(valor)
            print("    --> Moveremos el eje de Rotacion")

        if el_comando.startswith("MoverCabeceo"):
            # Vamos a partir el valor de la instrucion en dos quedandonos con la parte nuemrica
            _, valor = el_comando.split()
            oEjeCabeceo = int(valor)
            print("    --> Moveremos el eje de cabeceo")

        if el_comando.startswith("MoverFecha"):
            fechax = el_comando.split()
            mes_actual = int(fechax[3])
            dia_actual = int(fechax[2])
            hora_actual = int(fechax[1])
            oEjeRotacion = Cal_obj_rotacion(hora_actual, dia_actual, mes_actual)
            oEjeCabeceo = Cal_obj_cabeceo(hora_actual, dia_actual, mes_actual)



    lee_sensores_analogicos()
    print("    El valor del sensor del EjeRotacion  es: ", vEjeRotacion , "\tobjetivo: ", oEjeRotacion)
    print("    El valor del sensor del EjeCabeceo   es: ", vEjeCabeceo , "\tobjetivo: ", oEjeCabeceo)
    traza = traza + str(modo_automatico)
    traza = traza + " EjeRotacion: " + str(vEjeRotacion) + "-->" + str(oEjeRotacion)
    traza = traza + " EjeCabeceo: "  + str(vEjeCabeceo)  + "-->" + str(oEjeCabeceo)

    se_han_movido_las_placas = False

    if vEjeRotacion < (oEjeRotacion - 5) :
        print(" Girando las placas en sentido horario...")
        rotacion_horario()
        se_han_movido_las_placas = True
        traza = traza + " Horario "

    if vEjeRotacion > (oEjeRotacion + 8) :
        print(" Girando las plachas en sentido anti-horario...")
        rotacion_antihorario()
        se_han_movido_las_placas = True
        traza = traza + " Antihor "

    if vEjeCabeceo < (oEjeCabeceo - 3) :
        print(" Levantando las placas...")
        cabeceo_arriba()
        se_han_movido_las_placas = True
        traza = traza + " Levanta "

    if vEjeCabeceo > (oEjeCabeceo + 5) :
        print(" Bajando las placas...")
        cabeceo_abajo()
        se_han_movido_las_placas = True
        traza = traza + " Bajando "
    
    if not se_han_movido_las_placas:
        print(" Vamos a esperar 5 segundos para ver si hay que corregir...")
        traza = traza + " Nada que hacer "
        with open('logs/activity.log', 'a') as archivo_log:
            registro = f"{fechaleida}{traza}\n"
            archivo_log.write(registro)
        time.sleep(5)
    else:
        traza = traza + " Movimiento terminado "
        with open('logs/activity.log', 'a') as archivo_log:
            registro = f"{fechaleida}{traza}\n"
            archivo_log.write(registro)

    print ("Hacemos una llamada lambda a la web para actualizar valores")
    #Hacemos una llamada lambda a la web para actualizar valores
    url = "http://5ynslybapapfth4mgupcrsjtj40mwvph.lambda-url.eu-north-1.on.aws/?operacion="+str(modo_automatico)+"&oEjeRotacion="+str(vEjeRotacion)+"&oEjeCabeceo="+str(vEjeCabeceo)+"Fecha=2024-05-13"
    urllib.request.urlopen(url, 'estado.txt')

    print("\n\b--------------- Repetimos!\n\n")
  # Fin del while True

except KeyboardInterrupt:
    print ("\n\n\t\t AAAUUGGHH!!.... Eso ha dolido!")
finally:
    print ("\t\t Cerrando correctamente el puerto GPIO.\n\n")
    GPIO.cleanup()

# Fin del programa.
