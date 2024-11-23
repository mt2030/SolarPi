#!/usr/bin/python
import smbus
import RPi.GPIO as GPIO
import time
from datetime import datetime

ChipConversor = 0x48
cmdConvertirAD = 0x45
srotacion = 0
sinclinacion = 0
vEjeRotacion = 0
vEjeCabezeo = 0
oEjeRotacion = 200    #Valor objetivo rotacion (20-200)
oEjeCabezeo = 40     #Valor objetiuvo cabezeo (40-100)

bus = smbus.SMBus(1)
time.sleep(0.5)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)  # cable azul: motor rotacion en sentido horario
GPIO.setup(16, GPIO.OUT)  # cable verde: monotr rota. sen.  anti-horario
GPIO.setup(15, GPIO.OUT)  # cable amarillo: motor cabeza, abajo.
GPIO.setup(13, GPIO.OUT)  # cable naranja: motor cabeza, arriba.


GPIO.output(11, True)
GPIO.output(16, True)
GPIO.output(15, True)
GPIO.output(13, True)

bus = smbus.SMBus(1)
time.sleep(1)

def rotacion_horario():
    
    GPIO.output(11,False)
    time.sleep(0.5)
    GPIO.output(11,True)
    time.sleep(0.5)
    

def rotacion_antihorario():
    
    GPIO.output(16,False)
    time.sleep(0.5)
    GPIO.output(16,True)
    time.sleep(0.5)
    

def cabezeo_abajo():

    GPIO.output(15,False)
    time.sleep(0.5)
    GPIO.output(15,True)
    time.sleep(0.5)


def cabezeo_arriba():

    GPIO.output(13,False)
    time.sleep(0.5)
    GPIO.output(13,True)
    time.sleep(0.5)
    

def lee_sensores_analogicos():

    global vEjeCabezeo
    global vEjeRotacion
    bus.write_byte(ChipConversor,cmdConvertirAD)
    time.sleep(0.1)
    vAn0 = bus.read_byte(ChipConversor)
    vAn1 = bus.read_byte(ChipConversor)
    vEjeCabezeo = bus.read_byte(ChipConversor)
    vEjeRotacion = bus.read_byte(ChipConversor)


def Cal_obj_rotacion(arghora, argdia, argmes):

    #Queremos que esta funcion nos devuelva el valor en el que tienen que estar las placas en un determinado mes dia y hora
	#El valor que nos va a devolver es un numero entre 20 y 200 que sera la posicion objetivo o l aposicion a la que deberia estar la placa
    enero = (14,14,14,14,14,14,14,14,14,14,75,85,97,111,126,140,154,166,176,14,14,14,14,14)
    febrero = (14,14,14,14,14,14,14,14,14,59,69,80,92,108,124,141,157,170,181,190,14,14,14,14)
    marzo = (14,14,14,14,14,14,14,14,14,53,62,74,88,106,126,146,164,178,189,199,14,14,14,14)
    abril = (14,14,14,14,14,14,14,14,36,45,55,67,82,104,130,156,175,189,199,209,217,14,14,14)
    mayo = (14,14,14,14,14,14,14,22,30,38,48,59,74,99,135,166,185,198,208,216,224,14,14,14)
    junio = (14,14,14,14,14,14,14,18,26,34,43,53,67,92,134,170,190,202,211,219,227,235,14,14)
    julio = (14,14,14,14,14,14,14,19,27,35,43,54,68,91,129,165,186,199,209,217,225,233,14,14)
    agosto = (14,14,14,14,14,14,14,14,33,41,50,62,77,99,129,157,178,191,202,211,220,14,14,14)
    septiembre = (14,14,14,14,14,14,14,14,42,51,61,73,89,108,131,153,171,184,195,204,14,14,14,14)
    octubre = (14,14,14,14,14,14,14,14,52,61,71,83,98,115,133,150,165,178,188,197,14,14,14,14)
    noviembre = (14,14,14,14,14,14,14,14,14,68,77,89,102,117,132,147,160,172,182,14,14,14,14,14)
    diciembre = (14,14,14,14,14,14,14,14,14,14,79,89,101,115,129,143,156,167,177,14,14,14,14,14)

    if argmes == 1 :
       resultado = enero[arghora]
    if argmes == 2 :
       resultado = febrero[arghora]
    if argmes == 3 :
       resultado = marzo[arghora]
    if argmes == 4 :
       resultado = abril[arghora]
    if argmes == 5 :
       resultado = mayo[arghora]
    if argmes == 6 :
       resultado = junio[arghora]
    if argmes == 7 :
       resultado = julio[arghora]
    if argmes == 8 :
       resultado = agosto[arghora]
    if argmes == 9 :
       resultado = septiembre[arghora]
    if argmes == 10 :
       resultado = octubre[arghora]
    if argmes == 11 :
       resultado = noviembre[arghoora]
    if argmes == 12 :
       resultado =  diciembre[arghora]

    return resultado


