from turtle import pos

import pygame
from pygame.locals import *
from pygame.draw import circle, line


class DrawRede:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont('freestanding.ttf', 50)
        self.qtLayer = 0

    def draw(self, tela, player):

        text = self.font.render('GeeksForGeeks', True, (0, 255, 0))

        maior_c = 0

        for c in player.rede.last_process:
            tm = len(c)
            if tm > maior_c:
                maior_c = tm

        pygame.draw.rect(tela, (200, 200, 200), Rect(self.x, self.y, len(player.rede.last_process) * 60, maior_c * 50),0, 10)
        self.draw_net(tela, player, maior_c)

    def draw_net(self, tela, player, maior_c):
        pos_circle = []
        outputs = []
        for cam in player.rede.last_process:
            pos_circle.append(self.draw_layer(tela, cam, maior_c))
            outputs += cam
        self.qtLayer = 0
        self.draw_lines(tela, pos_circle, outputs)
        self.draw_circle(tela, pos_circle, outputs)

    def draw_lines(self, tela, pos_circle, out: list):
        j = -1
        for i in range(0, len(pos_circle) - 1):
            for pos_i in pos_circle[i]:
                j += 1
                for pos_f in pos_circle[i+1]:
                    line(tela, (out[j] * 255, 0, 0), pos_i, pos_f)

    def draw_circle(self, tela, pos_circle, out: list):
        j = -1
        for cam in pos_circle:
            for pos in cam:
                j += 1
                circle(tela, (out[j] * 255, 0, 0), pos, 10)

    def draw_layer(self, tela, out_perc: list, maior_c: int) -> list:
        pos_circle = []
        self.qtLayer += 1
        espace = (maior_c * 50) / (len(out_perc) + 1)
        qt_perc = 1
        for out in out_perc:
            pos = (self.x - 30 + self.qtLayer * 60, self.y + qt_perc * espace)
            pos_circle.append(pos)
            qt_perc += 1
        return pos_circle
