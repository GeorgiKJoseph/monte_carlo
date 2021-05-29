import random

class Rounds:
    def __init__(self, prob=0.5):
        self.prob = prob
        self.precision = len(str(self.prob))-2

    def go(self):
        rounds = 0
        prev = 0
        while(True):
            pick = round(
                random.uniform(0, 1),
                self.precision
            )
            if pick != self.prob:
                rounds += 1
                if prev >= self.prob and pick >= self.prob:
                    break
                prev = pick
        return rounds

    def avgRounds(self, rounds, total):
        return sum(rounds)/total

def run(iterations):
    results = []
    rounds = Rounds(0.8)
    for i in range(iterations):
        results.append(rounds.go())
    print('Estimated rounds: ', rounds.avgRounds(results, iterations))
