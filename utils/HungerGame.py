from utils.database import Database


class HungerGame(Database):
    def __init__(self):
        super().__init__()

    def create(self):
        self.connection.execute("")

    def get(self):
        pass

    def update(self):
        pass
