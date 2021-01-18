class Tribute:
    def __init__(self, id: int, name: str, image: str):
        self.id = id
        self.name = name
        self.image = image

        self.weapons = []
        self.medicine = []
        self.alliances = []  # List of tribute IDs that this tribute has alliances with

        self.has_weapon = False  # This should be True if the Tribute has any weapons
        self.has_medicine = False  # This should be True if the Tribute has any weapons
        self.has_alliance = False  # This should be True if the Tribute has any alliances

    def add_weapon(self, weapon: str):
        if weapon not in self.weapons:  # Avoid dupes
            self.weapons.append(weapon)
            self.has_weapon = True

    def remove_weapon(self, weapon: str):
        if weapon in self.weapons:
            self.weapons.pop(self.weapons.index(weapon))
            if len(self.weapons) == 0:
                self.has_weapon = False

    def add_medicine(self, medicine: str):
        if medicine not in self.medicine:  # Avoid dupes
            self.medicine.append(medicine)
            self.has_medicine = True

    def remove_medicine(self, medicine: str):
        if medicine in self.medicine:
            self.medicine.pop(self.medicine.index(medicine))
            if len(self.medicine) == 0:
                self.has_medicine = False

    def add_alliance(self, alliance: int):
        if alliance not in self.alliances:  # Avoid dupes
            self.alliances.append(alliance)
            self.has_alliance = True

    def remove_alliance(self, alliance: int):
        if alliance in self.alliances:
            self.alliances.pop(self.alliances.index(alliance))
            if len(self.alliances) == 0:
                self.has_alliance = False
