class Point:
    def __init__(self, x: int, y: int):
        self.x = x 
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
        
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
        
    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y
