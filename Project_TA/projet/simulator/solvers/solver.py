from ..utils.vector import Vector, Vector2
from ..physics.engine import *
class SolverError(Exception):
    pass


class ISolver:

    # NOTE: our systems do not depend on time,
    # so the input t0 will never be used by the
    # the derivatives function f
    # However, removing it will not simplify
    # our functions so we might as well keep it
    # and build a more general library that
    # we will be able to reuse some day

    def __init__(self, f, t0, y0,world,max_step_size=0.01):
        self.f = f
        self.t0 = t0
        self.y0 = y0
        self.max_step_size = max_step_size
        self.world = world

    def integrate(self, t):
        """ Compute the solution of the system at t
            The input `t` given to this method should be increasing
            throughout the execution of the program.
            Return the new state at time t.
        """
        raise NotImplementedError

def multiply(liste, float_f) :
    N = len(liste)
    for i in range(N):
        liste[i] *= float_f
    return liste

class DummySolver(ISolver):

    def integrate(self, t):
        """ Compute the solution of the system at t
            The input `t` given to this method should be increasing
            throughout the execution of the program.
            Return the new state at time t.
        """

        y=self.y0
        N = int((t-self.t0)//self.max_step_size)
        dt = self.max_step_size
        for k in range(1,N):
            funct = self.f(self.t0+k*dt,y)
            y = y+dt*funct
        self.y0 = y
        self.t0 = t
        return y

class LeapFrogSolver(ISolver):
    def integrate(self, t):
        y=self.y0 
        N = int((t-self.t0)//self.max_step_size)
        dt = self.max_step_size
        nb = int(len(y)/4)
        for k in range(1,N):
            f = self.f(self.t0+k*dt,y)
            f[2*nb:] = multiply(f[2*nb:],1/2)
            f[:2*nb] += multiply(f[2*nb:],dt)
            for i in range(nb) :
                acc_i = Vector2(0,0)
                pos_i = Vector2(y[2*i],y[2*i+1])
                for j in range(nb) :
                    if i!=j :
                        acc_i += gravitational_force(pos_i,1,Vector2(y[2*j],y[2*j+1]),self.world.get(j).mass)
                f[2*nb+2*i] += acc_i.get_x()/2
                f[2*nb+2*i+1] += acc_i.get_y()/2
            y = y+dt*f
        self.y0 = y
        self.t0 = t
        return y