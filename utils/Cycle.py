import random


class Cycle:
    def __init__(self, tributes: list):
        self.tributes = tributes
        self.number_of_tributes = len(tributes)
        self.unassigned_tributes = self.number_of_tributes

        """The weights dictionary defines the probability of any given event
        including x number of tributes"""
        self.weights = {5: 0.1, 4: 0.1, 3: 0.2, 2: 0.4, 1: 0.2}

    def find_number_of_tributes_in_events(self):
        """Determines the number of tributes in any given event
        via use of weighted average and returns results as a
        list of integers"""
        outcomes = list(self.weights.keys())
        probability = list(self.weights.values())

        list_of_events = []

        while self.unassigned_tributes > 0:
            if self.unassigned_tributes >= 5:
                n = random.choices(outcomes, probability)
                list_of_events.append(n)
                self.unassigned_tributes -= n
            elif self.unassigned_tributes == 4:
                n = random.choices(outcomes[1:], probability[1:])
                list_of_events.append(n)
                self.unassigned_tributes -= n
            elif self.unassigned_tributes == 3:
                n = random.choices(outcomes[2:], probability[2:])
                list_of_events.append(n)
                self.unassigned_tributes -= n
            elif self.unassigned_tributes == 2:
                n = random.choices(outcomes[3:], probability[3:])
                list_of_events.append(n)
                self.unassigned_tributes -= n
            elif self.unassigned_tributes == 1:
                list_of_events.append(1)
                self.unassigned_tributes -= 1

        return list_of_events

    def select_tributes(self, list_of_events: list):
        sorted_tributes = []
        for event in list_of_events:
            tributes_included = []
            for i in range(event):
                tribute = random.choice(self.tributes)
                self.tributes.pop(self.tributes.index(tribute))
                tributes_included.append(tribute)
            tributes_included.append(sorted_tributes)
