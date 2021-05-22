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
        y = self.solver.integrate(self.t + h)
       


        self.t += h


 # type=0
        
        # for i in range(len(self.world)):
        #     b_i = self.world.get(i)

        #     b_i.position.set_x(y[2 * i])
        #     b_i.position.set_y(y[2 * i + 1])
            

        #     b_i.velocity.set_x(y[len(self.world) + 2 * i])
        #     b_i.velocity.set_y(y[len(self.world) + 2 * i + 1])
        #     print(b_i.velocity)
        #     #mur(b_i)
        #     for j in range(i+1):
        #         if i!=j:
        #             b_j = self.world.get(j)
        #             colision(type,b_i,b_j)
# def colision(type,body1,body2):
#     rapport = 50
#     if ((body1.position -body2.position).norm()*rapport >(body1.draw_radius+body2.draw_radius)):

#         return None
#     else:
#         if type==0:   
#                    #fusion de 2 étoile
#             print(1)
#             masstot=body1.mass+body2.mass
#             v=1/masstot*(body1.mass*body1.velocity+body2.mass*body2.velocity) # consevation de la quantité de mouvement 
#             pos=1/masstot*(body1.mass*body1.position+body2.mass*body2.position) # Centre de gravité
#             body1.position=pos
#             body2.position=pos
#             body1.velocity=v
#             body2.velocity=v
#             body2.mass=masstot
#             body2.mass=0
#             body1.draw_radius=max(body1.draw_radius,body2.draw_radius)
#             body2.draw_radius=max(body1.draw_radius,body2.draw_radius)
            
            





#         if type==1:   
#             # print("4")                 #collision élastique
#             # m1=body1.mass
#             # m2=body2.mass
#             # v1=body1.velocity
#             # v2=body2.velocity
#             # nv1=body1.velocity.norm()
#             # nv2=body1.velocity.norm()
#             # teta1=-np.arctan(v1.get_y()/v1.get_x())
#             # teta2=-np.arctan(v2.get_y()/v2.get_x())
#             # teta1p=np.arctan((m1-m2)*np.tan(teta1)/(m1+m2)+2*m2*nv2*np.sin(teta2)/((m1+m2)*nv1*np.cos(teta1)))
#             # teta2p=np.arctan((m2-m1)*np.tan(teta2)/(m1+m2)+2*m1*nv1*np.sin(teta1)/((m1+m2)*nv2*np.cos(teta2)))
#             # v1p=np.sqrt(((m1-m2)*nv1*np.sin(teta1)+2*m2*nv2*np.sin(teta2))**2/(m1+m2)**2+(nv1*np.cos(teta1))**2)
#             # v2p=np.sqrt(((m2-m2)*nv2*np.sin(teta2)+2*m2*nv2*np.sin(teta2))**2/(m1+m2)**2+(nv2*np.cos(teta2))**2)
#             # V1=Vector2(v1p*np.cos(teta1p),v1p*np.sin(teta1p))
#             # V2=Vector2(v2p*np.cos(teta2p),v2p*np.sin(teta2p))
#             # print((V1-v1).norm())
#             # body1.velocity=V1
#             # body2.velocity=V2
#             r1=body1.draw_radius
#             r2=body2.draw_radius
#             R=r1+r2
#             u=body1.position-body2.position # calcul de vecteurs distance puis normalisation
#             r=(body1.position -body2.position).norm()*rapport
#             e=u/r
#             n=Rotation(np.pi/2,e) #calcul 
#             m1=body1.mass
#             m2=body2.mass
#             c11=(m1-m2)/(m1+m2)
#             c12=(2*m2/(m1+m2))
#             c21=(m2-m1)/(m1+m2)
#             c22=(2*m1)/(m1+m2)
#             v1=body1.velocity
#             v2=body2.velocity
#             theta1=np.arccos(np.dot(v1,n)/v1.norm()) #angles de collision
#             theta2=np.arccos(np.dot(v2,n)/v2.norm())
#             thetap1=np.arctan(c11*np.tan(theta1)+c12*v2.norm()*np.sin(theta2)/(np.cos(theta1)*v1.norm())) #angles de rebond
#             thetap2=np.arctan(c21*np.tan(theta2)+c22*v1.norm()*np.sin(theta1)/(np.cos(theta2)*v2.norm()))
#             vp1=np.sqrt((v2.norm()*c12*np.sin(theta2)+c11*v1.norm()*np.sin(theta1))**2+v1.norm()*v1.norm()*np.cos(theta1)*np.cos(theta1)) #vitesse de rebond
#             vp2=np.sqrt((v1.norm()*c22*np.sin(theta1)+c21*v2.norm()*np.sin(theta2))**2+v2.norm()*v2.norm()*np.cos(theta2)*np.cos(theta2))
#             body2.vitesse=vp1*Rotation(thetap1,n) #vecteurs vitesse des corps
#             body1.vitesse=vp2*Rotation(thetap2,n)
#             milieu=(r1*body2.position+r2*body1.position)/R
#             body1.position=milieu+r2*e 
#             body2.position=milieu-r1*e
#             body1.velocity=Vector2(vp1*np.cos(thetap1),vp1*np.sin(thetap1))
#             body2.velocity=Vector2(vp2*np.cos(thetap2),vp2*np.sin(thetap2))




# def mur(body):
#     p=body.position
#     v=body.velocity
#     R=body.draw_radius
#     vx=body.velocity.get_x()
#     vy=body.velocity.get_y()
#     if (p.get_x()+R)<-4:
#         print(1)
#         vx=-vx
#     if (p.get_y()+R)<-0:
#         print(2)
#         vy=-vy
#     if (p.get_x()+R)>8:
#         print(3)
#         print(p.get_x())
#         vx=-vx
#     if (p.get_y()+R)>8:
#         print(4)
#         print(p.get_x())
#         vy=-vy
#     body.velocity=Vector2(vx,vy)


# def Rotation(theta, v):
#     R=np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta),np.cos(theta)]])
#     return np.dot(R,np.transpose(v))