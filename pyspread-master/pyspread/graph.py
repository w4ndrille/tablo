
from ast import literal_eval
from contextlib import contextmanager
from io import BytesIO
from typing import Any, Iterable, List, Tuple, Union

import numpy

from PyQt6.QtWidgets \
    import (QTableView, QStyledItemDelegate, QTabBar, QWidget, QMainWindow,
            QStyleOptionViewItem, QApplication, QStyle, QAbstractItemDelegate,
            QHeaderView, QFontDialog, QInputDialog, QLineEdit,
            QAbstractItemView,QGraphicsItem)
from PyQt6.QtGui \
    import (QColor, QBrush, QFont, QPainter, QPalette, QImage, QKeyEvent,
            QTextOption, QAbstractTextDocumentLayout, QTextDocument,
            QWheelEvent, QContextMenuEvent, QTextCursor)

from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QBarSet, QBarSeries, QPieSeries, QScatterSeries,QValueAxis

from PyQt6.QtCore \
    import (Qt, QAbstractTableModel, QModelIndex, QVariant, QEvent, QSize,
            QRect, QRectF, QItemSelectionModel, QObject, QAbstractItemModel,
            QByteArray, pyqtSignal)

from lib.attrdict import AttrDict
try:
    import matplotlib
    import matplotlib.figure
except ImportError:
    matplotlib = None



FONTSTYLES = (QFont.Style.StyleNormal,
              QFont.Style.StyleItalic,
              QFont.Style.StyleOblique)

"""
 Like the grid.py
"""

class Graph(QChartView):
    def __init__(self, parent:QMainWindow, model=None):
        super().__init__()
        self.parent = parent
        self.series = [] #an array for all the plot | it's an array of Series especially XYSeries mother class
        self.axisLabels = []

        #shorting the accesser to data
        self.model = self.parent.grid.model

        self.axisX = QValueAxis()
        self.axisY = QValueAxis()

        self.get_series()
        self._init_chart()


        self.update_chart()


    def _init_chart(self):
        """
        Define the main chart and all the legends and axis
        """
        # The main chart which support the series
        self.chart = QChart()
        self.chart.legend().setVisible(False)

        #setting up the normal Axis
        self.axisX.setTickCount(10)
        self.axisY.setTickCount(10)

        #Possibility to add an axis on the right side for multi-plotting
        self.chart.addAxis(self.axisX, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignmentFlag.AlignLeft)


    def get_series(self, selectSeriesType : bool = False, colIndexX :int = 0,colIndexY :int = 1):
        """
        Getting the curve from X col and Y col
        """
        max = 150 # it matches the maximum row index
        inc = 1 #start at 1 to avoid getting the physical meaning of the column

        if selectSeriesType:
            series = QScatterSeries()
        else:
            series = QLineSeries()

        while inc < max :
            x = self.model.index(inc,colIndexX).data()
            y = self.model.index(inc,colIndexY).data()

            if x == "" or y == "":
                break

            series.append(int(x), int(y))

            inc += 1

        self.axisLabels.append(self.model.index(0,colIndexX).data())
        self.axisLabels.append(self.model.index(0,colIndexY).data())

        self.series.append(series)


    def update_chart(self):
        """
        Update the chart with all the series
        """
        n = len(self.series)

        #setting the labels
        self.axisX.setTitleText(self.axisLabels[0])
        self.axisY.setTitleText(self.axisLabels[1])


        for i in range(n):
            self.chart.addSeries(self.series[i])



            self.series[i].attachAxis(self.axisY)
            self.series[i].attachAxis(self.axisX)

        self.setChart(self.chart)







class GridTableModel(QAbstractTableModel):
    """QAbstractTableModel for Grid"""

    cell_to_update = pyqtSignal(tuple)

    def __init__(self, main_window: QMainWindow,
                 shape: Tuple[int, int, int]):
        """
        :param main_window: Application main window
        :param shape: Grid shape `(rows, columns, tables)`

        """

        super().__init__()

        self.main_window = main_window
