class Mapmanager:
    """Управління карткою"""

    def __init__(self):
        self.model = "block"  # модель кубика лежить у файлі block.egg
        # # використовуються такі текстури:
        self.texture = "block.png"
        self.colors = [
           (0.2, 0.2, 0.35, 1),
           (0.2, 0.5, 0.2, 1),
           (0.7, 0.2, 0.2, 1),
           (0.5, 0.3, 0.0, 1)
       ]


        # створюємо основний вузол картки:
        self.startNew()
        # створюємо будівельні блоки

    def startNew(self):
        """створює основу для нової картки"""
        self.land = render.attachNewNode(
            "Land"
        )  # вузол, до якого прив'язані всі блоки картки
    def getColor(self, z):
            if z < len(self.colors):
                return self.colors[z]
            else:
                return self.colors[len(self.colors) - 1]

    def addBlock(self, position):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)

        self.block.setTag("at", str(position))
        self.block.reparentTo(self.land)
    
    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True

    def loadLand(self, filename):
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(" ")
                for z in line:
                    for z0 in range(int(z) + 1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x, y
            

    def clear(self):
        self.land.removeNode()
        self.startNew()
