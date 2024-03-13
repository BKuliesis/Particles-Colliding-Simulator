import pygame
import sys
import random


class Object:
    def __init__(self, radius, mass, horizontal_position, initial_velocity):
        self.radius = radius
        self.mass = mass
        self.horizontal_position = horizontal_position
        self.velocity = initial_velocity

    def get_radius(self):
        return self.radius

    def get_mass(self):
        return self.mass

    def get_horizontal_position(self):
        return self.horizontal_position

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity

    def update_horizontal_position(self):
        self.horizontal_position += self.velocity * (60/144)


class Wall(Object):
    def __init__(self, horizontal_position):
        super().__init__(0, float("inf"), horizontal_position, 0)


class Collision:
    def __init__(self, object1, object2, elasticity):
        self.objects = [object1, object2]
        self.elasticity = elasticity

    def get_distance(self):
        return abs(self.objects[0].get_horizontal_position() - self.objects[1].get_horizontal_position())

    def check_if_collision(self):
        if self.get_distance() <= self.objects[0].get_radius() + self.objects[1].get_radius():
            return True
        collision_with_wall, index = self.collision_with_wall()
        if collision_with_wall:
            position_of_wall = self.objects[index].get_horizontal_position()
            index_of_moving_object = (index + 1) % 2
            position_of_moving_object = self.objects[index_of_moving_object].get_horizontal_position()
            if self.objects[index_of_moving_object].get_velocity() < 0 and position_of_moving_object < 20:
                return True
            elif self.objects[index_of_moving_object].get_velocity() > 0 and position_of_moving_object > 780:
                return True
        return False

    def collision_with_wall(self):
        for index, collision_object in enumerate(self.objects):
            if isinstance(collision_object, Wall):
                return True, index
        return False, None

    def operate_collision(self):
        collision_with_wall, index = self.collision_with_wall()
        if collision_with_wall:
            index_of_moving_object = (index + 1) % 2
            new_velocity = self.elasticity * self.objects[index_of_moving_object].get_velocity() * (-1)
            self.objects[index_of_moving_object].set_velocity(new_velocity)
        else:
            masses = [self.objects[0].get_mass(), self.objects[1].get_mass()]
            initial_velocities = [self.objects[0].get_velocity(), self.objects[1].get_velocity()]
            velocity1 = ((masses[0]*initial_velocities[0]) + (masses[1]*initial_velocities[1]) - (self.elasticity*masses[1]*(abs(initial_velocities[1] - initial_velocities[0])))) / (masses[0]+masses[1])
            velocity2 = ((masses[0]*initial_velocities[0]) + (masses[1]*initial_velocities[1]) + (self.elasticity*masses[0]*(abs(initial_velocities[1] - initial_velocities[0])))) / (masses[0]+masses[1])
            self.objects[0].set_velocity(velocity1)
            self.objects[1].set_velocity(velocity2)


def animation(walls, objects, screen, screen_height):
    white = (255, 255, 255)
    colours = [(255, 255, 0), (0, 255, 255), (255, 0, 255)]
    wall_height = int(screen_height * 0.5)
    for wall in walls:
        horizontal_position = wall.get_horizontal_position()
        pygame.draw.rect(screen, white, (horizontal_position, int((screen_height - wall_height) / 2), 5, wall_height))
    for colour_index, object_to_display in enumerate(objects):
        horizontal_position = int(object_to_display.get_horizontal_position())
        vertical_position = int(screen_height / 2)
        pygame.draw.circle(screen, colours[colour_index], (horizontal_position, vertical_position), object_to_display.get_radius())


def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Collision Simulator")
    CLOCK = pygame.time.Clock()

    radius = 25

    objects = [Wall(20), Wall(SCREEN_WIDTH - 20), Object(radius, 10, 100, 5), Object(radius, 10, 400, -2),
               Object(radius, 10, 500, -1)]

    collisions = []

    for index1 in range(len(objects) - 1):
        for index2 in range(index1 + 1, len(objects)):
            if not (isinstance(objects[index1], Wall) and isinstance(objects[index2], Wall)) and objects[index1] != objects[index2]:
                collisions.append(Collision(objects[index1], objects[index2], 1))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((0, 0, 0))

        for collision in collisions:
            if collision.check_if_collision():
                collision.operate_collision()

        for moving_object in objects:
            moving_object.update_horizontal_position()

        animation(objects[:2], objects[2:], SCREEN, SCREEN_HEIGHT)

        pygame.display.update()
        CLOCK.tick(144)



if __name__ == "__main__":
    main()
