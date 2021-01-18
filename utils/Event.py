import json
import random


class Event:
    def __init__(self, tributes, json_blob: str):
        self.tributes = tributes  # Tributes is a list of Tribute objects
        """The 'subject' tribute is the 'main character' of this event.
        The prerequisites will be judged against the subject tribute"""
        self.subject_tribute = random.choice(self.tributes)
        self.tributes.pop(self.tributes.index(self.subject_tribute))
        self.n = len(self.tributes) + len(self.subject_tribute)

        # Read the json and populate the object
        self.json = json.loads(json_blob)
        self.id = self.json["id"]
        self.name = self.json["name"]
        self.number_of_tributes = self.json["number_of_tributes"]
        self.time = self.json["time"]
        self.prerequisites = self.json["prerequisites"]

    def subject_meets_prerequisites(self):
        """Returns True if the subject tribute has all of the prerequisites"""
        matches = 0
        for prerequisite in self.prerequisites:  # This loop needs an if case for every type of prerequisite
            if prerequisite == "hasWeapon":
                if self.__has_weapon__():
                    matches += 1

        if matches == len(self.prerequisites):
            return True
        else:
            return False

    def __has_weapon__(self):
        """Returns True if subject tribute has a weapon, False if not"""
        return self.subject_tribute.has_weapon
