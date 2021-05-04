from ..utils.vector import Vector2
"""Initialement la caméra se situe en 0,0. Sont affichées les planètes qui se situent dans l'écran c'est à dire les coordonnées 800*600. 
Le reste n'est pas affiché (coordonnées négatives). 
Le facteur scale n'est que utilisé lorsque """

class Camera:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.position = Vector2(0, 0)
        self.scale = 1

    def to_screen_coords(self, position):
        """ Converts the world-coordinate position to a screen-coordinate. """
        return position.__add__(self.position) 

    def from_screen_coords(self, position):
        """ Converts the screen-coordinate position to a world-coordinate. """
        return position.__sub__(self.position)
