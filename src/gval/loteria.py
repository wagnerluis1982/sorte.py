import random

class Loteria:
    def __init__(self, nome):
        pass

    def gerar_aposta(self):
        result = set()
        while len(result) < 5:
            result.add(random.randint(1, 80))
        return tuple(result)
