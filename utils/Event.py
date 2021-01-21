import json
import random


class Event:
    def __init__(self, tributes, json_blob: str):
        self.tributes = tributes  # Tributes is a list of Tribute objects
        """The 'subject' tribute is the 'main character' of this event.
        The prerequisites will be judged against the subject tribute"""
        self.subject_tribute = random.choice(self.tributes)
        self.tributes.pop(self.tributes.index(self.subject_tribute))
        self.n = len(self.tributes) + 1
        self.completed = False  # Set this to True once the event has been resolved

        # Read the json and populate the object
        self.json = json.loads(json_blob)
        self.id = self.json["id"]
        self.name = self.json["name"]
        self.string = self.json["string"]
        self.event_type = self.json["type"]
        self.number_of_tributes = self.json["number_of_tributes"]
        self.time = self.json["time"]
        self.prerequisites = self.json["prerequisites"]
        self.dies = self.json["dies"]
        self.survives = self.json["survives"]

    def subject_meets_prerequisites(self, ignore_items=False, ignore_alliances=False):
        """Returns True if the subject tribute has all of the prerequisites"""
        matches = 0

        for prerequisite in self.prerequisites:  # This loop needs an if case for every type of prerequisite
            if not ignore_items:  # If statements for prerequisites that need items go under here
                if prerequisite == "hasWeapon":
                    if self.__has_weapon__():
                        matches += 1
            if not ignore_alliances:  # If statements for prerequisites that need alliances go here
                if prerequisite == "noAlliance":
                    if self.__no_alliance__():
                        matches += 1

        if matches == len(self.prerequisites):
            return True
        else:
            return False

    def resolve(self):
        """Resolves the event by calling the appropriate function"""
        if self.event_type == "murder":
            return self.__cull_tributes__()
        elif self.event_type == "alliance":
            pass
        elif self.event_type == "injury":
            result = self.__injure_tributes__()
            for tribute in result[0]:
                tribute.add_injury("injury")
            survivors = [self.subject_tribute]
            for tribute in self.tributes:
                survivors.append(tribute)
            return [], survivors  # Return an empty list in place of dead tributes

    def __cull_tributes__(self):
        """Randomly selects tributes involved in the event to either die or survive"""
        n_dead = self.dies["number"]

        dead = []
        survive = []

        if self.dies["subject"]:  # Remove the subject from the dies/survives group
            n_dead -= 1
            dead.append(self.subject_tribute)
        else:
            survive.append(self.subject_tribute)

        for i in range(n_dead):  # Pick random tributes until the number of dead is high enough
            tribute = random.choice(self.tributes)
            dead.append(tribute)
            self.tributes.pop(self.tributes.index(tribute))
        for tribute in self.tributes:  # Add the rest of the tributes to the survivors
            survive.append(tribute)

        self.completed = True
        return dead, survive

    def __injure_tributes__(self):
        """Randomly selects tributes involved in the event to be injured"""
        n_injured = self.dies["number"]

        injured = []
        not_injured = []

        if self.dies["subject"]:  # Remove the subject from the injured group
            n_injured -= 1
            injured.append(self.subject_tribute)

        if len(self.tributes) > 0:
            for i in range(n_injured):  # Pick random tributes until the number injured is high enough
                tribute = random.choice(self.tributes)
                injured.append(tribute)
            for tribute in self.tributes:  # Add any remaining to the not injured group
                not_injured.append(tribute)

        self.completed = True
        return injured, not_injured

    def __has_weapon__(self):
        """Returns True if subject tribute has a weapon, False if not"""
        return self.subject_tribute.has_weapon

    def __no_alliance__(self):
        """Returns True if subject tribute has no alliances with included tributes, False if they do"""
        for tribute in self.tributes:
            if tribute.id in self.subject_tribute.alliances:
                return False
        return True
