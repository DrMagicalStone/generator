from shapely import Point
from TextInfo import TextInfo
from numpy import matrix, linalg, argmin

def getTextTuCut(texts: list[TextInfo]):
    copy = texts.copy()
    copy.sort(key= lambda text: text.border[0].x + text.border[0].y * 10000)
    return copy[0]

def cuttingLoss(y_true, y_pred):
    castData(y_pred, y_true)

def castData(coordinateValues: tuple[float, float, float, float, float, float, float, float], text: TextInfo):
    cuttedText = []
    cuttedTextCenterVector = matrix([[0, 0]]).T
    for i in range(0, 4):
        vertex = matrix([[coordinateValues[2 * i], coordinateValues[2 * i + 1]]]).T
        cuttedTextCenterVector = cuttedTextCenterVector + vertex
        cuttedText.append(vertex)
    cuttedTextCenterVector = cuttedTextCenterVector / 4
    
    return calcuteDiff(cuttedText, text)
    
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

print(castData((0, 0, 0, 0, 0, 0, 0, 0), testTexts))