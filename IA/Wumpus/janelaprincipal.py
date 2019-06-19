import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk

from caverna import Caverna
from agente import Agente
import random
from playsound import playsound

import _thread as thread

class JanelaPrincipal(Gtk.Window):

	def __init__ (self, debug):

		Gtk.Window.__init__(self, title="The World Of Wumpus")
		#self.set_size_request(600, 400)

		self.status = 0

		self.caverna = Caverna((3, 0), debug)
			
		self.agente = Agente(self.caverna.salas)

		self.caixa = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.caixa)

		self.caixaInferior = Gtk.Box()
		self.caixaInterna = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

		self.gridCaverna = Gtk.Grid()
		self.gridAgente = Gtk.Grid()

		self.score = Gtk.Label()
		self.score.set_justify(Gtk.Justification.FILL)

		self.wrapper = Gtk.Fixed()
		self.wrapper.put(self.gridCaverna, 0, 0)
		self.wrapper.put(self.caixaInterna, 430, 140)
		self.wrapper.put(self.gridAgente, 570, 0)

		self.caixaInterna.pack_start(self.score, True, True, 0)
		
		# self.caixaInterna.pack_start(self.gridCaverna, True, True, 0)
		# self.caixaInterna.pack_start(Gtk.Label(' '), True, True, 0)
		# self.caixaInterna.pack_start(self.score, True, True, 0)
		# self.caixaInterna.pack_start(Gtk.Label(' '), True, True, 0)
		# self.caixaInterna.pack_start(self.wrapperAgente, True, True, 0)

		# self.wrapper.add(self.caixaInterna)
		
		self.caixa.add(self.wrapper)
		self.caixa.add(self.caixaInferior)

		self.botaoRodar = Gtk.Button("Rodar")
		self.botaoRodar.connect("clicked", self.aoClick)
		self.botaoGerar = Gtk.Button("Gerar nova caverna")
		self.botaoGerar.connect("clicked", self.aoClick)

		self.caixaInferior.pack_start(self.botaoGerar, True, True, 0)
		self.caixaInferior.pack_start(self.botaoRodar, True, True, 0)

		self.imagensCaverna = [[Gtk.Image() for i in range(4)] for j in range(4)]
		self.imagensAgente = [[Gtk.Image() for i in range(4)] for j in range(4)]

		self.gerarMapas(False)

	def gerarMapas (self, override):

		self.score.set_markup('<big><b>Score:</b>\n'+str(self.agente.desempenho)+'</big>\n'+self.agente.status)

		for i in range(4):
			for j in range(4):

				imagem = 'Imagens/'

				if 'agente' in self.caverna.salas[i][j]:
					imagem += 'agente'
					
					if 'ouro' in self.caverna.salas[i][j]:
						imagem += 'ouro'
					if 'fedor' in self.caverna.salas[i][j]:
						imagem += 'fedor'
					if 'brisa' in self.caverna.salas[i][j]:
						imagem += 'brisa'

					self.imagensCaverna[i][j].set_from_file(imagem+".png")

				else:

					if 'wumpus' in self.caverna.salas[i][j]:

						imagem += 'wumpus'

						if 'ouro' in self.caverna.salas[i][j]:
							imagem += 'ouro'
						if 'brisa' in self.caverna.salas[i][j]:
							imagem += 'brisa'

					elif 'wumpusmorto' in self.caverna.salas[i][j]:

						imagem += 'wumpusmorto'

					elif 'ouro' in self.caverna.salas[i][j]:
						
						imagem += 'ouro'

						if 'fedor' in self.caverna.salas[i][j]:
							imagem += 'fedor'
						if 'brisa' in self.caverna.salas[i][j]:
							imagem += 'brisa'

					elif 'poço' in self.caverna.salas[i][j]:

						imagem += 'poço'

						if 'fedor' in self.caverna.salas[i][j]:
							imagem += 'fedor'

					else:

						if 'fedor' in self.caverna.salas[i][j]:
							imagem += 'fedor'
						
						if 'brisa' in self.caverna.salas[i][j]:
							imagem += 'brisa'

					if imagem == 'Imagens/':
						imagem += 'vazio'

					self.imagensCaverna[i][j].set_from_file(imagem+".png")

				if not override:
					self.gridCaverna.attach(self.imagensCaverna[i][j], j, i, 1, 1)

		for i in range(4):
			for j in range(4):

				imagem = 'Imagens/'

				if 'agente' in self.agente.salasConhecidas[i][j]:
					imagem += 'agente'
					
					if 'ouro' in self.agente.salasConhecidas[i][j]:
						imagem += 'ouro'
					if 'fedor' in self.agente.salasConhecidas[i][j]:
						imagem += 'fedor'
					if 'brisa' in self.agente.salasConhecidas[i][j]:
						imagem += 'brisa'

				else:

					if 'wumpus' in self.agente.salasConhecidas[i][j]:

						imagem += 'wumpus'

						if 'ouro' in self.agente.salasConhecidas[i][j]:
							imagem += 'ouro'
						if 'brisa' in self.agente.salasConhecidas[i][j]:
							imagem += 'brisa'

					elif 'wumpusmorto' in self.agente.salasConhecidas[i][j]:

						imagem += 'wumpusmorto'

					elif 'wumpus?' in self.agente.salasConhecidas[i][j] and '~w' not in self.agente.salasConhecidas[i][j]:

						imagem += 'wumpus?'

						if 'poço?' in self.agente.salasConhecidas[i][j] and '~p' not in self.agente.salasConhecidas[i][j]:

							imagem += 'poço?'

					elif 'ouro' in self.agente.salasConhecidas[i][j]:
						
						imagem += 'ouro'

						if 'fedor' in self.agente.salasConhecidas[i][j]:
							imagem += 'fedor'
						if 'brisa' in self.agente.salasConhecidas[i][j]:
							imagem += 'brisa'

					elif 'poço' in self.agente.salasConhecidas[i][j]:

						imagem += 'poço'

						if 'fedor' in self.agente.salasConhecidas[i][j]:
							imagem += 'fedor'

					elif 'poço?' in self.agente.salasConhecidas[i][j] and '~p' not in self.agente.salasConhecidas[i][j]:

						imagem += 'poço?'

					else:

						if 'fedor' in self.agente.salasConhecidas[i][j]:
							imagem += 'fedor'
						
						if 'brisa' in self.agente.salasConhecidas[i][j]:
							imagem += 'brisa'

					if imagem == 'Imagens/':

						if 'visitada' in self.agente.salasConhecidas[i][j]:
							imagem += 'vazio'
	
						else:
							imagem += 'vazio?'

				self.imagensAgente[i][j].set_from_file(imagem+".png")

				if not override:
					self.gridAgente.attach(self.imagensAgente[i][j], j, i, 1, 1)

	def aoClick (self, widget):

		if widget.get_label() == 'Rodar':

			if self.status == 0: #Diz se o agente morreu ou encontrou o ouro

				self.status = self.agente.acao()
				self.caverna.atualizaAgente(self.agente.posicao)

		else:
			self.caverna.geraCaverna((3,0), '0')
			self.agente.resetaAgente(self.caverna.salas)
			self.status = 0
		
		#self.agente.imprimeCaverna()
		self.gerarMapas(True)
		self.show_all()


	def main(self):

		Gtk.main()