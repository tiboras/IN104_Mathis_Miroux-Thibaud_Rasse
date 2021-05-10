from ..utils.vector import Vector, Vector2
from .constants import G
import numpy as np

#à intégrer qqpart dans le code
def gravitational_force(pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    vect = pos2-pos1
    return (G*mass2*mass1/(vect.norm()**3))*vect



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
        raise NotImplementedError

        
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

        N = len(self.world)
        deriv = Vector(4*N)
        for i in range(N) :
            deriv[2*i] = y0[(N+i)*2]
            deriv[2*i+1] = y0[(N+i)*2+1]
            acc_i = Vector2(0,0)
            pos_i = Vector2(y0[2*i],y0[2*i+1])  
            for j in range(2) :
                if i!=j :
                    acc_i += gravitational_force(pos_i,1,Vector2(y0[2*j],y0[2*j+1]),self.world.get(j).mass)
            deriv[2*N+2*i] = acc_i.get_x()
            deriv[2*N+2*i+1] = acc_i.get_y()
            
        return deriv


        # Fx = np.zeros((N,N)) #utiliser le inti ?
        # Fy = np.zeros((N,N)) #utiliser le inti ?
        # for i in range(len(self.world)):
        #     for j in range(i):
        #         Fx[i][j]=-G*self.world.get(i).mass*self.world.get(j).mass*(self.world.get(i).position.get_x()-self.world.get(j).position.get_x())/((self.world.get(i).position-self.world.get(j).position).norm())**(3/2)
        #         Fx[j,i] = -Fx[i,j]
        #         Fy[i][j]=-G*self.world.get(i).mass*self.world.get(j).mass*(self.world.get(i).position.get_y()-self.world.get(j).position.get_y())/((self.world.get(i).position-self.world.get(j).position).norm())**(3/2)
        #         Fy[j,i] = -Fy[i,j]
        # forces_appliques_x = np.dot(Fx, np.ones((N,1))) #faire la somme des forces appliqueés à toutes les planètes
        # forces_appliques_y = np.dot(Fy, np.ones((N,1))) #faire la somme des forces appliqueés à toutes les planètes

        # deriv = Vector(4*N)
        # for j in range(2*N) :
        #     deriv[j] = y0[2*N+j]
        # for i in range(N):
        #     deriv[2*N+ (2*i)] = (forces_appliques_x[i,0])/self.world.get(i).mass
        #     deriv[2*N+ (2*i+1)] = (forces_appliques_y[i,0])/self.world.get(i).mass
        # return deriv

    def make_solver_state(self):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the 
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities. """
        N = len(self.world)
       
        pos_vit=Vector(4*N)
        for k in range(N):
            pos_vit[2*k]=self.world.get(k).position.get_x()
            pos_vit[2*k+1]=self.world.get(k).position.get_y()
            pos_vit[2*N+2*k]=self.world.get(k).velocity.get_x()
            pos_vit[2*N+2*k+1]=self.world.get(k).velocity.get_y()
        
        return pos_vit
