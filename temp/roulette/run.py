import random

TOTAL_SLOTS = 36

class Roulette:
    def __init__(self):
        self.slots = [x for x in range(1,TOTAL_SLOTS+1)]
        self.ball = None
    def spin(self):
        self.ball = random.choice(self.slots)
    def earning(self, bet):
        if self.ball == bet:
            return TOTAL_SLOTS-1
        return -1

spins = 1000000
wallet = 0
game = Roulette()
for i in range(spins):
    game.spin()
    wallet += game.earning(1)
print('Wallet: ', wallet)
print('expected amount per spin: ', 100*wallet/spins, '%')
