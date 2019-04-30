import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class BarraTarefas (Gtk.MenuBar):

	def __init__ (self, pai):

		Gtk.MenuBar.__init__(self)

		# Arquivo
		self.menuArquivo = Gtk.Menu()
		self.menuArquivoDropdown = Gtk.MenuItem("Arquivo")

		self.arquivoAbrir = Gtk.MenuItem("Abrir")
		self.arquivoAbrir.connect("activate", pai.click)
		self.arquivoSair = Gtk.MenuItem("Sair")
		self.arquivoSair.connect("activate", pai.click)

		self.menuArquivoDropdown.set_submenu(self.menuArquivo)
		self.menuArquivo.append(self.arquivoAbrir)
		self.menuArquivo.append(Gtk.SeparatorMenuItem())
		self.menuArquivo.append(self.arquivoSair)

		self.append(self.menuArquivoDropdown)

		# Ajuda
		self.menuAjuda = Gtk.Menu()
		self.menuAjudaDropdown = Gtk.MenuItem("Ajuda")

		self.info = Gtk.MenuItem("Sobre")
		self.info.connect("activate", pai.click)

		self.menuAjudaDropdown.set_submenu(self.menuAjuda)
		self.menuAjuda.append(self.info)

		self.append(self.menuAjudaDropdown)
		