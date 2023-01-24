
class Cluster:

    def __init__(self, constituants, sequence, distance) -> None:

        self.constituants = constituants
        self.sequence = sequence
        self.distance = distance

    def __repr__(self) -> str:
        return f'{self.sequence}'
