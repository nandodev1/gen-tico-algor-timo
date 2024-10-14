import pygame
from obj import *
import conf
import sys
import time
import draw_rede
import AG

class Loop:
    def __init__(self, surface):
        self.alg_gen = AG.AG()
        self.draw_rede = draw_rede.DrawRede(825, 20)
        self.best_agente = None
        self.quant_agentes = 500
        self.qt_loop_epoca = 1_000
        self.qt_iter = 0
        self.surface = surface
        self.parede = Parede(surface, 'tst.svg',  (255, 255, 255))
        self.checkpoints = Parede(surface, 'checkpoints.svg', (0, 155, 0))
        self.sensor = Sensor(surface)
        self.agentes = []
        #ag = self.load_net()
        #self.agentes.append(ag)
        for i in range(0, self.quant_agentes):
            self.agentes.append(Agente(surface, self.parede))
    def loop(self):
        my_font = pygame.font.SysFont('Comic Sans MS', 40)
        self.surface.blit(my_font.render('Epóca: ' + str(self.qt_iter) + '/' + str(self.qt_loop_epoca), False, (255, 255, 255)), (50,10))
        if pygame.mouse.get_pressed() == (True, False, False):
            agent = Agente(self.surface, self.parede)
            pos_m = pygame.mouse.get_pos()
            agent.x = pos_m[0]
            agent.y = pos_m[1]
            self.agentes.append(agent)
        if pygame.mouse.get_pressed() == (False, False, True):
            pos_m = pygame.mouse.get_pos()
            agent.x = pos_m[0]
            agent.y = pos_m[1]
        self.parede.loop()
        self.checkpoints.loop()
        self.sensor.loop()
        for ag in self.agentes:
            ag.loop()
        for rect in self.checkpoints.rects:
            for ag in self.agentes:
                collision = rect.colliderect((ag.pos_rect[0] -5, ag.pos_rect[1] - 5, ag.pos_rect[2], ag.pos_rect[3]))
                if collision and not ag.is_collide:
                    ag.score += 1
                    ag.is_collide = True
                    #self.agentes.remove(ag)
                else:
                    ag.is_collide = False
        self.qt_iter += 1
        if self.qt_iter >= self.qt_loop_epoca:
            self.qt_iter = 0
            sys.stdout.write("\n=======================Fim de epoca========================\n")
            agentes_remover = []
            for ag in self.agentes:
                if ag.score == 0:
                    agentes_remover.append(ag)
            ags = self.select_ag_cross()
            self.save_net(ags)
            for ag in agentes_remover:
                self.agentes.remove(ag)
            #Zera score para iniciar nova epoca
            for ag in self.agentes:
                ag.score = 0
            self.alg_gen.crosover()
            self.alg_gen.load_nets(self.surface, self.parede)
        self.draw_rede.draw(self.surface, self.agentes[0])

    def save_net(self, ag):
        arq = open('pesos.txt', 'w')
        arq.write(str(ag.score)+' ')
        for layer in ag.rede.rede:
            for perc in layer.perceptrons:
                arq.write(str(perc.bias)+' ')
                for peso in perc.pesos:
                    arq.write(str(peso)+' ')
        arq.close()

    def save_net(self, ags: tuple):
        arq = open('pesos.txt', 'w')
        arq.write(str(ags[0].score)+' ')
        for layer in ags[0].rede.rede:
            for perc in layer.perceptrons:
                arq.write(str(perc.bias)+' ')
                for peso in perc.pesos:
                    arq.write(str(peso)+' ')
        arq.write('\n')
        arq.write(str(ags[1].score)+' ')
        for layer in ags[1].rede.rede:
            for perc in layer.perceptrons:
                arq.write(str(perc.bias)+' ')
                for peso in perc.pesos:
                    arq.write(str(peso)+' ')
        arq.write('\n')
        arq.close()

    def ordenarLista(self, list_agente: list):
        val = []
        for ag in list_agente:
            val.append(ag.score)
        val.sort()
        val_min = val[-1]
        return val_min
    
    def select_ag_cross(self)-> tuple:
        ag_a = Agente(self.surface, self.parede)
        ag_b = Agente(self.surface, self.parede)
        for ag in self.agentes:
            if ag.score > ag_a.score:
                ag_a = ag
            elif ag.score > ag_b.score:
                ag_b = ag
        return (ag_a, ag_b)