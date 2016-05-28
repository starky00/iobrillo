#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  io-sensors.py
#  
#  Copyright 2016 starky <starky@TP300LJ>
#
#  Es necesario que el servicio iio-sensor-proxy instalado y esté activo.
#  Script para cambiar automaticamente el brillo con el sensor de luz
#  salida de brillo /sys/bus/acpi/devices/ACPI0008:00/iio:device0/in_illuminance_raw
#  el fichero recoge luz desde 0 a 42144 la idea es que existan 20 posiciones diferentes de luz
#  por lo que la transicion sera de 2107 puntos
#  para modificar el brillo hay que escirbir sobre /sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-eDP-1/intel_backlight/brigthness
#  maximo brillo que yo tengo es 937
#  la variacion no debe estar entre unos valores durante un periodo para cambiar

import sys
import time 
import math

global K
K = 0.50 #Multiplicador de la K entre menor valor menor sensibilidad

def comienzo():
		time.sleep(0.5)
		salida = prepara_dato()
		escribe_brillo(salida)
		return 0

def brillo(): #Accede a el sensor y extrae el dato
		fichero=open('/sys/bus/acpi/devices/ACPI0008:00/iio:device0/in_illuminance_raw','r')
		dato=fichero.readline()
		fichero.close()
		return dato
		
def lee_brillo():
		fichero = open('/sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-eDP-1/intel_backlight/brightness','r')
		dato_previo=fichero.readline()
		fichero.close()
		return dato_previo		

def prepara_dato(): #Prepara el dato
		dato_tratado = int(brillo())
		if dato_tratado <= 1:
			dato_tratado = 2
		dato_tratado = int(math.log(dato_tratado)*120)
		return dato_tratado
	
	
def escribe_brillo(dato_listo):
		#print dato_listo
		global K
		dato_previo = lee_brillo()
		r = int(dato_previo) / float(dato_listo)
		c = int(dato_listo) / float(dato_previo)
		#print dato_previo,"dato previo entre listo", r,"X",dato_listo,"dato listo entre previo ", c
		#if ((dato_listo / int(dato_previo)) > ) or ((int(dato_previo) / dato_listo) > 0.1):
		if ((int(dato_previo) / float(dato_listo)) < K ) or ((int(dato_listo) / float(dato_previo)) < K):
			fichero=open('/sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-eDP-1/intel_backlight/brightness','w')
			dato_listo=fichero.write(str(dato_listo))
			fichero.close()

