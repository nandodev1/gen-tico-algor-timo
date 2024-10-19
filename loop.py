import pygame
from obj import *
import conf
import sys
import time
import draw_rede
import AG

class Loop:
    def __init__(self, surface):
        self.qt_epoca = 0
        self.alg_gen = AG.AG()
        self.draw_rede = draw_rede.DrawRede(850, 20)
        self.best_agente = None
        self.quant_agentes = 200
        self.qt_loop_epoca = 6_000
        self.qt_iter = 0
        self.surface = surface
        self.parede = Parede(surface, 'tst.svg',  (255, 255, 255))
        self.checkpoints = Parede(surface, 'checkpoints.svg', (0, 155, 0))
        self.desist = Parede(surface, 'dest.svg', (0, 0, 155))
        self.sensor = Sensor(surface)
        self.agentes = []
        self.agentes_removidos = []
        #ag = self.load_net()
        #self.agentes.append(ag)
        ags = self.alg_gen.get_pesos_str()
        for i in range(0, self.quant_agentes):
            self.agentes.append(Agente(surface, self.parede))
    def loop(self):
        my_font = pygame.font.SysFont('monospace', 20)
        self.surface.blit(my_font.render('(' + str(self.qt_iter) + '/' + str(self.qt_loop_epoca) + ')', False, (255, 255, 255)), (930,430))
        self.surface.blit(my_font.render('Epóca: ' + str(self.qt_epoca) , False, (255, 255, 255)), (850,400))
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
        self.desist.loop()
        self.sensor.loop()
        for ag in self.agentes:
            ag.loop()
        for rect in self.checkpoints.rects:
            for ag in self.agentes:
                collision = rect.colliderect((ag.pos_rect[0] -5, ag.pos_rect[1] - 5, ag.pos_rect[2], ag.pos_rect[3]))
                if collision and not ag.is_collide:
                    ag.score += 1
                    ag.is_collide = True
                if not collision and not ag.is_collide:
                    ag.is_collide = False
        agentes_remover = []
        for rect in self.desist.rects:
            for ag in self.agentes:
                collision = rect.colliderect((ag.pos_rect[0] -5, ag.pos_rect[1] - 5, ag.pos_rect[2], ag.pos_rect[3]))
                if collision:
                    agentes_remover.append(ag)

        for ag in agentes_remover:
            self.agentes_removidos.append(ag)
            self.agentes.remove(ag)
        for ag in self.agentes:
            if ag.score == 0:
                    agentes_remover.append(ag)
        self.qt_iter += 1
        if self.qt_iter >= self.qt_loop_epoca:
            self.qt_epoca += 1
            self.qt_iter = 0
            sys.stdout.write("\n=======================Fim de epoca========================\n")
            ags = self.select_ag_cross()
            self.save_net(ags)
            for ag in agentes_remover:
                self.agentes.remove(ag)
            #Zera score para iniciar nova epoca
            for ag in self.agentes:
                ag.score = 0
            self.agentes.clear()
            self.alg_gen.crosover()
            #adiciona agentes melhores e o crusamento
            for a in ags:
                self.agentes.append(a)
            #self.agentes.append(ags[0])
            for i in range( 0, 197):
                peso_mut = self.alg_gen.get_pesos_str()
                sort = randint(0, 100)
                if sort < 60:
                    ag_mut = self.alg_gen.mutation(peso_mut[2], 0.3)
                if sort >= 60 and sort < 90:
                    ag_mut = self.alg_gen.mutation(peso_mut[0], 0.3)
                if sort > 90:
                    ag_mut = self.alg_gen.mutation(peso_mut[1], 0.3)
                ag = self.alg_gen.load_pesos(self.surface, self.parede, ag_mut)
                self.agentes.append(ag)
        age_max_score = self.agentes[0]
        for ag in self.agentes:
            if ag.score > age_max_score.score:
                age_max_score = ag
        draw.line(self.surface, (255, 0, 0),(age_max_score.x, age_max_score.y), (850, 20))
        self.draw_rede.draw(self.surface, age_max_score)
        self.surface.blit(my_font.render('Score: ' + str(age_max_score.score), False, (255, 255, 255)), (850,460))

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
    
    def select_ag_cross(self)-> tuple:
        ag_a = Agente(self.surface, self.parede)
        ag_b = Agente(self.surface, self.parede)
        agts = self.agentes_removidos + self.agentes
        for ag in agts:
            if ag.score > ag_a.score:
                ag_a = ag
            elif ag.score > ag_b.score:
                ag_b = ag
        self.agentes_removidos.clear()
        return (ag_a, ag_b)