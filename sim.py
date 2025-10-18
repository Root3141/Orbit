import numpy as np
import matplotlib.pyplot as plt
import json

G = 6.67e-11  # Gravitational Constant


class SolarSystem:
    def __init__(self, size):
        self.size = size
        self.bodies = []
        self.fig = plt.figure(figsize=(self.size / 50, self.size / 50))
        self.ax = self.fig.add_subplot(1, 1, 1, projection="3d")
        self.fig.tight_layout()
        self.ax.view_init(30, 30)

    def add_body(self, body):
        self.bodies.append(body)

    def interact(self):
        for idx, first in enumerate(self.bodies):
            for second in self.bodies[idx + 1 :]:
                first.grav_acc(second)

    def move_all(self, dt=1):
        for body in self.bodies:
            body.move(dt)
        for body in self.bodies:
            body.force = np.zeros(3)
        self.interact()
        for body in self.bodies:
            old_acc = body.acc.copy()
            body.updateAcc()
            body.velocity += 0.5 * (old_acc + body.acc) * dt

    def draw_all(self):
        max_size = self.size / 2
        for body in self.bodies:
            max_dim = np.max(np.abs(body.position))
            if max_size < max_dim:
                max_size = max_dim
            body.draw()
        self.ax.set_xlim3d([-max_size, max_size])
        self.ax.set_ylim3d([-max_size, max_size])
        self.ax.set_zlim3d([-max_size, max_size])
        self.ax.axis("off")
        plt.pause(0.03)


class Celestial_Body:
    def __init__(
        self,
        solar_system,
        mass=0,
        size=0,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        label="",
        color="black"
    ):
        self.mass = mass
        self.size = size
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.solar_system = solar_system
        self.color = color
        self.solar_system.add_body(self)
        self.force = np.zeros(3)
        self.label = label
        self.acc = np.zeros(3)

    def move(self, dt=1):
        self.position += self.velocity * dt + 0.5 * (self.acc) * dt**2

    def draw(self):
        self.solar_system.ax.scatter(
            *self.position, marker="o", s=self.size, color=self.color
        )

    def grav_acc(self, other):
        dist = other.position - self.position
        dist_mag = np.linalg.norm(dist)
        if dist_mag == 0:
            return
        epsilon = 0  # Softening factor to avoid singularities
        force_mag = G * (self.mass * other.mass) / (dist_mag**2 + epsilon**2)
        force = dist * (force_mag / dist_mag)
        self.force = self.force + force
        other.force = other.force - force

    def updateAcc(self):
        self.acc = self.force / self.mass


class Star(Celestial_Body):
    def __init__(
        self,
        solar_system,
        mass=1000,
        size=50,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        label="",
        color="orange",
    ):
        super().__init__(solar_system, mass, size, position, velocity, label, color)


class Planet(Celestial_Body):
    def __init__(
        self,
        solar_system,
        mass=100,
        size=15,
        color="blue",
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        label="",
    ):
        super().__init__(solar_system, mass, size, position, velocity, label, color)


def create_solar_system(include=None):
    solar_system = SolarSystem(400)
    with open("static/bodies.json", "r") as f:
        bodies_data = json.load(f)
        if include:
            bodies_data = [b for b in bodies_data if b["label"] in include]
        for body in bodies_data:
            if body["type"]=="Star":
                cls = Star
            elif body["type"]=="Planet":
                cls = Planet
            else:
                cls = Celestial_Body
            cls(
                solar_system,
                mass=body["mass"],
                size=body["size"],
                position=tuple(body["position"]),
                velocity=tuple(body["velocity"]),
                label=body["label"],
                color=body["color"],
            )
    return solar_system


def sim_step(solar_system, dt):
    solar_system.move_all(dt)


def coordinates(solar_system):
    bodies = []
    scale = 6.5e8
    for body in solar_system.bodies:
        bodies.append(
            {
                "x": body.position[0] / scale,
                "y": body.position[1] / scale,
                "z": body.position[2] / scale,
                "size": body.size,
                "color": body.color,
                "label": body.label,
            }
        )
    return bodies


def main():
    solar_system = create_solar_system(include=["Sun", "Earth", "Mars"])
    dt = 60 * 60 * 24
    while True:
        sim_step(solar_system, dt)
        solar_system.draw_all()


if __name__ == "__main__":
    main()