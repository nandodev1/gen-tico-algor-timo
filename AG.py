class AG:
    def __init__(self):
        pass
    def crosover(self):
        db_pesos = open('pesos.txt', 'r')
        ag_a = db_pesos.readline()
        ag_b = db_pesos.readline()