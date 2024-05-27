from shapely import Point
from TextInfo import TextInfo
from numpy import matrix, linalg, argmin

def cuttingLoss(y_true, y_pred):
    pass

def findNearestText(coordinateValues: tuple[float, float, float, float, float, float, float, float], texts: list[TextInfo]):
    cuttedText = []
    cuttedTextCenterVector = matrix([[0, 0]]).T
    for i in range(0, 4):
        vertex = matrix([[coordinateValues[2 * i], coordinateValues[2 * i + 1]]]).T
        cuttedTextCenterVector = cuttedTextCenterVector + vertex
        cuttedText.append(vertex)
    cuttedTextCenterVector = cuttedTextCenterVector / 4
    
    centerVectors: list[matrix] = []
    for text in texts:
        center: Point = text.borderPolygon().centroid
        centerVectors.append(matrix(center.x, center.y).T)
    diffs: list[float] = []
    for i in range(0, len(texts)):
        diffs.append(linalg.norm(cuttedTextCenterVector -  centerVectors[i]))
    indexOfNearest = argmin(diffs)
    return calcuteDiff(cuttedText, texts[indexOfNearest])
    
def calcuteDiff(cuttedText: list[matrix], nearestText: TextInfo):
    vertexs: list[matrix] = []
    error = 0
    for vertex in nearestText.border:
        vertexs.append(matrix([[vertex.x, vertex.y]]).T)
    for point in cuttedText:
        diffs = []
        for vertex in vertexs:
            diffs.append(linalg.norm(point - vertex))
        index = argmin(diffs)
        error = max(error, diffs[index])
        del vertexs[index]
    return error
        
        
testTexts = [TextInfo("xxxx", (Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))), TextInfo("xxxx", (Point(0, 0), Point(0, 1), Point(0, 0), Point(1, 0)))]

print(findNearestText((0, 0, 0, 0, 0, 0, 0, 0), testTexts))