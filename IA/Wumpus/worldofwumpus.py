from janelaprincipal import JanelaPrincipal

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sys
import _thread as thread

from playsound import playsound

def soundFX(arquivo, loop):

	if loop:
		while (True):
			playsound(arquivo)

	else:
		playsound(arquivo)

def fechar (self, widget):
	
	thread.exit()
	Gtk.main_quit()

if __name__ == "__main__":

	worldOfWumpus = JanelaPrincipal(sys.argv[1])
	worldOfWumpus.connect("delete-event", fechar)
	worldOfWumpus.show_all()

	thread.start_new_thread(soundFX, ('Audio/March of the Spoons.mp3', True))
	worldOfWumpus.main()
