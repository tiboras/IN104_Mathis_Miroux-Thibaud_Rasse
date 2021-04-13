import unittest
import IN104_TD2

class testAnimal(unittest.TestCase):
	couleurPossible=["bleu","rouge","vert","jaune"]
	
	def test_couleur(self):
		self.assertTrue(self.couleurPossible)
	


