from Automate import Automate

autom = Automate("test_fich/test.txt")

autom.affiche()

print(autom.isComplet())

for x in autom.listEtat:
	print(x.alphaReconnu)


print('\n'*5)

autom.completer()

for etat in autom.listEtat:
	print(etat.transiParMot('a'))

for x in autom.listEtat:
	print(x.alphaReconnu)

print(autom.isComplet())

autom.affiche()
