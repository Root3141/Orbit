import numpy as np
import matplotlib.pyplot as plt
G = 6.67e-11 #Gravitational Constant

#Model of Solar System
class SolarSystem:
    def __init__(self, size):
        self.size=size
        self.bodies=[]
        self.fig = plt.figure(figsize=(self.size/50, self.size/50))
        self.ax = self.fig.add_subplot(1, 1, 1, projection='3d')
        self.fig.tight_layout()
        self.ax.view_init(30, 30)
    #adds celestial bodies to solar system  
    def add_body(self, body):
        self.bodies.append(body)
    #gravitational interaction amongst the bodies of solar system
    def interact(self):
        for idx, first in enumerate(self.bodies):
            for second in self.bodies[idx+1:]:
                first.grav_acc(second)
    #moves all the bodies      
    def move_all(self, dt=1):
        for body in self.bodies:
            body.move(dt)
            
    #refreshes plot
    def draw_all(self):
        #self.ax.clear()
        max_size = self.size/2
        for body in self.bodies:
            max_dim = np.max(np.abs(body.position))
            if max_size < max_dim:
                max_size = max_dim
            body.draw()
        self.ax.set_xlim3d([-max_size, max_size])
        self.ax.set_ylim3d([-max_size, max_size])
        self.ax.set_zlim3d([-max_size, max_size])
        self.ax.axis('off')
        plt.pause(0.01)

#Model of celestial bodies(planets, stars, etc)
class Celestial_Body:
    def __init__(self,solar_system, mass=0, size=0, position = (0,0,0), velocity = (0,0,0)):
        self.mass = mass
        self.size = size
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.solar_system = solar_system
        self.color = "black"
        self.solar_system.add_body(self)
        self.force = np.zeros(3)
    def move(self, dt=1):
        # update velocity and position using semi-implicit Euler method
        self.velocity += (self.force/self.mass)*dt
        self.position += self.velocity*dt
    def draw(self):
        self.solar_system.ax.scatter(*self.position, marker = 'o', s = self.size, color = self.color)
    #accelaration due to gravity
    def grav_acc(self, other):
        dist = other.position - self.position
        dist_mag = np.linalg.norm(dist)
        if dist_mag==0:
            return
        epsilon = 0
        force_mag = G*(self.mass*other.mass)/(dist_mag**2+epsilon**2)
        force=dist*(force_mag/dist_mag)
        self.force = self.force + force
        other.force = other.force - force

#Model of Star
class Star(Celestial_Body):
    def __init__(self, solar_system, mass=1000, size=50, position=(0, 0, 0), velocity=(0, 0, 0)):
        super().__init__(solar_system, mass, size, position, velocity)
        self.color = "orange"

#Model of Planet
class Planet(Celestial_Body):
    def __init__(self, solar_system, mass=100, size=15, color = "blue", position=(0, 0, 0), velocity=(0, 0, 0)):
        super().__init__(solar_system, mass, size, position, velocity)
        self.color = color
def main():    
    solar_system = SolarSystem(400)
    sun = Star(solar_system, mass=1.989e30, size=50, position=(0, 0, 0), velocity=(0, 0, 0))
    earth = Planet(solar_system, mass=5.972e24, size=10, color="blue", position=(1.496e11, 0, 0), velocity=(0, 29780, 0))
    mars = Planet(solar_system, mass=6.39e23, size=7, color="red", position=(2.279e11, 0, 0), velocity=(0, 24070, 0))
    dt = 60*60*24
    while True:
        # Reset forces
        for body in solar_system.bodies:
            body.force = np.zeros(3)
        solar_system.interact()
        solar_system.move_all(dt=dt)
        solar_system.draw_all()

if __name__ == "__main__":
    main()
