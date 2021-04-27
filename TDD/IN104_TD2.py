class Animal:

    def __init__(self, name,weight,size):


        self.name = name
        self.weight = weight
        self.size = size


class mamifère(Animal):

	def _init_(self,couleurPelage,tempsGestation):
		self.couleurPelage=couleurPelage
		self.tempsGestation=tempsGestation

	def couleur(self,couleurPelage):
		self.couleurPelage=couleurPelage

	def tempsGestation(self,tempsGestation):
		self.tempsGestation=tempsGestation


class oiseau(Animal):

	def _init_(self,couleurPlume,tailleOeuf):
		self.couleurPlume=couleurPlume
		self.tailleOeuf=tailleOeuf

	def couleur(self,couleurPlume):
		self.couleurPlume=couleurPlume

	def tailleOeuf(self,tailleOeuf):
		self.tailleOeuf=tailleOeuf

	def printoiseau(self):
		print ("L'oiseau s'appelle" ,self.name, ",ses plumes sont de couleur", self.couleurPlume)


class OutOfRangeError(ValueError) :
	pass


def definition_animal(gestation):	
	if not (1<gestation<12) :	
		raise OutOfRangeError("le temps de gestation est trop long")

	taille_Oeuf = 2
	coucou=oiseau("coucou",3,0.4)
	coucou.couleur("rouge")
	coucou.tailleOeuf(taille_Oeuf)
	coucou.printoiseau()

	

definition_animal(8)