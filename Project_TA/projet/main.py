#!/usr/bin/env python3

from simulator import Simulator, World, Body
from simulator.utils.vector import Vector, Vector2
from simulator.solvers.solver import DummySolver
from simulator.physics.engine import DummyEngine
from simulator.graphics import Screen

import pygame as pg
import numpy as np 

#cette fonction sert à mettre à jour y0 qui change de dimension lorsqu'on ajoute de nouveaux corps.
def add_body(body,y0,N) :
    y0_bis = Vector(4*N)
    y0_bis[:2*(N-1)] = y0[:2*(N-1)]
    y0_bis[2*(N-1)+2-1 :4*N-2] = y0[2*(N-1)-1:]
    y0_bis[2*N-2] = body.position.get_x()
    y0_bis[2*N-1] = body.position.get_y()
    y0_bis[4*N-2] = body.velocity.get_x()
    y0_bis[4*N-1] = body.velocity.get_y()
    return y0_bis

if __name__ == "__main__":
    #tuple(np.random.randint(256, size=3))

    #faire une boucle avec que des add pour afficher plein de corps
    b1 = Body(Vector2(0, 0),
              velocity=Vector2(0.00001, 0.00001),
              mass=10, color=tuple(np.random.randint(256, size=3)),
              draw_radius=20)
    b2 = Body(Vector2(1,1),
              velocity=Vector2(0.0001,-0.2),
              mass=5,
              color = tuple(np.random.randint(256, size=3)),
                draw_radius=20)


    world = World()
    world.add(b1)
    world.add(b2)


    simulator = Simulator(world, DummyEngine, DummySolver)

    screen_size = Vector2(800, 600)
    screen = Screen(screen_size,
                    bg_color=(0, 0, 0),
                    caption="Simulator")
    screen.camera.scale = 50

    # this coefficient controls the speed
    # of the simulation
    time_scale = 10
    mv_cam_pas = 0.1
    print("Start program")
    while not screen.should_quit:
        dt = screen.tick(60)

        # simulate physics
        delta_time = time_scale * dt / 1000
        simulator.step(delta_time)
        # read events
        screen.get_events()
        move_camera = Vector2(0, 0)
        # handle events
        #   scroll wheel and movements
        if screen.get_wheel_up():
            screen.camera.scale *= 1.1
        elif screen.get_wheel_down():
            screen.camera.scale *= 0.9
        elif screen.get_key_right():
            move_camera -= Vector2(mv_cam_pas,0)
        elif screen.get_key_down():
            move_camera -= Vector2(0,mv_cam_pas)
        elif screen.get_key_left():
            move_camera -= Vector2(-mv_cam_pas,0)
        elif screen.get_key_up():
            move_camera -= Vector2(0,-mv_cam_pas)
        elif screen.get_right_mouse() :
            pos_ecran = screen.camera.from_screen_coords(screen.mouse_position)
            b_add = Body(pos_ecran,velocity=Vector2(0.0001, 0.0001),
                 mass=1,
                color = tuple(np.random.randint(256, size=3)),
                draw_radius=10)
            world.add(b_add)
            simulator.solver.y0 = add_body(b_add, simulator.solver.y0,len(world))

        screen.camera.position += move_camera
        # draw current state
        screen.draw(world)

        # draw additional stuff
        screen.draw_corner_text("Time: %f" % simulator.t)

        # show new state
        screen.update()

    screen.close()
    print("Done")
