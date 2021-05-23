import numpy as np 
from simulator.utils.vector import Vector, Vector2
class Simulator:
    def __init__(self, world, Engine, Solver):
        self.t = 0
        self.world = world

        self.engine = Engine(self.world)

        # Engine uses World to represent the state
        # of the world while Solver uses a
        # vector to represent the current state of
        # the ODE system.
        # The method Engine.make_solver_state computes
        # the vector of state variables (the positions
        # and velocities of the bodies) as a Vector

        y0 = self.engine.make_solver_state()


        self.solver = Solver(self.engine.derivatives, self.t, y0, world)

    def step(self, h):
        y = self.solver.integrate(self.t + h) # toute l'opération est maintenant présente dans solveur, cela est plus simple pour intergrer les collision 
       


        self.t += h


