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
		print ("l'oiseau s'apelle " ,self.name, "il est de couleur ", self.couleurPlume)




def main()
	coucou=oiseau("coucou",3,0.4)
	coucou.couleur("rouge")
	coucou.tailleOeuf(2)
	coucou.printoiseau()

# j'ai travaillé avec Thiabud sur ce code