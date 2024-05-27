from shapely import Point, LineString, Polygon

from re import sub

class TextInfo:
    
    def __init__(self, text: str, border: tuple[Point, Point, Point, Point]) -> None:
        self.text = text
        self.border = border
        
    def borderPolygon(self) -> Polygon:
        return Polygon((self.border[0], self.border[1], self.border[2], self.border[3]))
        
    def intersects(self, another) -> bool:
        border: Polygon = self.borderPolygon()
        anotherBorder: Polygon = another.borderPolygon()
        return border.intersects(anotherBorder)
                
    def __repr__(self) -> str:
        return self.text.replace("\n", "\\n") + ": " + str(self.border)