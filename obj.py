from pygame import *
import time
from svglibv import svg2retv

class Obj():
    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.x = 0
        self.y = 0
        self.stop = False
    def loop(self):
        self.update()
        self.draw()
    def update(self):
        pass
    def draw(self):
        pass
        
class Parede(Obj):
    def __init__(self, surface, base_img: str, color):
        super().__init__(surface)
        self.color = color
        self.surface = surface
        self.rects = svg2retv(base_img)
    def draw(self):
        for rects in self.rects:
            draw.rect(self.surface, self.color, rects)
    def collide(self, point):
        for rect in self.rects:
            collision = rect.collidepoint(point)
            if collision:
                return True 

class Sensor(Obj):
    def __init__(self, surface):
        super().__init__(surface)
    def draw(self):
        draw.circle(self.surface, (255, 0, 0), (self.x, self.y), 2)
    # def update(self):
    #     mouse_pos = mouse.get_pos()
    #     self.x = mouse_pos[0]
    #     self.y = mouse_pos[1]

import IA
from random import randint
import math

class Agente(Obj):
    def __init__(self, surface, paredes):
        super().__init__(surface)
        self.is_collide = False
        self.speed =  6#Velocidade em pixels por update
        self.angle = (math.pi*2/360)*(randint(1, 360))
        self.score = 0
        self.rede = IA.Rede()
        self.obst = paredes
        self.x = 100#randint(100, 550)
        self.y = 300#randint(100, 550)
        self.pos_rect = (self.x, self.y, 10, 10)
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.sensor_d = Sensor(surface)
        self.sensor_d.x = self.x + 20
        self.sensor_d.y = self.y + 5
        self.sensor_e = Sensor(surface)
        self.sensor_e.x = self.x
        self.sensor_e.y = self.y + 10
    def draw(self):
        self.pos_rect = (self.x, self.y, 10, 10)
        draw.circle(self.surface, self.color, (self.pos_rect[0], self.pos_rect[1]), 5)
        self.sensor_d.loop()
        self.sensor_e.loop()
    def update(self):
        inp_sensor = []
        self.sensor_d.x = self.x + math.cos(self.angle) * 15
        self.sensor_d.y = self.y + math.sin(self.angle) * 15
        if self.obst.collide((self.sensor_d.x, self.sensor_d.y)):
            inp_sensor.append(1)
        else:
            inp_sensor.append(0)
        self.sensor_e.x = self.x + math.cos(self.angle - math.pi/2) * 15
        self.sensor_e.y = self.y + math.sin(self.angle - math.pi/2) * 15
        if self.obst.collide((self.sensor_e.x, self.sensor_e.y)):
           inp_sensor.append(1)
        else:
           inp_sensor.append(0)
        inp_rede = inp_sensor
        out = self.rede.out(inp_rede)
        if out[0] > 0:
            self.angle += math.pi/30
        if out[1] > 0:
            self.angle -= math.pi/30
        if out[2] > 0:
            self.speed = 2
        if out[3] > 0:
            self.speed = -2
        self.x += math.cos(self.angle - math.pi/4) * self.speed
        self.y += math.sin(self.angle - math.pi/4) * self.speed
        