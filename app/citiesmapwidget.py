#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QTransform, QPainterPath
from PyQt5.QtCore import Qt, QPoint

class CitiesMapWidget(QWidget):
    def __init__(self, citiesMap, carsPaths, parent):
        super(CitiesMapWidget, self).__init__(parent)
        self.citiesMap = citiesMap
        self.carsPaths = carsPaths
        self.currentPath = []

        # shift everything by (10, 10)
        beginPoint = [20, 20]

        self.initPoints(citiesMap)
        self.initTransform(citiesMap, beginPoint)
        self.initPens()

    def initPoints(self, citiesMap):
        [backeryX, backeryY] = citiesMap[0]
        self.backeryPoint = QPoint(backeryX, backeryY)

        self.citiesPoint = []
        for [cityX, cityY] in citiesMap[1:]:
            cityPoint = QPoint(cityX, cityY)
            self.citiesPoint.append(cityPoint)

    def initTransform(self, citiesMap, beginPoint):
        [minX, minY] = citiesMap[0]
        for [x, y] in citiesMap[1:]:
            [minX, minY] = [min(x, minX), min(y, minY)]

        [offsetX, offsetY] = [0, 0]
        if minX < 0:
            minX = -minX
            offsetX = 2 * minX
        if minY < 0:
            minY = -minY
            offsetY = 2 * minY

        [beginX, beginY] = beginPoint
        assert beginX >= 0 and beginY >= 0, "Begin point must be in first quarter"
        if minX < beginX:
            offsetX += (beginX - minX)
        if minY < beginY:
            offsetY += (beginY - minY)

        [scaleX, scaleY] = [1, 1]

        self.transform = QTransform()
        self.transform.scale(scaleX, scaleY)
        self.transform.translate(offsetX, offsetY)

    def initPens(self):
        cap = Qt.RoundCap
        style = Qt.SolidLine
        otherPathsStyle = Qt.DashLine
        pointsWidth = 5
        pathsWidth = 1
        currentPathWidth = 2
        citiesColor = QColor(255, 0, 0)
        backeryColor = QColor(0, 255, 0)
        otherPathsColor = QColor(196, 196, 196)
        currentPathColor = QColor(0, 0, 0)
        self.backeryPen = QPen(backeryColor, pointsWidth, style, cap)
        self.citiesPen = QPen(citiesColor, pointsWidth, style, cap)
        self.otherPathsPen = QPen(otherPathsColor, pathsWidth, otherPathsStyle, cap)
        self.currentPathPen = QPen(currentPathColor, currentPathWidth, style, cap)
        
    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.setWorldTransform(self.transform)
            self.drawCitiesMap(painter)
            self.drawCurrentPath(painter)

    def drawCitiesMap(self, painter):
        self.drawCities(painter)
        self.drawBackery(painter)
        self.drawCarsPaths(painter)

    def drawCurrentPath(self, painter):
        if len(self.currentPath) == 0:
            return

        painter.setPen(self.currentPathPen)
        path = QPainterPath()
        path.moveTo(0, 0)
        for cityIndex in self.currentPath[1:]:
            cityPoint = self.citiesPoint[cityIndex-1]
            path.lineTo(cityPoint.x(), cityPoint.y())

        painter.drawPath(path)

    def drawBackery(self, painter):
        painter.setPen(self.backeryPen)
        [backeryX, backeryY] = self.citiesMap[0]
        backeryPoint = QPoint(backeryX, backeryY)
        painter.drawPoint(backeryPoint)

    def drawCities(self, painter):
        painter.setPen(self.citiesPen)
        for [cityX, cityY] in self.citiesMap[1:]:
            cityPoint = QPoint(cityX, cityY)
            painter.drawPoint(cityPoint)

    def drawCarsPaths(self, painter):
        painter.setPen(self.otherPathsPen)
        for carPath in self.carsPaths:
            if len(carPath) == 1: # don't draw empty path
                continue

            path = QPainterPath()
            path.moveTo(0, 0)
            for cityIndex in carPath[1:]:
                cityPoint = self.citiesPoint[cityIndex-1]
                path.lineTo(cityPoint.x(), cityPoint.y())

            painter.drawPath(path)

    def setCurrentPath(self, path):
        self.currentPath = path;
        self.repaint()

if __name__ == '__main__':
    citiesMap = [[0,0], [100,100], [100,-100], [-100,-100], [-100, 100]]
    paths = [[0, 3, 1], [0, 2, 4]]
    app = QApplication(sys.argv)
    ex = CitiesMapWidget(citiesMap, paths)
    sys.exit(app.exec_())

#     50000, 732, 217, 564, 58
# 217, 50000, 290, 201, 79
# 217, 290, 50000, 113, 303
# 164, 201, 113, 50000, 196
# 58, 89, 403, 196, 50000