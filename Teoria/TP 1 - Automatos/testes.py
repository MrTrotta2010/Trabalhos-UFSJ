import unittest
from automato import Automato
import entrada_saida as io

class testesAutomato (unittest.TestCase):

	def testeVerificaAlfabeto (self):

		AFD = Automato()
		AFD.alfabeto = ['a', 'b']

		self.assertTrue(AFD.verificaAlfabeto("ab"))
		retorno = "Palavra não aceita! - Os símbolos ['c', 'd'] não estão no alfabeto\n<< Alfabeto: ['a', 'b']"
		self.assertEqual(retorno, AFD.verificaAlfabeto("abcd"))

	def testeTestaaPalavra (self):
		
		AFN = Automato()
		AFN.alfabeto = ['a', 'b']
		AFN.transicoes = {'q0' : {'a' : ['q1', 'qf'], 'b' : ['q0']}, 'q1' : {'b' : 'qf'}, 'qf' : {}}
		AFN.estadoInicial = 'q0'
		AFN.estadosFinais = ['qf']

		#self.assertEqual("Palavra aceita!", AFN.testaPalavra("bbab", False))
		self.assertEqual("Palavra aceita!", AFN.testaPalavra("a", False))
		#self.assertEqual("Palavra aceita!", AFN.testaPalavra("ab", False))

		#self.assertEqual("Palavra não aceita!", AFN.testaPalavra("ba", False))
		self.assertEqual("Palavra não aceita!", AFN.testaPalavra("b", False))
		self.assertEqual("Palavra não aceita!", AFN.testaPalavra("baa", False))

if __name__ == '__main__':

	unittest.main()