from random import randint


#---------------------------------------------------------
#IAS
#---------------------------------------------------------

class Perc:

    def __init__(self, qt_inp: int) -> None:
        self.bias = randint(-1000, 1000)
        self.pesos = []
        for i in range(0, qt_inp):
            peso = 0
            while peso == 0:
                peso = randint(-1000, 1000)
            self.pesos.append(peso)

    def out(self, entradas: list) -> int:
        soma = 0
        for p in range(0, len(self.pesos)):
            soma += self.pesos[p] * entradas[p] + self.bias
        if soma > 0:
            return soma
        return 0


class Layer:
    def __init__(self, qt_perc: int, qt_inp: int):
        self.perceptrons = []
        for i in range(0, qt_perc):
            self.perceptrons.append(Perc(qt_inp))


class Rede:
    def __init__(self) -> None:

        self.rede = []

        self.add_layer(4, 2)
        self.add_layer(5, 4)
        self.add_layer(4, 5)

        self.last_process = []

    def add_layer(self, qt_perc: int, qt_inp: int):
        self.rede.append(Layer(qt_perc, qt_inp))

    def out(self, entrada):
        inputs = []
        for inp in entrada:
            inputs.append(int(inp))
        outputs_rede = [inputs]

        for layer in self.rede:
            tmp_out_perc = []
            for per in layer.perceptrons:
                tmp_out_perc.append(int(per.out(outputs_rede[-1])))
            outputs_rede.append(tmp_out_perc)

        self.last_process.clear()

        last_tmp = []

        self.last_process = outputs_rede

        for c in self.last_process:
            tmp_tuple = []
            for out in c:
                if out > 0:
                    tmp_tuple.append(1)
                else:
                    tmp_tuple.append(0)
            last_tmp.append(tmp_tuple)

        self.last_process = last_tmp

        return outputs_rede[-1]
