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
        if "partialAlliance" in self.prerequisites:
            self.has_partial_alliance = True
            self.n_partial = self.json["partial_alliance_number"]
            self.tributes_allied = []
        else:
            self.has_partial_alliance = False
        self.dies = self.json["dies"]
        self.survives = self.json["survives"]

        self.dead = []
        self.survived = []

    def subject_meets_prerequisites(self, ignore_items=False, ignore_alliances=False):
        """Returns True if the subject tribute has all of the prerequisites"""
        matches = 0

        for prerequisite in self.prerequisites:  # This loop needs an if case for every type of prerequisite
            if prerequisite == "hasWeapon":
                if not ignore_items:
                    if self.__has_weapon__():
                        matches += 1
                else:
                    matches += 1

            if prerequisite == "noAlliance":
                if not ignore_alliances:
                    if self.__no_alliance__():
                        matches += 1
                else:
                    matches += 1

            if prerequisite == "hasAlliance":
                if not ignore_alliances:
                    if self.__has_alliance__():
                        matches += 1
                else:
                    matches += 1

            if prerequisite == "hasMedicine":
                if not ignore_items:
                    if self.__has_medicine__():
                        matches += 1
                else:
                    matches += 1

        if matches == len(self.prerequisites):
            return True
        else:
            return False

    def resolve(self):
        """Resolves the event by calling the appropriate function"""
        if self.event_type == "murder":
            self.__cull_tributes__()

        elif self.event_type == "alliance_formed":
            self.__alliance_formed__()
            self.survived.append(self.subject_tribute)
            for tribute in self.tributes:
                self.survived.append(tribute)

        elif self.event_type == "alliance_broken":
            self.__alliance_broken__()

        elif self.event_type == "injury":
            result = self.__injure_tributes__()
            for tribute in result[0]:
                tribute.add_injury("injury")
            self.survived.append(self.subject_tribute)
            for tribute in self.tributes:
                self.survived.append(tribute)

        elif self.event_type == "remove_injury":
            n_injuries = len(self.subject_tribute.injuries)
            index = random.randint(0, n_injuries - 1)
            injury_to_remove = self.subject_tribute.injuries[index]
            self.subject_tribute.remove_injury(injury_to_remove)
            self.survived.append(self.subject_tribute)
            for tribute in self.tributes:
                self.survived.append(tribute)

        elif self.event_type == "get_weapon":
            weapon = self.json["weapon"]
            self.subject_tribute.add_weapon(weapon)
            self.survived.append(self.subject_tribute)
            for tribute in self.tributes:
                self.survived.append(tribute)

        elif self.event_type == "get_medicine":
            medicine = self.json["medicine"]
            self.subject_tribute.add_medicine(medicine)
            self.survived.append(self.subject_tribute)
            for tribute in self.tributes:
                self.survived.append(tribute)

        elif self.event_type == "neutral":  # Default type for an event where no-one dies or is injured.
            self.survived.append(self.subject_tribute)
            for tribute in self.tributes:
                self.survived.append(tribute)

        self.completed = True

    def get_formatted_string(self):
        if not self.completed:
            raise Exception("Please resolve the event before generating a formatted string.")

        if self.dies["number"] == 0:
            return self.__get_formatted_not_fatal__()
        elif self.dies["number"] > 0:
            return self.__get_formatted_fatal__()

    def __get_formatted_not_fatal__(self):
        if self.n == 1:
            string = self.string.format(subject=self.subject_tribute.name)
            return string
        elif self.n == 2:
            string = self.string.format(self.survived[0].name,
                                        subject=self.subject_tribute.name)
            return string
        elif self.n == 3:
            string = self.string.format(self.survived[0].name,
                                        self.survived[1].name,
                                        subject=self.subject_tribute.name)
            return string
        elif self.n == 4:
            string = self.string.format(self.survived[0].name,
                                        self.survived[1].name,
                                        self.survived[2].name,
                                        subject=self.subject_tribute.name)
            return string
        elif self.n == 5:
            string = self.string.format(self.survived[0].name,
                                        self.survived[1].name,
                                        self.survived[2].name,
                                        self.survived[3].name,
                                        subject=self.subject_tribute.name)
            return string

    def __get_formatted_fatal__(self):
        if self.n == 1:
            string = self.string.format(subject=self.subject_tribute.name)
            return string
        elif self.n == 2:
            string = self.string.format(subject=self.subject_tribute.name,
                                        first_dead=self.dead[0].name)
            return string
        elif self.n == 3:
            # Determine which outcome occurred (either 1, 2, or 3 died)
            if self.dies["number"] == 1:
                string = self.string.format(self.survived[0].name,
                                            subject=self.subject_tribute.name,
                                            first_dead=self.dead[0].name)
                return string
            elif self.dies["number"] >= 2:
                string = self.string.format(subject=self.subject_tribute.name,
                                            first_dead=self.dead[0].name,
                                            second_dead=self.dead[1].name)
                return string
        elif self.n == 4:
            # Determine which outcome occurred (either 1, 2 3 or 4 died)
            if self.dies["number"] == 1:
                string = self.string.format(self.survived[0].name,
                                            self.survived[1].name,
                                            subject=self.subject_tribute.name,
                                            first_dead=self.dead[0].name)
                return string
            elif self.dies["number"] == 2:
                string = self.string.format(self.survived[0].name,
                                            subject=self.subject_tribute.name,
                                            first_dead=self.dead[0].name,
                                            second_dead=self.dead[1].name)
                return string
            elif self.dies["number"] >= 3:
                string = self.string.format(subject=self.subject_tribute.name,
                                            first_dead=self.dead[0].name,
                                            second_dead=self.dead[1].name,
                                            third_dead=self.dead[2].name)
                return string
        elif self.n == 5:
            # Determine which outcome occurred (either 1, 2, 3, 4 or 5 died)
            if self.dies["number"] == 1:
                if self.dies["number"] == 1:
                    string = self.string.format(self.survived[0].name,
                                                self.survived[1].name,
                                                self.survived[2].name,
                                                subject=self.subject_tribute.name,
                                                first_dead=self.dead[0].name)
                    return string
                elif self.dies["number"] == 2:
                    string = self.string.format(self.survived[0].name,
                                                self.survived[1].name,
                                                subject=self.subject_tribute.name,
                                                first_dead=self.dead[0].name,
                                                second_dead=self.dead[1].name)
                    return string
                elif self.dies["number"] == 3:
                    string = self.string.format(self.survived[0].name,
                                                subject=self.subject_tribute.name,
                                                first_dead=self.dead[0].name,
                                                second_dead=self.dead[1].name,
                                                third_dead=self.dead[2].name)
                    return string
                elif self.dies["number"] >= 4:
                    string = self.string.format(subject=self.subject_tribute.name,
                                                first_dead=self.dead[0].name,
                                                second_dead=self.dead[1].name,
                                                third_dead=self.dead[2].name,
                                                fourth_dead=self.dead[3].name)
                    return string

    def __cull_tributes__(self):
        """Randomly selects tributes involved in the event to either die or survive"""
        n_dead = self.dies["number"]

        if self.dies["subject"]:  # Remove the subject from the dies/survives group
            n_dead -= 1
            self.dead.append(self.subject_tribute)
        else:
            self.survived.append(self.subject_tribute)

        if self.has_partial_alliance:
            # Remove allied tributes from the pool and add them to survived
            for allied_tribute in self.tributes_allied:
                self.tributes.pop(self.tributes.index(allied_tribute))
                self.survived.append(allied_tribute)

        for i in range(n_dead):  # Pick random tributes until the number of dead is high enough
            tribute = random.choice(self.tributes)
            self.dead.append(tribute)
            self.tributes.pop(self.tributes.index(tribute))
        for tribute in self.tributes:  # Add the rest of the tributes to the survivors
            self.survived.append(tribute)

    def __injure_tributes__(self):
        """Randomly selects tributes involved in the event to be injured"""
        n_injured = self.dies["number"]

        injured = []
        not_injured = []

        if self.dies["subject"]:  # Remove the subject from the injured group
            n_injured -= 1
            injured.append(self.subject_tribute)

        if self.has_partial_alliance:
            # Remove the allied tributes from the pool and add them to not_injured
            for allied_tribute in self.tributes_allied:
                self.tributes.pop(self.tributes.index(allied_tribute))
                not_injured.append(allied_tribute)

        if len(self.tributes) > 0:
            for i in range(n_injured):  # Pick random tributes until the number injured is high enough
                tribute = random.choice(self.tributes)
                injured.append(tribute)
            for tribute in self.tributes:  # Add any remaining to the not injured group
                not_injured.append(tribute)

        self.completed = True
        return injured, not_injured

    def __alliance_formed__(self):
        """Forms an alliance between the tributes"""
        tributes_involved = [self.subject_tribute]
        for tribute in self.tributes:  # Add all tributes to the tributes_involved
            tributes_involved.append(tribute)

        for tribute in tributes_involved:  # Add an alliance for every tribute except themselves
            for tribute_to_add in tributes_involved:
                if tribute_to_add.id != tribute.id:
                    tribute.add_alliance(tribute_to_add.id)

    def __alliance_broken__(self):
        """Breaks an alliance between the tributes"""
        tributes_involved = [self.subject_tribute]
        for tribute in self.tributes:  # Add all tributes to the tributes_involved
            tributes_involved.append(tribute)

        for tribute in tributes_involved:  # Remove the alliance for every tribute except themselves
            for tribute_to_remove in tributes_involved:
                if tribute_to_remove.id != tribute.id:
                    tribute.remove_alliance(tribute_to_remove.id)

        if self.dies["number"] > 0:  # If event specifies tributes die, kill tributes
            self.__cull_tributes__()

    def __has_weapon__(self):
        """Returns True if subject tribute has a weapon, False if not"""
        if "weapon" in self.json:  # Check if a weapon is specified
            if self.json["weapon"] in self.subject_tribute.weapons:
                return True
            else:
                return False
        return self.subject_tribute.has_weapon

    def __has_medicine__(self):
        """Returns True if subject tribute has medicine, False if not"""
        if "medicine" in self.json:  # Check if a medicine is specified
            if self.json["medicine"] in self.subject_tribute.medicine:
                return True
            else:
                return False

    def __no_alliance__(self):
        """Returns True if subject tribute has no alliances with included tributes, False if they don't"""
        for tribute in self.tributes:
            if tribute.id in self.subject_tribute.alliances:
                return False
        return True

    def __has_alliance__(self):
        """Returns True if subject tribute has an alliance with all included tributes, False if they don't"""
        alliances = 0
        for tribute in self.tributes:
            if tribute.id in self.subject_tribute.alliances:
                alliances += 1

        if alliances == len(self.tributes):
            return True
        else:
            return False

    def __partial_alliance__(self):
        """Returns true if subject tribute has an alliance with the specified number of tributes, False if they don't"""
        alliances = 0
        for tribute in self.tributes:
            if tribute.id in self.subject_tribute.alliances:
                self.tributes_allied.append(tribute)  # Create a list of allied tributes so they don't get killed
                alliances += 1

        if alliances == self.n_partial:
            return True
        else:
            return False
