#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)  # cable azul: Cabeceo Abajo.
GPIO.setup(13, GPIO.OUT)  # cable naranja: Cabeceo Arriba.
GPIO.setup(15, GPIO.OUT)  # cable amarillo: Rotacion anti-horario
GPIO.setup(16, GPIO.OUT)  # cable verde: Rotacion horario

GPIO.output(11, True)
GPIO.output(13, True)
GPIO.output(16, True)
GPIO.output(15, True)


def rotacion_horario():
    GPIO.output(15,False)
    time.sleep(0.4)
    GPIO.output(15,True)
    time.sleep(0.2)
    

def rotacion_antihorario():
    GPIO.output(16,False)
    time.sleep(0.3)
    GPIO.output(16,True)
    time.sleep(0.2)


def rotacion_continua_horario():
    time.sleep(0.5) # previene la inercia de un movimiento anterior.
    GPIO.output(15,False)


def rotacion_continua_antihorario():
    time.sleep(0.3) # previene la inercia de un movimiento anterior.
    GPIO.output(16,False)


def rotacion_parar():
    GPIO.output(15,True)
    GPIO.output(16,True)
    time.sleep(0.3) # previene la inercia del movimiento anterior.


def cabeceo_abajo():
    GPIO.output(11,False)
    time.sleep(0.3)
    GPIO.output(11,True)
    time.sleep(0.2)


def cabeceo_continuo_abajo():
    time.sleep(0.3)
    GPIO.output(11,False)


def cabeceo_arriba():
    GPIO.output(13,False)
    time.sleep(0.3)
    GPIO.output(13,True)
    time.sleep(0.2)


def cabeceo_continuo_arriba():
    time.sleep(0.3)
    GPIO.output(13,False)


def cabeceo_parar():
    GPIO.output(11,True)
    GPIO.output(13,True)
    time.sleep(0.2) # previene la inercia del movimiento anterior.


