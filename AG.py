from random import randint
import obj
from obj import Agente

class AG:
    def __init__(self):
        pass
    def crosover(self):
        ag_base = obj.Agente(None, None)
        db_pesos = open('pesos.txt', 'r')
        ag_a = db_pesos.readline().split(' ')
        ag_b = db_pesos.readline().split(' ')
        qt_w = len(ag_a)
        ag_cross = []
        for i in range(0, int(len(ag_a)/2)):
            ag_cross.append(ag_a[i])
        for i in range(int(len(ag_b)/2), len(ag_b)):
            ag_cross.append(ag_b[i])
        db_pesos.close()
        self.save_pesos(ag_cross)

    def save_pesos(self, pesos_txt: str):
        db_pesos = open('pesos.txt', 'a')
        for str in pesos_txt:
            db_pesos.write(str + ' ')
        db_pesos.write('\n')
        db_pesos.close()

    def load_nets(self, surface, parede):
        ags = []
        arq = open('pesos.txt', 'r')
        for k in range(0, 3):
            ag = Agente(surface, parede)
            pesos = arq.readline().split(' ')
            self.mutation(pesos)
            i = 1
            for layer in ag.rede.rede:
                for perc in layer.perceptrons:
                    perc.bias = int(pesos[i])
                    i += 1
                    for j in range(0, len(perc.pesos)):
                        perc.pesos[j] = int(pesos[i])
                        i += 1
            ags.append(ag)
        arq.close()

    def mutation(self, pesos:str):
        pesos_txt = []
        for p in pesos:
            if randint(0, 100) < 30:
                if p == '\n':
                    break
                p_n = int(p)
                p_n += int(p_n * 0.3)
                pesos_txt.append(str(p_n))
        pass