import random

class Loteria:
    def __init__(self, nome):
        pass

    def gerar_aposta(self, quant=5):
        if not (5 <= quant <= 80):
            return ()
        result = random.sample(xrange(1, 81), quant)
        return tuple(sorted(result))
