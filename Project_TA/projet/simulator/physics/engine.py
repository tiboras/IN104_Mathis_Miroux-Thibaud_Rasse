from ..utils.vector import Vector, Vector2
from .constants import G
import numpy as np

#à intégrer qqpart dans le code
def gravitational_force(pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    vect = pos2-pos1
    return (( G*mass2*mass1/norm(vect)**3)*vect)



class IEngine:
    def __init__(self, world):
        self.world = world


    def derivatives(self, t0, y0):
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
        N = len(world)
        Fx = np.empty((N,N), dtype = Vector) #utiliser le inti ?
        Fy = np.empty((N,N), dtype = Vector) #utiliser le inti ?
        for i in range(1,len(world)+1):
            for j in range(1,i):
                Fx[i][j]=G*mass.get.world(i)*mass.get.world(j)*(get_x(position.get.world(i)-position.get.world(j)))/norm.Vector(position.get.world(i)-position.get.world(j))**(3/2)
                Fx[j,i] = -Fx[i,j]
                Fy[i][j]=G*mass.get.world(i)*mass.get.world(j)*(get_y(position.get.world(i)-position.get.world(j)))/norm.Vector(position.get.world(i)-position.get.world(j))**(3/2)
                Fy[j,i] = -Fy[i,j]


        forces_appliques_x = Fx * np.ones((N,1)) #faire la somme des forces appliqueés à toutes les planètes
        forces_appliques_y = Fy * np.ones((N,1)) #faire la somme des forces appliqueés à toutes les planètes

        deriv = vector(4*N)
        deriv[1:2*N] = y0[2*N:]
        for i in range(N):
            deriv[2*N+ (2*i)] = (forces_appliques_x[i])/mass.get.world(i)
            deriv[2*N+ (2*i+1)] = (forces_appliques_y[i])/mass.get.world(i)
        return deriv

        
    def make_solver_state(self):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the 
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """

        positions=np.zeros(N,1)
        vitesse=np.zeros(N,1)
        for k in range(N):
            positions[k]=position.get.world(k)
            vitesse[k]=velocity.get.world(k)
        result=np.concatenate((positions, vitesse), axis=None)
        raise NotImplementedError


class DummyEngine(IEngine):
    pass
