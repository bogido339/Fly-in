class Dron:
    def __init__(self, id , path):
        self.id = id
        self.path = path
        self.objective = None
        self.position_index = 0
        self.current_zone = path[self.position_index]

    def run(self):
        pass

    def stop(self):
        pass
