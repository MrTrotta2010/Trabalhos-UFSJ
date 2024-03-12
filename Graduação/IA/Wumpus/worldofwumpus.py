from janelaprincipal import JanelaPrincipal

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sys

if __name__ == "__main__":

	worldOfWumpus = JanelaPrincipal(sys.argv[1])
	worldOfWumpus.connect("delete-event", Gtk.main_quit)
	worldOfWumpus.show_all()
	worldOfWumpus.main()