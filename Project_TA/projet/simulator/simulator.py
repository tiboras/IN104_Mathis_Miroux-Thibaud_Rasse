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
        type=0
        
        for i in range(len(self.world)):
            b_i = self.world.get(i)

            b_i.position.set_x(y[2 * i])
            b_i.position.set_y(y[2 * i + 1])

            b_i.velocity.set_x(y[len(self.world) + 2 * i])
            b_i.velocity.set_y(y[len(self.world) + 2 * i + 1])
            for j in range(len(self.world)):
                b_j = self.world.get(j)
                colision(type,b_i,b_j)


        self.t += h



def colision(type,body1,body2):
    if (body1.position -body2.position).norm() >(body1.draw_radius+body1.draw_radius):
        print ("3")
        return None
    else:
        if type==0:                  #fusion de 2 étoile
            masstot=body1.mass+body2.mass
            body1.mass=masstot
            body2.mass=0
            v=1/masstot*(body1.mass*body1.velocity+body2.mass*body2.velocity) # consevation de la quantité de mouvement 
            pos=1/masstot*(body1.mass*body1.position+body2.mass*body2.position) # Centre de gravité
            body1.position=pos
            body2.position=pos
            body1.velocity=v
            body2.velocity=v
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
            V1=Vector2(v1p*cos(teta1),v1p*sin(teta1))
            V2=Vector2(v2p*cos(teta1),v2p*sin(teta1))
            body1.velocity=V1
            body2.velocity=V2
