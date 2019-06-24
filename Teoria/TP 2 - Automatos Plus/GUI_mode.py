import sys
sys.path.append('Fonte/')

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from JanelaPrincipal import JanelaPrincipal

if __name__ == "__main__":
	
	app = JanelaPrincipal()
	app.connect("delete-event", Gtk.main_quit)
	app.show_all()
	app.main()
	