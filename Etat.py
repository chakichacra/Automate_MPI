from Transition import Transition

class Etat(object):
	"""docstring for Etat"""
	def __init__(self,num, final = False, init = False):
		self.numero = num
		self.Transitions = []
		self.isFinal = final 
		self.isInit = init 
		self.alphaReconnu = []

	def newTransi(self, mot, etat):
		self.Transitions.append(Transition(mot, etat))
		if mot not in self.alphaReconnu:
			self.alphaReconnu.append(mot)


	def transiParMot(self, mot):
		result = []
		for transi in self.Transitions:
			if (transi.mot == mot):
				result.append(str(transi.etatCible.numero))
		return result
