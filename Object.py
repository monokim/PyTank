import random
import math
import pygame
import Util
screen_width = 1200
screen_height = 800
class Tank:
    size = 30
    alive = True
    is_fire = False
    bullet = None
    accel = 0
    speed = 10
    c_len = 50
    def __init__(self, side, screen):
        self.side = side
        self.screen = screen
        if side == 0:
            self.position = [screen_width // 2, screen_height // 2]
            self.color = (0, 0, 255)
        else:
            self.position = [random.randrange(50, screen_width - 50), random.randrange(50, screen_height - 50)]
            self.color = (255, 0, 0)
            
        self.angle = (math.degrees(math.atan2(random.uniform(-1, 1), random.uniform(-1, 1))) + 360) % 360
        self.c_x = self.position[0] + math.cos(math.radians(self.angle)) * self.c_len    # cannon_x
        self.c_y = self.position[1] + math.sin(math.radians(self.angle)) * self.c_len    # cannon_y
    def draw(self):
        pygame.draw.circle(self.screen, self.color, [int(self.position[0]), int(self.position[1])], self.size)
        self.draw_cannon()

    def draw_cannon(self):
        # draw cannon
        pygame.draw.line(self.screen, (0, 0, 0), (self.position[0], self.position[1]), (self.c_x,self.c_y), 10)
    
    def move(self):
        self.position[0] += math.cos(math.radians(self.angle)) * self.speed
        self.position[1] += math.sin(math.radians(self.angle)) * self.speed

    def fire(self):
        if self.is_fire == False:
            self.is_fire = True

    def check_status(self):
        self.angle = (self.angle + 360) % 360
        direction = [math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))]
        if self.position[0] <= 0 or self.position[0] >= screen_width - 50:
            direction[0] *= -1
            self.angle = (math.degrees(math.atan2(direction[1], direction[0])) + 360) % 360
        
        if self.position[1] <= 0 or self.position[1] >= screen_height - 50:
            direction[1] *= -1
            self.angle = (math.degrees(math.atan2(direction[1], direction[0])) + 360) % 360

        self.c_x = self.position[0] + math.cos(math.radians(self.angle)) * self.c_len    # cannon_x
        self.c_y = self.position[1] + math.sin(math.radians(self.angle)) * self.c_len    # cannon_y
  

    def update_status(self):
        self.check_status()
        self.move()

    def predict_hit(self, b):
        abs_angle = Util.get_angle(self.position.copy(), b.position.copy())
        a1 = (b.angle - abs_angle + 360) % 360
        a2 = (abs_angle - b.angle + 360) % 360
        if a1 > a2:
            big = a1
            small = a2
        else:
            big = a2
            small = a1
        if small <= 15 or big >= 360 - 15:
            return 1
        return 0

    def emergency_avoid(self, b):
        # + : right, - left
        angle_diff = (self.angle - b.angle + 360) % 360
        if angle_diff < 45:
            return 1
        elif angle_diff > 135 and angle_diff <= 180:
                return 0
        elif angle_diff > 180 and angle_diff <= 225:
                return 1
        elif angle_diff > 315:
            return 0
        else:
            return 2
        

class Bullet:
    speed = 50
    alive = 1
    angle = 0
    size = 5

    # for train
    min_dist = 9999
    hit = False

    def set_new_direction(self):
        self.angle = (math.degrees(math.atan2(random.uniform(-1, 1), random.uniform(-1, 1))) + 360) % 360

    def __init__(self, screen, position, angle = 0):
        self.screen = screen
        self.position = position
        if angle == 0:
            self.angle = (math.degrees(math.atan2(random.uniform(-1, 1), random.uniform(-1, 1))) + 360) % 360
        else:
            self.angle = angle

    def move(self):
        self.position[0] += math.cos(math.radians(self.angle)) * self.speed
        self.position[1] += math.sin(math.radians(self.angle)) * self.speed

    def draw(self):
        pygame.draw.circle(self.screen, (0, 0, 0), [int(self.position[0]), int(self.position[1])], self.size)

    def check_status(self):
        if self.position[0] <= 0 or self.position[0] >= screen_width or \
            self.position[1] <= 0 or self.position[1] >= screen_height:
            self.alive = 0
    
    def update_status(self):
        self.check_status()
        self.move()
