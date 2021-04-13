import unittest
import IN104_TD2

class testAnimal(unittest.TestCase):
	couleurPossible=["bleu","rouge","vert","jaune"]
	
	def test_couleur(self):
		self.assertTrue(self.couleurPossible)
	

	def test_temps_gestation(self)
		self.assertRaises(IN104_TD2.OutOfRangeError, IN104_TD2.main, 9) #créer cdans IN104TD2 un si temps de gestation trp grand raise l'erreur quu'il faut.



