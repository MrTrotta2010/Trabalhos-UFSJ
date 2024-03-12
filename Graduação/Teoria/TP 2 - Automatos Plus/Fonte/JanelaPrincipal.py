import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
from BarraDeTarefas import BarraTarefas
from popup import PopUp
from automato import Automato
from entrada_saida import *
import tempfile

class JanelaPrincipal(Gtk.Window):

	def __init__(self):

		self.automato = Automato()

		self.mostrarPassoAPasso = False
		self.automatoCarregado = False

		Gtk.Window.__init__(self, title="Autômatos")
		self.set_size_request(600, 400)

		# Caixa Externa
		self.caixa = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
		self.add(self.caixa)

		# Caixa Interna
		self.caixaIn = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.caixa.add(self.caixaIn)

		# Barra de Tarefas
		self.barraDeTarefas = BarraTarefas(self)
		self.caixaIn.pack_start(self.barraDeTarefas, True, True, 0)

		# Imagem
		self.logo = Gtk.Image()
		self.logo.set_from_file("Imagens/Logo2.png")
		self.caixa.pack_start(self.logo, True, True, 0)

	def click (self, widget):

		if widget.get_label() == "Sair":

			Gtk.main_quit()

		elif widget.get_label() == "Abrir":

			abrir = Gtk.FileChooserDialog("Escolha um arquivo", self, Gtk.FileChooserAction.OPEN,
											("Cancelar", Gtk.ResponseType.CANCEL, "Abrir", Gtk.ResponseType.OK))

			resposta = abrir.run()

			if resposta == Gtk.ResponseType.OK:
				
				self.arquivo = abrir.get_filename()

				self.automato.destroiAutomato()
				retorno = criaAutomato(self.automato, self.arquivo)

				# Monta o grafo que representa o autômato
				self.automato.montaGrafo(self.arquivo)

				if retorno != None:

					abrir.destroy()

					# PopUp de erro
					popup = PopUp(self, "Erro", retorno, None, None)
					popup.run()

					popup.destroy()
					
					return
				
				if not self.automatoCarregado:

					self.descricao = Gtk.Label()
					self.caixaIn.pack_end(self.descricao, True, True, 0)
				
				self.descricao.set_markup("\n\n<b><big>" + self.automato.descricao.title() + "</big></b>")
				self.descricao.set_justify(Gtk.Justification.CENTER)


				pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
							filename=self.arquivo.replace("Entradas", "Grafos")+".svg", 
							width=650, 
							height=450, 
							preserve_aspect_ratio=True)
				
				self.logo.set_from_pixbuf(pixbuf)
				self.caixa.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(255.0, 255.0, 255.0, 1.0))

				if not self.automatoCarregado:
					
					self.caixaInferior = Gtk.Box(spacing=20)
					self.caixa.pack_start(self.caixaInferior, True, True, 0)
	
					# Grid Layout
					self.grid = Gtk.Grid()
					self.grid.set_column_spacing(20)
					self.grid.set_row_spacing(10)
					self.caixaInferior.pack_start(Gtk.Label(), True, True, 0)
					self.caixaInferior.pack_start(self.grid, True, True, 0)
					self.caixaInferior.pack_end(Gtk.Label(), True, True, 0)

					self.automatoCarregado = True

					self.caixa.pack_start(Gtk.Label(''), True, True, 0)
					self.caixa.pack_end(Gtk.Label(''), True, True, 0)

					self.entradaPalavraLabel = Gtk.Label("Palavra: ")
					self.entradaPalavraLabel.set_justify(Gtk.Justification.RIGHT)
					self.entradaPalavraLabel.set_hexpand(True)

					self.entradaPalavra = Gtk.Entry()
					self.entradaPalavra.connect("activate", self.testeEnter)
					self.entradaPalavra.set_hexpand(True)

					self.resultadoImagem = Gtk.Image()
					self.resultadoImagem.set_from_file("Imagens/aguardando.png")

					self.passoSwitch = Gtk.Switch()
					self.passoSwitch.connect("notify::active", self.passoAPasso)
					self.passoSwitch.set_active(False)
					self.passoSwitch.set_hexpand(True)

					self.grid.attach(self.entradaPalavraLabel, 0, 0, 1, 1)
					self.grid.attach(self.entradaPalavra, 1, 0, 1, 1)
					self.grid.attach(self.resultadoImagem, 2, 0, 1, 2)
					self.grid.attach(Gtk.Label("Mostrar passo-a-passo: "), 0, 1, 1, 1)
					self.grid.attach(self.passoSwitch, 1, 1, 1, 1)
					
				self.show_all()

			abrir.destroy()

		elif widget.get_label() == "Exportar":

			if self.automatoCarregado:

				exportar = Gtk.FileChooserDialog("Exportar autômato", self, Gtk.FileChooserAction.SAVE,
													("Cancelar", Gtk.ResponseType.CANCEL, "Salvar", Gtk.ResponseType.OK))

				resposta = exportar.run()

				if resposta == Gtk.ResponseType.OK:

					self.automato.grafo.render(filename=(exportar.get_filename()).replace(".svg", ''), format='svg', cleanup=True)

				exportar.destroy()

			else:

				popup = PopUp(self, "Erro", "Nenhum autômato carregado!", self.automato, None)
				popup.run()

				popup.destroy()

		elif widget.get_label() == "Sobre":
			
			# PopUp de Ajuda
			popup = PopUp(self, "Ajuda", None, self.automato, None)
			popup.run()

			popup.destroy()

	def testeEnter (self, widget):

		retorno = self.automato.testaPalavra(self.entradaPalavra.get_text(), self.mostrarPassoAPasso)

		if len(retorno) > 19:

			popup = PopUp(self, "Erro", retorno, self.automato, self.entradaPalavra.get_text())
			popup.run()

			popup.destroy()

		else:

			if self.mostrarPassoAPasso:

				# PopUp passo a passo
				popup = PopUp(self, "Passo-a-Passo", None, self.automato, self.entradaPalavra.get_text())

			if retorno[8] == 'a':
				
				self.resultadoImagem.set_from_file("Imagens/aceita.png")
			
			else:
				
				self.resultadoImagem.set_from_file("Imagens/nAceita.png")

	def passoAPasso (self, widget, bool):

		self.mostrarPassoAPasso = not (self.mostrarPassoAPasso and True)

	def main(self):

		Gtk.main()