def Cal_obj_cabezeo(arghora, argdia, argmes):

    #Queremos que esta funcion nos devuelva el valor en el que tienen que estar las placas en un determinado mes dia y hora
    #El valor que nos va a devolver es un numero entre 20 y 200 que sera la posicion objetivo o l aposicion a la que deberia estar la placa
    enero = (46,46,46,46,46,46,46,46,46,46,46,54,59,63,63,63,59,53,46,42,42,42,42,42)
    febrero = (42,42,42,42,42,42,42,42,42,42,51,59,65,69,71,69,65,60,51,43,49,49,49,49)
    marzo = (49,49,49,49,49,49,49,49,49,49,58,66,72,77,79,77,72,65,57,48,56,56,56,56)
    abril = (46,46,46,46,46,46,46,46,46,56,65,74,82,87,89,85,79,71,62,53,43,61,61,61)
    mayo = (43,43,43,43,43,43,43,43,52,61,70,80,88,94,96,92,84,75,66,56,47,63,63,63)
    junio = (45,45,45,45,45,45,45,45,54,63,72,81,90,98,100,95,87,78,68,59,51,42,61,61)
    julio = (43,43,43,43,43,43,43,43,52,61,70,80,89,96,98,94,87,78,68,59,50,42,58,58)
    agosto = (48,48,48,48,48,48,48,48,48,58,67,76,84,90,92,89,82,74,65,55,46,54,54,54)
    septiembre = (44,44,44,44,44,44,44,44,44,54,63,71,78,82,83,81,74,67,58,48,49,49,49,49)
    octubre = (40,40,40,40,40,40,40,40,40,49,57,64,70,73,74,71,65,58,50,41,43,43,43,43)
    noviembre = (43,43,43,43,43,43,43,43,43,43,51,58,63,66,66,63,59,52,44,46,46,46,46,46)
    diciembre = (46,46,46,46,46,46,46,46,46,46,46,54,59,61,62,60,56,50,42,46,46,46,46,46)

    if argmes == 1 :
       resultado = enero[arghora]
    if argmes == 2 :
       resultado = febrero[arghora]
    if argmes == 3 :
       resultado = marzo[arghora]
    if argmes == 4 :
       resultado = abril[arghora]
    if argmes == 5 :
       resultado = mayo[arghora]
    if argmes == 6 :
       resultado = junio[arghora]
    if argmes == 7 :
       resultado = julio[arghora]
    if argmes == 8 :
       resultado = agosto[arghora]
    if argmes == 9 :
       resultado = septiembre[arghora]
    if argmes == 10 :
       resultado = octubre[arghora]
    if argmes == 11 :
       resultado = noviembre[arghoora]
    if argmes == 12 :
       resultado =  diciembre[arghora]

    return resultado



while True:
    print("\n\n")
    print("# Aqui empieza un nuevo ciclo................................######")
    

    fechaleida = datetime.now()
    print("Esta es la fecha que acabamos de leer: ", fechaleida)
    mes_actual = fechaleida.month
    print("    Este es el mes actual:", mes_actual)
    dia_actual = fechaleida.day
    print("    Este es el dia actual:", dia_actual)
    hora_actual = fechaleida.hour
    print("    Esta es la hora actual:", hora_actual)

    oEjeRotacion = Cal_obj_rotacion(hora_actual, dia_actual, mes_actual)
    print("    Este es el objetivo rotacion: ", oEjeRotacion)

    oEjeCabezeo = Cal_obj_cabezeo(hora_actual,dia_actual,mes_actual)
    print("    Este es el objetivo cabezeo: ", oEjeCabezeo)
    
    lee_sensores_analogicos()
    print("    El valor del EjeRotacion  es: ", vEjeRotacion )
    print("    El valor del EjeCabezeo  es: ", vEjeCabezeo )

    se_han_movido_las_placas = False

    if vEjeRotacion < (oEjeRotacion - 5) :
        print(" Girando las placas en sentido horario...")
        rotacion_horario()
        se_han_movido_las_placas = True

    if vEjeRotacion > (oEjeRotacion + 5) :
        print(" Girando las plachas en sentido anti-horario...")
        rotacion_antihorario()
        se_han_movido_las_placas = True

    if vEjeCabezeo < (oEjeCabezeo - 3) :
        print(" Levantando las placas...")
        cabezeo_arriba()
        se_han_movido_las_placas = True

    if vEjeCabezeo > (oEjeCabezeo + 3) :
        print(" Bajando las placas...")
        cabezeo_abajo()
        se_han_movido_las_placas = True
  
    if not se_han_movido_las_placas:
        print(" Parece que las placas estan en su sitio.")
        print(" Vamos a esperar 5 segundos para ver si hay que corregir...")
        time.sleep(5)

# Fin del programa.






