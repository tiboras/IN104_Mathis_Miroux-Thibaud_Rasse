import unittest

class testAnimal(unittest.TestCase):
	couleurPossible=["bleu","rouge","vert","jaune"]
	
	def test_couleur(self):
		self.assertTrue(self.couleurPossible)
	


