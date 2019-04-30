import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
from graphviz import Digraph

class PopUp (Gtk.Dialog):

	def __init__ (self, pai, tipo, erro, automato, palavra):

		if tipo == "Ajuda":

			Gtk.Dialog.__init__(self, "Sobre", pai, Gtk.DialogFlags.MODAL)

			self.set_default_size(200,300)
			self.set_border_width(30)

			titulo = Gtk.Label("Como executar o programa\n")
			titulo.set_justify(Gtk.Justification.CENTER)
			self.get_content_area().add(titulo)			

			texto = Gtk.Label("1- Carregue um autômato no formato .aut a partir do menu Abrir\n" + 
					"2- Digite uma palavra e aperte Enter para verificar se a palavra é aceita pelo autômato\n"
					"3- Para ver os estados ativos a cada passo do processamento ative o passo a passo e entre com a palavra\n")

			texto.set_line_wrap(True)
			self.get_content_area().add(texto)

			fim = Gtk.Label("\nDesenvolvido por: Tiago Trotta, Thiago Adriano, Lucas Rezende e Yan Victor\n" +
							"UFSJ - 2019\n")

			fim.set_justify(Gtk.Justification.CENTER)
			self.get_content_area().add(fim)			

			self.show_all()

		elif tipo == "Erro":

			Gtk.Dialog.__init__(self, "Erro!", pai, Gtk.DialogFlags.MODAL)

			self.set_border_width(30)

			titulo = Gtk.Label(erro)
			# titulo.set_justify(Gtk.Justification.CENTER)
			self.get_content_area().add(titulo)			

			self.show_all()

		elif tipo == "Passo-a-Passo":

			self.palavra = palavra
			self.automato = automato

			Gtk.Dialog.__init__(self, "Passo-a-Passo", pai, Gtk.DialogFlags.MODAL)

			# self.set_border_width(30)

			self.titulo = Gtk.Label("Palavra: " + palavra + "\nEstado Inicial")
			self.titulo.set_justify(Gtk.Justification.CENTER)

			self.grafo = Digraph(format='svg')
			self.grafo.attr(rankdir='LR')
			# automato.grafo.node(automato.estadoInicial)

			self.grafo.node('', shape='plaintext', fixedsize='true', height='0.1', width='0.1')

			for no in automato.transicoes.keys():

				if no in automato.estadosFinais:
					self.grafo.attr('node', shape='doublecircle')

				else:
					self.grafo.attr('node', shape='circle')

				if no == automato.estadoInicial:
					self.grafo.attr('node', color='red')

				else:
					self.grafo.attr('node', color='black')
					

				self.grafo.node(no)

			for no in automato.transicoes.keys():

				if no == self.automato.estadoInicial:

					self.grafo.edge('', no, arrowsize='0.5')

				for transicao in automato.transicoes[no]:

					for no2 in automato.transicoes[no][transicao]:

						self.grafo.edge(no, no2, label=transicao)

			self.grafo.render(filename=(automato.arquivo.replace("Entradas", "Grafos/Passos")), format='svg', cleanup=True)
			
			self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
							filename=automato.arquivo.replace("Entradas", "Grafos/Passos")+".svg", 
							width=650, 
							height=450, 
							preserve_aspect_ratio=True)
			
			self.imagem = Gtk.Image()
			self.imagem.set_from_pixbuf(self.pixbuf)
			
			self.caixa = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=40)

			self.caixa.pack_start(self.titulo, True, True, 0)
			self.caixa.pack_start(self.imagem, True, True, 0)

			self.caixaInterna = Gtk.Box(spacing=20)

			botaoProximo = Gtk.Button("Próximo")
			botaoProximo.connect("clicked", self.aoClick)
			botaoAnterior = Gtk.Button("Anterior")
			botaoAnterior.connect("clicked", self.aoClick)

			self.caixaInterna.pack_start(botaoAnterior, True, True, 0)
			self.caixaInterna.pack_start(botaoProximo, True, True, 0)
			self.caixaInterna.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(255.0, 255.0, 255.0, 1.0))

			self.caixa.pack_start(self.caixaInterna, True, True, 0)

			self.get_content_area().add(self.caixa)

			self.caixa.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(255.0, 255.0, 255.0, 1.0))

			self.indice = -1

			self.show_all()

	def aoClick (self, widget):

		if widget.get_label() == "Próximo":

			if self.indice < len(self.palavra)-1:
				self.indice += 1

			else:
				self.titulo.set_label("Palavra: " + self.palavra + "\nFim da palavra!")
				self.show_all()
				return

		elif widget.get_label() == "Anterior":

			if self.indice > -1:
				self.indice -= 1

		self.grafo.clear()
		self.grafo.attr(rankdir='LR')
		# automato.grafo.node(automato.estadoInicial)

		self.grafo.node('', shape='plaintext', fixedsize='true', height='0.1', width='0.1')

		for no in self.automato.transicoes.keys():

			if no in self.automato.estadosFinais:
				self.grafo.attr('node', shape='doublecircle')

			else:
				self.grafo.attr('node', shape='circle')

			if self.indice == -1:

				self.titulo.set_label("Palavra: " + self.palavra + "\nEstado Inicial")

				if no == self.automato.estadoInicial:
					self.grafo.attr('node', color='red')

				else:
					self.grafo.attr('node', color='black')

			else:

				self.titulo.set_label("Palavra: " + self.palavra + "\nProcessou " + self.palavra[self.indice])

				if no in self.automato.estadosAtivos[self.indice]:
					self.grafo.attr('node', color='red')

				else:
					self.grafo.attr('node', color='black')
				

			self.grafo.node(no)

		for no in self.automato.transicoes.keys():

			if no == self.automato.estadoInicial:

				self.grafo.edge('', no, arrowsize='0.5')

			for transicao in self.automato.transicoes[no]:

				for no2 in self.automato.transicoes[no][transicao]:

					self.grafo.edge(no, no2, label=transicao)

		self.grafo.render(filename=(self.automato.arquivo.replace("Entradas", "Grafos/Passos")), format='svg', cleanup=True)
			
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
						filename=self.automato.arquivo.replace("Entradas", "Grafos/Passos")+".svg", 
						width=650, 
						height=450, 
						preserve_aspect_ratio=True)
			
		self.imagem.set_from_pixbuf(self.pixbuf)

		self.show_all()
