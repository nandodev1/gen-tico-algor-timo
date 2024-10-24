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
        return ags
    
    def get_pesos_str(self):
        pesos = []
        pesos_txt = open('pesos.txt', 'r')
        for i in range(0, 3):
            p = pesos_txt.readline().split(' ')
            pesos.append(p)
        return pesos

    def load_pesos(self, surface, parede, pesos_str):
        ags = []
        ag = Agente(surface, parede)
        i = 1
        for layer in ag.rede.rede:
            for perc in layer.perceptrons:
                perc.bias = int(pesos_str[i])
                i += 1
                for j in range(0, len(perc.pesos)):
                    perc.pesos[j] = int(pesos_str[i])
                    i += 1
            ags.append(ag)
        return ag

    def mutation(self, pesos:str, hate_taxe: float):
        pesos_txt = []
        pesos_txt.append(pesos[0])
        for i in range(1, len(pesos)-1):
            if randint(0, 100) < 90:
                if pesos[i] == '\n':
                    break
                p_n = int(pesos[i])
                if randint(0, 2) == 1:
                    p_n += int(p_n * hate_taxe)
                else:
                    p_n -= int(p_n * hate_taxe)
                pesos_txt.append(str(p_n))
            else:
                pesos_txt.append(pesos[i])
        pesos_txt.append(pesos[-1])
        return pesos_txt