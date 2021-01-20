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

        # Read the json and populate the object
        self.json = json.loads(json_blob)
        self.id = self.json["id"]
        self.name = self.json["name"]
        self.string = self.json["string"]
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
                    if self.__no_alliance():
                        matches += 1

        if matches == len(self.prerequisites):
            return True
        else:
            return False

    def cull_tributes(self):
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

        return dead, survive

    def __has_weapon__(self):
        """Returns True if subject tribute has a weapon, False if not"""
        return self.subject_tribute.has_weapon

    def __no_alliance(self):
        """Returns True if subject tribute has no alliances with included tributes, False if they do"""
        for tribute in self.tributes:
            if tribute.id in self.subject_tribute.alliances:
                return False
        return True
