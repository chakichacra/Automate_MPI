from Etat import Etat



class Automate(object):
	"""docstring for Automate"""
	def __init__(self, path):

		file = open(path, 'r')
		content = file.read()
		content = content.split("\n")   # Lis le fihier et met les diferentes lignes dans un tableau 



		self.listEtat = [] 
		for x in range(0,int(content[1])):     #Initialise les Etats et les mets dans une liste
			self.listEtat.append(Etat(x))



		self.nmbrEtatInit = int(content[2].split(':')[0])  #Stock le nombre d'etat initial
		self.nmbrEtatFinal = int(content[3].split(':')[0]) #Stock le nombre d'etat final 


		self.etatInit = []
		for x in range(0,self.nmbrEtatInit):
			self.listEtat[int(content[2].split(':')[1].split(',')[x])].isInit = True   #Set les Etat initiaux 
			self.etatInit.append(self.listEtat[int(content[2].split(':')[1].split(',')[x])])


		self.etatFin = []
		for x in range(0,self.nmbrEtatFinal):
			self.listEtat[int(content[3].split(':')[1].split(',')[x])].isFinal = True #Set les Etat finaux
			self.etatFin.append(self.listEtat[int(content[3].split(':')[1].split(',')[x])])



		temp = content[4].split('/') #Isole chaque transition de la ligne du fichier contenant les transitions



		for x in temp:
			tempp = x.split(';')
			self.listEtat[int(tempp[0])].newTransi(tempp[1], self.listEtat[int(tempp[2])]) #Initialise les transitions de chaque Etat



		self.nmbrEtat = int(content[1])
		self.alphabet = []
		self.AlphabetEntier = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','*']
		for x in range(0,int(content[0])):
			self.alphabet.append(self.AlphabetEntier[x])
		self.est_synchrone = self.checkSync()



	def affiche(self):


		if (self.nmbrEtatInit <= 1):
			print("Etat initial: " + str(self.etatInit[0].numero), end='')
		else:
			print("Etats initiaux: "+str(self.etatInit[0].numero), end='')
			for x in range(1,self.nmbrEtatInit):
				print(','+str(self.etatInit[x].numero), end='')



		if (self.nmbrEtatFinal <= 1):
			print("\nEtat final: " + str(self.etatFin[0].numero), end='')
		else:
			print("\nEtats finaux: "+str(self.etatFin[0].numero), end='')
			for x in range(1,self.nmbrEtatFinal):
				print(','+str(self.etatFin[x].numero), end='')

		tableau = self.tableauTransi()


		
		for x in tableau:
			print('\n')
			for y in x:
				print(y, end='\t')

			



	def isDeterministe(self):
		if (self.nmbrEtatInit != 1):  
			return False				#verifie qu'il n'y a qu'un seul etat initiale
		
		temp = []
		for etat in self.listEtat:
			for transi in etat.Transitions:     #verifie pour chaque etat
				if (transi.mot in temp):		#qu'il n'a qu'une seul transition par mot
					return False
				temp.append(transi.mot)
			temp = []


		return True

	def isComplet(self):

		for etat in self.listEtat: 
	
			if (len(self.alphabet) != len(etat.alphaReconnu)):
				return False

		return True


	def tableauTransi(self):

		
		tablal = []
		for x in range(0, self.nmbrEtat + 1):
			tablal.append([])							#Initialisation du tableau

			for y in range(0, len(self.alphabet) + 2):
				tablal[x].append([])




		for x in range(0,self.nmbrEtat):
			tablal[x+1][1] = str(self.listEtat[x].numero) #1er colonne

		for x in range(0,len(self.alphabet)):
			tablal[0][x+2] = self.alphabet[x]

		tablal[0][0] = "f/i"
		tablal[0][1] = "Etat"

		for x in self.listEtat:
			if (x.isInit == True):
				tablal[x.numero+1][0] = "I"

			if (x.isFinal):
				if (x.isInit):
					tablal[x.numero+1][0] += "/F"
				else:
					tablal[x.numero+1][0] = "F"

		cpt = 0
		for etat in self.listEtat:
			for lettre in self.alphabet:
				transi = etat.transiParMot(lettre)
				for tran in transi:
					if (tablal[etat.numero+1][self.AlphabetEntier.index(lettre)+2] == []):
						tablal[etat.numero+1][self.AlphabetEntier.index(lettre)+2] = tran
					else:
						tablal[etat.numero+1][self.AlphabetEntier.index(lettre)+2] += ','+str(tran)




		return tablal

	def checkSync(self):
		'''if ('*' in self.alphabet):
			self.est_synchrone = True
			return True
		self.est_synchrone = False
		return False'''

		for etat in self.listEtat:
			if (etat.transiParMot('*') != []):
				self.est_synchrone = True
				return True
		self.est_synchrone = False
		return False



	def completer(self):
		if (self.isComplet()):
			return

		poubelle = Etat(self.nmbrEtat)

		for etat in self.listEtat:
			temp_transi_manquante = []
			for alpha in self.alphabet:
				if (alpha not in etat.alphaReconnu):
					temp_transi_manquante.append(alpha)
			for alpha in temp_transi_manquante:
				etat.newTransi(alpha, poubelle)

		for alpha in self.alphabet:
			poubelle.newTransi(alpha, poubelle)

		self.listEtat.append(poubelle)
		self.nmbrEtat += 1




		