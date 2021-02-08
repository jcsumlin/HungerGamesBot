import random

from .Event import Event


class Cycle:
    def __init__(self, tributes: list, daytime: bool, ignore_items=False, ignore_alliances=False):
        self.tributes = tributes
        self.number_of_tributes = len(tributes)
        self.unassigned_tributes = self.number_of_tributes
        if daytime:
            self.time = "Day"
        else:
            self.time = "Night"
        self.ignore_items = ignore_items
        self.ignore_alliances = ignore_alliances

        self.events = self.__get_events__()
        self.dead = []
        self.survive = []

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
                n = random.choices(outcomes, probability)[0]
                list_of_events.append(n)
                self.unassigned_tributes -= n
            elif self.unassigned_tributes == 4:
                n = random.choices(outcomes[1:], probability[1:])[0]
                list_of_events.append(n)
                self.unassigned_tributes -= n
            elif self.unassigned_tributes == 3:
                n = random.choices(outcomes[2:], probability[2:])[0]
                list_of_events.append(n)
                self.unassigned_tributes -= n
            elif self.unassigned_tributes == 2:
                n = random.choices(outcomes[3:], probability[3:])[0]
                list_of_events.append(n)
                self.unassigned_tributes -= n
            elif self.unassigned_tributes == 1:
                list_of_events.append(1)
                self.unassigned_tributes -= 1

        return list_of_events

    def resolve_events(self):
        """Resolves the days events by marking tributes as dead or survived"""
        for event in self.events:
            event.resolve()
            for death in event.dead:
                self.dead.append(death)
            for survivor in event.survived:
                self.survive.append(survivor)

    def __select_tributes__(self, list_of_events: list):
        """Sorts tributes into a list of groups of tributes involved in each event"""
        sorted_tributes = []
        for event in list_of_events:
            tributes_included = []
            for i in range(event):
                tribute = random.choice(self.tributes)
                self.tributes.pop(self.tributes.index(tribute))
                tributes_included.append(tribute)
            sorted_tributes.append(tributes_included)
        return sorted_tributes

    def __get_events__(self):
        """Returns the days events as a list of event objects"""
        events = []
        list_of_events = self.find_number_of_tributes_in_events()
        tribute_groups = self.__select_tributes__(list_of_events)
        for tribute_group in tribute_groups:
            if self.time == "Day":
                event = self.__get_daytime_event__(tribute_group)
            else:
                event = self.__get_nighttime_event__(tribute_group)
            events.append(event)
        return events

    def __get_daytime_event__(self, tributes):
        """Returns a random daytime event that matches the constraints"""
        n = len(tributes)
        events_for_n_tributes = []  # Placeholder until code is written

        events = []
        for event in events_for_n_tributes:  # Create an Event object for each event instance
            i = Event(tributes, event)
            events.append(i)

        for event in events:  # Filter by time of day == day
            if event.time == "night":
                events.pop(events.index(event))
        for event in events:  # Filter by subject tribute meeting prerequisites
            if not event.subject_meets_prerequisites(ignore_items=self.ignore_items,
                                                     ignore_alliances=self.ignore_alliances):
                events.pop(events.index(event))

        return random.choice(events)  # Return a random event from the remaining candidates

    def __get_nighttime_event__(self, tributes):
        """Returns a random nighttime event that matches the constraints"""
        n = len(tributes)
        events_for_n_tributes = []  # Placeholder until code is written

        events = []
        for event in events_for_n_tributes:  # Create an Event object for each event instance
            i = Event(tributes, event)
            events.append(i)

        for event in events:  # Filter by time of day == night
            if event.time == "day":
                events.pop(events.index(event))
        for event in events:  # Filter by subject tribute meeting prerequisites
            if not event.subject_meets_prerequisites(ignore_items=self.ignore_items,
                                                     ignore_alliances=self.ignore_alliances):
                events.pop(events.index(event))

        return random.choice(events)  # Return a random event from the remaining candidates
