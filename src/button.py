from sprites import Sprite

class Button:
    def __init__(self, label: str, pos: tuple[float, float], size: tuple[float, float], sprite: Sprite,
                 kind: str, value: int = 0, scaleText: bool = True) -> None:
        self.pos = pos
        self.size = size
        
        self.sprite = sprite
        self.label = label
        self.kind = kind
        self.value = value
        self.scaleText = scaleText

    def inside(self, pos: tuple[float, float]) -> bool:
        """
        Whether `pos` is inside the button
        """
        x, y = pos
        minX, minY = self.pos
        deltaX, deltaY = self.size
        maxX, maxY = minX + deltaX, minY + deltaY
        return minX <= x <= maxX and minY <= y <= maxY
    
    def draw(self, screen) -> None:
        self.sprite.draw(screen, self.pos, size=self.size, text=self.label, scaleText=self.scaleText)