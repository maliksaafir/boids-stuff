from p5 import *

class Boid():
    def __init__(self, x, y, width, height):
        self.color = 0
        self.height = height
        self.radius = 25
        self.max_force = 1
        self.max_speed = 10
        self.perception = 100
        self.position = Vector(x, y)
        self.width = width
        vec = (np.random.rand(2) - 0.5) * 10 # random velocity between (-5, -5) and (5, 5)
        self.velocity = Vector(*vec)
        vec = (np.random.rand(2) - 0.5) * 2 # random acceleration between (-1, -1) and (1, 1)
        self.acceleration = Vector(*vec)

    def edges(self):
        if self.position.x < 0:
            self.position.x = self.width
        elif self.position.x > self.width:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = self.height
        elif self.position.y > self.height:
            self.position.y = 0

    def show(self):
        no_stroke()
        fill(self.color)
        circle((self.position.x, self.position.y), radius=self.radius)

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

    def apply_behaviour(self, flock):
        separation = self.separate(flock)
        alignment = self.align(flock)
        cohesion = self.cohere(flock)
        self.acceleration += separation
        self.acceleration += alignment
        self.acceleration += cohesion
        if np.linalg.norm(self.acceleration) > self.max_force:
            self.acceleration = (self.acceleration / np.linalg.norm(self.acceleration)) * self.max_force
        
    def separate(self, flock):
        steering = Vector(0, 0)
        total = 0
        avg_vec = Vector(0, 0)
        steering = Vector(0, 0)
        for boid in flock:
            distance = np.linalg.norm(boid.position - self.position)
            if self.position != boid.position and distance < self.perception:
                away = self.position - boid.position
                away /= distance
                avg_vec += away
                total += 1
        
        if total > 0:
            avg_vec /= total
            avg_vec = Vector(*avg_vec)
            if np.linalg.norm(avg_vec) > 0:
                avg_vec = (avg_vec / np.linalg.norm(avg_vec)) * self.max_speed
            steering = avg_vec - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering)) * self.max_force
        
        return steering

    def align(self, flock):
        steering = Vector(0, 0)
        total = 0
        avg_vel = Vector(0, 0)
        for boid in flock:
            if np.linalg.norm(boid.position - self.position) < self.perception:
                avg_vel += boid.velocity
                total += 1
        
        if total > 0:
            avg_vel /= total
            avg_vel = Vector(*avg_vel)
            if np.linalg.norm(avg_vel) > 0:
                avg_vel = avg_vel / np.linalg.norm(avg_vel) * self.max_speed
            steering = avg_vel - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering)) * self.max_force

        return steering

    def cohere(self, flock):
        center_of_mass = Vector(0, 0)
        total = 0
        steering = Vector(0, 0)
        for boid in flock:
            if np.linalg.norm(boid.position - self.position) < self.perception:
                center_of_mass += boid.position
                total += 1

        if total > 0:
            center_of_mass /= total
            center_of_mass = Vector(*center_of_mass)
            vec_to_com = center_of_mass - self.position

            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
                steering = vec_to_com - self.velocity
                if np.linalg.norm(steering) > self.max_force:
                    steering = (steering / np.linalg.norm(steering)) * self.max_force

        return steering

