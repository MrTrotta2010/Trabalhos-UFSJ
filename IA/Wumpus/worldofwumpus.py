from janelaprincipal import JanelaPrincipal

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

if __name__ == "__main__":

	worldOfWumpus = JanelaPrincipal()
	worldOfWumpus.connect("delete-event", Gtk.main_quit)
	worldOfWumpus.show_all()
	worldOfWumpus.main()