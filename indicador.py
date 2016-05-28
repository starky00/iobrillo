#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import appindicator
import threading
from iobrillo import iobrillo 
gtk.gdk.threads_init()





    
class AppIndicatorBrillo:
	def __init__(self):

		self.contador = 0
		self.dato = 1
		self.ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
		self.ind.set_status(appindicator.STATUS_ACTIVE)
		self.ind.set_attention_icon ("indicator-brillo")
		self.ind.set_icon("/home/auto.png") #Colocar donde prefiramos

		# create a menu
		self.menu = gtk.Menu()
		# create items for the menu - labels, checkboxes, radio buttons and images are supported:
		check = gtk.CheckMenuItem("Brillo automatico")
		gtk.gdk.threads_enter()
		check.connect("activate",self.datohilo)
		gtk.gdk.threads_leave()
		check.show()
		self.menu.append(check)
 

		salida = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		salida.connect("activate", self.quit)
		salida.show()
		self.menu.append(salida)
					
		self.menu.show()

		self.ind.set_menu(self.menu)
		
	def datoext(self):		
		while self.dato:
			iobrillo.comienzo()	

	def datohilo(self, widget, data=None):
		if self.contador >= 1:	
			self.dato = 0
			self.contador = 0
		else:
			t = threading.Thread(target = self.datoext).start()  
			self.contador += 1
			self.dato = 1
	def quit(self, widget, data=None):
		gtk.main_quit()
	


def main():
	gtk.main()
	return 0

if __name__ == "__main__":
	indicator = AppIndicatorBrillo()
	main()
