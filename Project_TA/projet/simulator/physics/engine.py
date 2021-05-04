from ..utils.vector import Vector, Vector2
from .constants import G
import numpy as np


def gravitational_force(pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    vect = pos2-pos1
    return (( G*mass2*mass1/norm(vect)**3)*vect)



class IEngine:
    def __init__(self, world):
        self.world = world

    def derivatives(self, t0, y0, masses,N):
        """ This is the method that will be fed to the solver
            it does not use it's first argument t0,
            its second argument y0 is a vector containing the positions 
            and velocities of the bodies, it is laid out as follow
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.

            Return the derivative of the state, it is laid out as follow
                [vx1, vy1, vx2, vy2, ..., vxn, vyn, ax1, ay1, ax2, ay2, ..., axn, ayn]
            where vxi, vyi are the velocities and axi, ayi are the accelerations.
        """
        """faire une matrice des forces"""
        forces = np.empty((N,N), dtype = object)
        for i in range(N):
            for j in range(i+1):
                forces[i,j] = gravitational_force(y0[2*i],masses[i], y0[2*j],masses[j])
                forces[j,i] = -1* gravitational_force(y0[2*i],masses[i], y0[2*j],masses[j])
        forces_appliques = forces * np.ones((N,1)) #faire la somme des forces appliqueés à toutes les planètes
        deriv = vector(4*N)
        deriv[1:2*N] = y0[2*N:]
        for i in range(N):
            deriv[2*N+ (2*i)] = get_x(forces_appliques[i])
            deriv[2*N+ (2*i+1)] = get_y(forces_appliques[i])
        return deriv



    def make_solver_state(self):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the 
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """
        raise NotImplementedError


class DummyEngine(IEngine):
    pass
