class Tools:
    nom = ""

    def __init__(self, nom):
        self.nom = nom

class BoiteOutils:
    Tools liste_tools = []

    def __init__(self, tool):
        pass

    def add_tool(self, tool):
        self.liste_tools.append(tool)

    def remove_tool(self, tool):
        self.liste_tools.pop(tool)

class Tournevis:
    size = 0

    def __init__(self):
        super().__init__("Tournevis")

    def tighten(self, screw):
        pass
    def loosen(self, screw):
        pass

class Marteau:
    color = "white"

    def paint(self, color):
        self.color = color
    def hammer_in(self, nail):
        pass
    def remove(self, nail):
        pass