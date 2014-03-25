import random

class Loteria:
    def __init__(self, nome):
        pass

    def gerar_aposta(self, quant=5):
        if not (5 <= quant <= 80):
            return ()
        result = set()
        while len(result) < quant:
            result.add(random.randint(1, 80))
        return tuple(result)
