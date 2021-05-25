from ..utils.vector import Vector, Vector2
from ..physics.engine import *
from simulator.physics.constants import G
import numpy as np

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
        for i in range(len(self.world)):
            b_i = self.world.get(i)
            b_i.position.set_x(y[2 * i])
            b_i.position.set_y(y[2 * i + 1])
            b_i.velocity.set_x(y[len(self.world)*2 + 2 * i])
            b_i.velocity.set_y(y[len(self.world)*2 + 2 * i + 1])
            
            mur(b_i)
            for j in range(i+1):
                if i!=j:
                    b_j = self.world.get(j)
                    colision(type,b_i,b_j)
        for i in range(len(self.world)):
            b_i = self.world.get(i)

            y[2 * i]=b_i.position.get_x()
            y[2 * i + 1]=b_i.position.get_y()
            

            y[len(self.world)*2 + 2 * i]=b_i.velocity.get_x()
            y[len(self.world)*2 + 2 * i + 1]=b_i.velocity.get_y()
    


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
        for i in range(len(self.world)):
            b_i = self.world.get(i)
            b_i.position.set_x(y[2 * i])
            b_i.position.set_y(y[2 * i + 1])
            b_i.velocity.set_x(y[len(self.world)*2 + 2 * i])
            b_i.velocity.set_y(y[len(self.world)*2 + 2 * i + 1])
            
            mur(b_i)
            for j in range(i+1):
                if i!=j:
                    b_j = self.world.get(j)
                    colision(type,b_i,b_j)
        for i in range(len(self.world)):
            b_i = self.world.get(i)

            y[2 * i]=b_i.position.get_x()
            y[2 * i + 1]=b_i.position.get_y()
            

            y[len(self.world)*2 + 2 * i]=b_i.velocity.get_x()
            y[len(self.world)*2 + 2 * i + 1]=b_i.velocity.get_y()   
        self.y0 = y
        self.t0 = t
        return y



def colision(type,body1,body2):
    rapport = 50
    if (body1.position -body2.position).norm()>0:                                                   # on verifie que les 2 concerné ne sont pas deja le resultat d'une fusion
        Ep=G*body1.mass*body2.mass/((body1.position -body2.position).norm())
        Ec=0.5*(body1.velocity.norm())**2*body1.mass+0.5*(body2.velocity.norm())**2*body2.mass


        if ((body1.position -body2.position).norm()*rapport >(body1.draw_radius+body2.draw_radius)):   #on regarde si la distanste entre 2 corps est suffisament faible pour qu'il y ai un choc 
            return None
        else:
            if Ep>Ec:   
                       #fusion de 2 étoile
                if body1.mass==0 or body2.mass==0:
                    return None
                else:
                    masstot=body1.mass+body2.mass
                    v=(body1.mass*body1.velocity+body2.mass*body2.velocity)/masstot # consevation de la quantité de mouvement 
                    pos=1/masstot*(body1.mass*body1.position+body2.mass*body2.position) # Centre de gravité
                    body1.position=pos
                    body2.position=pos
                    body1.velocity=v
                    body2.velocity=v
                    body1.mass=masstot
                    body2.mass=0
                    r=((body1.draw_radius)**(3)+(body2.draw_radius)**(3))**(1/3) #rayon résultant de la somme des volumes
                    body1.draw_radius=r
                    body2.draw_radius=0



            if Ec>=Ep and (body1.mass*body2.mass>0):   # cas de la collsion elastique
            
                r1=body1.draw_radius
                r2=body2.draw_radius
                R=r1+r2
                u=body1.position-body2.position # calcul de vecteurs distance puis normalisation
                r=(body1.position -body2.position).norm()*rapport
                e=u/r
                n=Rotation(np.pi/2,e) #calcul 
                m1=body1.mass
                m2=body2.mass
                c11=(m1-m2)/(m1+m2)
                c12=(2*m2/(m1+m2))
                c21=(m2-m1)/(m1+m2)
                c22=(2*m1)/(m1+m2)
                v1=body1.velocity
                v2=body2.velocity
                theta1=np.arccos(np.dot(v1,n)/v1.norm()) #angles de collision
                theta2=np.arccos(np.dot(v2,n)/v2.norm())
                thetap1=np.arctan(c11*np.tan(theta1)+c12*v2.norm()*np.sin(theta2)/(np.cos(theta1)*v1.norm())) #angles de rebond
                thetap2=np.arctan(c21*np.tan(theta2)+c22*v1.norm()*np.sin(theta1)/(np.cos(theta2)*v2.norm()))
                vp1=np.sqrt((v2.norm()*c12*np.sin(theta2)+c11*v1.norm()*np.sin(theta1))**2+v1.norm()*v1.norm()*np.cos(theta1)*np.cos(theta1)) #vitesse de rebond
                vp2=np.sqrt((v1.norm()*c22*np.sin(theta1)+c21*v2.norm()*np.sin(theta2))**2+v2.norm()*v2.norm()*np.cos(theta2)*np.cos(theta2))
                body2.vitesse=vp1*Rotation(thetap1,n) #vecteurs vitesse des corps
                body1.vitesse=vp2*Rotation(thetap2,n)
                milieu=(r1*body2.position+r2*body1.position)/R
                body1.position=milieu+r1*e 
                body2.position=milieu-r2*e
                body1.velocity=Vector2(vp1*np.cos(thetap1),vp1*np.sin(thetap1))
                body2.velocity=Vector2(vp2*np.cos(thetap2),vp2*np.sin(thetap2))


def mur(body):
    rapport = 50
    p=body.position
    v=body.velocity
    R=body.draw_radius
    vx=body.velocity.get_x()
    vy=body.velocity.get_y()
    if (p.get_x()*rapport-R)<-400:
        vx=-vx
        p.set_x((-400+R)/rapport)
    if (p.get_y()*rapport-R)<-300:
        vy=-vy
        p.set_y((-300+R)/rapport)
    if (p.get_x()*rapport+R)>400:
        vx=-vx
        p.set_x((400-R)/rapport)
    if (p.get_y()*rapport+R)>300:
        vy=-vy
        p.set_y((300-R)/rapport)
    body.velocity=Vector2(vx,vy)


def Rotation(theta, v):
    R=np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta),np.cos(theta)]])
    return np.dot(R,np.transpose(v))