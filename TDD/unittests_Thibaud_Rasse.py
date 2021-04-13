import unittest
import IN104_TD2

class testAnimal(unittest.TestCase):
	couleurPossible=["bleu","rouge","vert","jaune"]
	
	def test_couleur(self):
		coucou=oiseau("coucou",3,0.4)
		coucou.couleur("rouge")
		self.assertTrue(self.couleurPossible)

	def test_temps gestation(self):
		
		marmotte=mamifère("marmotte",5,5)
		marmotte.tempsGestation(5)
		self.assertTrue((self.tempsGestation<12)&(self.tempsGestation>1))


	


	def test_temps_gestation(self)
		self.assertRaises(IN104_TD2.OutOfRangeError, IN104_TD2.main, 9) #créer cdans IN104TD2 un si temps de gestation trp grand raise l'erreur quu'il faut.





if __name__ == '__main__':
    unittest.main()