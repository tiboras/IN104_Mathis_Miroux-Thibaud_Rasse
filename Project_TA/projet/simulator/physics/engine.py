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

def colision(type,body1,body2):
    if (body1.position -body2.position).norm() >(body1.draw_radius+body1.draw_radius):
        return body1,body2
    else:
        if type==0:                  #fusion de 2 étoile
            masstot=body1.mass+body2.mass
            body1.mass=masstot
            body2.mass=masstot
            body1.velocity=1/masstot*(body1.mass*body1.velocity+body2.mass*body2.velocity) # consevation de la quantité de mouvement 
            body2.velocity=1/masstot*(body1.mass*body1.velocity+body2.mass*body2.velocity)
            body1.position=1/masstot*(body1.mass*body1.position+body2.mass*body2.position) # Centre de gravité
            body2.position=1/masstot*(body1.mass*body1.position+body2.mass*body2.position) # Centre de gravité
            body1.draw_radius=max(body1.draw_radius,body2.draw_radius)
            body2.draw_radius=max(body1.draw_radius,body2.draw_radius)





        if type==1:                    #collision élastique
            m1=body1.mass
            m2=body2.mass
            v1=body1.velocity
            v2=body2.velocity
            nv1=body1.velocity.norm()
            nv2=body1.velocity.norm()
            teta1=np.arctan(v1.get_y()/v1.get_x())
            teta2=np.arctan(v2.get_y()/v2.get_x())
            teta1p=np.arctan((m1-m2)*np.tan(teta1)/(m1+m2)+2*m2*v2*np.sin(teta2)/((m1+m2)*v1*np.cos(teta1)))
            teta2p=np.arctan((m2-m1)*np.tan(teta2)/(m1+m2)+2*m1*v1*np.sin(teta1)/((m1+m2)*v2*np.cos(teta2)))
            v1p=np.sqrt(((m1-m2)*v1*np.sin(teta1)+2*m2*v2*np.sin(teta2))**2/(m1+m2)**2+(v1*np.cos(teta1))**2)
            v2p=np.sqrt(((m2-m2)*v2*np.sin(teta2)+2*m2*v2*np.sin(teta2))**2/(m1+m2)**2+(v2*np.cos(teta2))**2)
            body1.velocity.get_x()=v1p*cos(teta1)
            body1.velocity.get_y()=v1p*sin(teta1)
            body2.velocity.get_x()=v1p*cos(teta1)
            body2.velocity.get_y()=v1p*sin(teta1)



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

            Edit : to do the leapfrog solver, it is necessary to keep the previous accelerations in mind
            So we added
        """
        type=0
        N = len(self.world)
        deriv = Vector(4*N)
        for i in range(N) :
            deriv[2*i] = y0[(N+i)*2]
            deriv[2*i+1] = y0[(N+i)*2+1]
            acc_i = Vector2(0,0)
            pos_i = Vector2(y0[2*i],y0[2*i+1])  
            for j in range(N) :
                if i!=j :
                    #collision(type,self.world.get(i),type,self.world.get(j))
                    if (self.world.get(i).position.get_x()!=self.world.get(j).position.get_x()) or (self.world.get(i).position.get_y()!=self.world.get(j).position.get_y())

                        acc_i += gravitational_force(pos_i,1,Vector2(y0[2*j],y0[2*j+1]),self.world.get(j).mass)
            deriv[2*N+2*i] = acc_i.get_x()
            deriv[2*N+2*i+1] = acc_i.get_y()
            
        return deriv


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
