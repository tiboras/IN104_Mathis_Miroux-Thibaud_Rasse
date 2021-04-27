import IN104_TD2 
import unittest


class testAnimal(unittest.TestCase):
	
	def test_couleur(self):
		coucou=IN104_TD2.oiseau("coucou",3,0.4)
		couleurPossible=["bleu","rouge","vert","jaune"]
		for couleur in couleurPossible :
			coucou.couleur(couleur)
			print(coucou.couleur)
			self.assertTrue(coucou.couleur in couleurPossible)

	def test_temps_gestation(self):
		marmotte=IN104_TD2.mamifère("marmotte",5,5)
		marmotte.tempsGestation(5)
		self.assertTrue(1<marmotte.tempsGestation<12)

class testAnimalBadInput(unittest.TestCase) :
	def test_temps_gestation_2(self) : 
		self.assertRaises(IN104_TD2.OutOfRangeError, IN104_TD2.definition_animal, 15)

if __name__ == '__main__':
    unittest.main()