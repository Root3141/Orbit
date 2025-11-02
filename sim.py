import numpy as np
import matplotlib.pyplot as plt
import json

G = 6.67e-11  # Gravitational Constant


class SolarSystem:
    def __init__(self, size, enable_trails=False, visualize=False):
        self.size = size
        self.bodies = []
        self.visualize = visualize
        self.enable_trails = enable_trails
        if visualize:
            self.fig = plt.figure(figsize=(8, 8))
            self.ax = self.fig.add_subplot(1, 1, 1, projection="3d")
            self.fig.tight_layout()
            self.ax.view_init(30, 30)
            self.ax.set_facecolor("#181818")
            self.fig.patch.set_facecolor("black")
            self._step_count = 0
            plt.ion()

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

    def setup_plot(self):
        if not self.visualize:
            return
        self.resize_axes()
        for body in self.bodies:
            body.init_draw(self.enable_trails)
        self.ax.legend(
            [b.scatter for b in self.bodies],
            [b.label for b in self.bodies],
            loc="upper right",
            fontsize="small",
        )

    def resize_axes(self, margin=0.2):
        positions = np.array([body.position for body in self.bodies])
        max_dist = np.max(np.abs(positions))
        target_size = max_dist * (1 + margin)
        if target_size > self.size:
            self.size = target_size
            half = self.size / 2
            self.ax.set_xlim3d([-half, half])
            self.ax.set_ylim3d([-half, half])
            self.ax.set_zlim3d([-half, half])
            self.ax.axis("off")
            self.ax.figure.canvas.draw_idle()
            self.ax.figure.canvas.flush_events()

    def draw_all(self):
        if not self.visualize:
            return False
        if not plt.fignum_exists(self.fig.number):
            return
        for body in self.bodies:
            body.draw()
        self._step_count += 1
        if self._step_count >= 25:
            self.resize_axes()
            self._step_count = 0
        plt.pause(0.01)
        return True


class Celestial_Body:
    def __init__(
        self,
        solar_system,
        mass=0,
        size=0,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        label="",
        color="black",
    ):
        self.mass = mass
        self.size = size
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.solar_system = solar_system
        self.color = color
        self.force = np.zeros(3)
        self.label = label
        self.acc = np.zeros(3)

        self.scatter = None
        self.trail = None
        self.trail_history = []
        self.trail_length = 400

        solar_system.add_body(self)

    def move(self, dt=1):
        self.position += self.velocity * dt + 0.5 * (self.acc) * dt**2

    def init_draw(self, enable_trail=False):
        self.scatter = self.solar_system.ax.scatter(
            *self.position,
            marker="o",
            s=self.size,
            color=self.color,
            label=self.label,
            depthshade=True
        )
        if enable_trail:
            self.trail = self.solar_system.ax.plot(
                [self.position[0]],
                [self.position[1]],
                [self.position[2]],
                color=self.color,
                linewidth=1,
            )
            self.trail_history = [self.position.copy()] * self.trail_length

    def draw(self):
        if self.scatter is None:
            self.init_draw(self.solar_system.enable_trails)
        else:
            self.scatter._offsets3d = (
                np.array([self.position[0]]),
                np.array([self.position[1]]),
                np.array([self.position[2]]),
            )
        if self.trail is not None:
            self.trail_history.append(self.position.copy())
            if len(self.trail_history) > self.trail_length:
                self.trail_history.pop(0)
            xs, ys, zs = np.transpose(self.trail_history)
            self.trail[0].set_data(xs, ys)
            self.trail[0].set_3d_properties(zs)

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


def create_solar_system(include=None, size=400, enable_trails=False, visualize=False):
    solar_system = SolarSystem(size, enable_trails=enable_trails, visualize=visualize)
    with open("static/bodies.json", "r") as f:
        bodies_data = json.load(f)
        if include:
            bodies_data = [b for b in bodies_data if b["label"] in include]
        for body in bodies_data:
            if body["type"] == "Star":
                cls = Star
            elif body["type"] == "Planet":
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
    solar_system = create_solar_system(
        include=["Sun", "Earth", "Mars"], enable_trails=True, visualize=True
    )
    solar_system.setup_plot()
    dt = 60 * 60 * 24
    while True:
        sim_step(solar_system, dt)
        if not solar_system.draw_all():
            break


if __name__ == "__main__":
    main()
