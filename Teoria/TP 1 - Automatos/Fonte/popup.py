import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
from graphviz import Digraph

# Classe geral de PopUp
class PopUp (Gtk.Dialog):

	# O construtor recebe o tipo de PopUp a ser instanciado
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
			self.get_content_area().add(titulo)			

			self.show_all()

		elif tipo == "Passo-a-Passo":


			self.pai = pai
			self.palavra = palavra
			self.automato = automato

			Gtk.Dialog.__init__(self, "Passo-a-Passo", pai, Gtk.DialogFlags.MODAL)

			self.aceita = False

			# Verifica se ao final do processamento da palavra, algum dos estados finais está ativo
			for estado in automato.estadosFinais:
				
				if estado in automato.estadosAtivos[len(palavra)-1]:
				
					self.aceita = True
					break

			self.subtitulo = Gtk.Label()
			self.subtitulo.set_justify(Gtk.Justification.CENTER)

			if self.aceita:

				self.subtitulo.set_markup("<big><span foreground='green'>Aceita!</span></big>")

			else:

				self.subtitulo.set_markup("<big><span foreground='red'>Não aceita!</span></big>")

			self.titulo = Gtk.Label()
			self.titulo.set_markup("<big>Palavra: " + palavra + "\nEstado Inicial</big>")
			self.titulo.set_justify(Gtk.Justification.CENTER)

			# Monta o grafo com os estados ativos ressaltados
			self.grafo = self.pai.automato.montaGrafoPassoAPasso(self.palavra, -1)

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
			self.caixa.pack_start(self.subtitulo, True, True, 0)
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
				self.titulo.set_markup("<big>Palavra: " + self.palavra + "\nProcessou " + self.palavra[self.indice] + "</big>")

			else:
				self.titulo.set_markup("<big>Palavra: " + self.palavra + "\nFim da palavra!</big>")
				self.show_all()
				return

		elif widget.get_label() == "Anterior":

			if self.indice > -1:
				self.indice -= 1
				self.titulo.set_markup("<big>Palavra: " + self.palavra + "\nProcessou " + self.palavra[self.indice] + "</big>")

			else:
				self.titulo.set_markup("<big>Palavra: " + self.palavra + "\nEstado Inicial</big>")

		self.grafo.clear()

		self.grafo = self.pai.automato.montaGrafoPassoAPasso(self.palavra, self.indice)

		self.grafo.render(filename=(self.automato.arquivo.replace("Entradas", "Grafos/Passos")), format='svg', cleanup=True)
			
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
						filename=self.automato.arquivo.replace("Entradas", "Grafos/Passos")+".svg", 
						width=650, 
						height=450, 
						preserve_aspect_ratio=True)
			
		self.imagem.set_from_pixbuf(self.pixbuf)

		self.show_all()
