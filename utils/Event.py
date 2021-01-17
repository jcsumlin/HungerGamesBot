import discord


class Event:
    def __init__(self, tributes, id: int, name: str, number_of_tributes: int, time: int, prerequisites):
        self.tributes = tributes
        self.id = id
        self.name = name
        self.number_of_tributes = number_of_tributes
        self.time = time
        self.prerequisites = prerequisites

    def generate_embed(self):
        """Returns the event as an embed"""
        pass
