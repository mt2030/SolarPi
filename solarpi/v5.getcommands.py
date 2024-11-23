#!/bin/python

import time
from datetime import datetime
import urllib.request
import os

try:
  while True:
    fechaleida = datetime.now()
    if os.stat('comandos.txt').st_size == 0:
        print(str(fechaleida), " Vamos a descargar el archivo de internet")
        try:
            url = "http://s3.eu-north-1.amazonaws.com/ciudad94.com/comandos.txt"
            urllib.request.urlretrieve(url, 'comandos.txt')
        except socket.gaierror:
            print("    Ha habido un error gaierror al descargar el fichero")
        except urllib.error.URLError:
            print("    Tenemos problemas con la url de aws, ¿es correcta?")
        except:
            print("    Ha petatado algo y no sabemos bien el que")
        else:
            print("    Ya se ha descargado el archivo")
        finally:
            pass
    else:
        print(str(fechaleida)," Exite un fichero con datos por procesar...")




    #Aqui haremos la llamada a la lambda




    time.sleep(60)

except KeyboardInterrupt:
    print ("\n\n\t\t Entendio... vamos finalizando...")

#except:
#    print("Algo fue mal pero no sabemos el qué...")

