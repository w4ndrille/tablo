
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
from PyQt6.QtWebEngineWidgets import QWebEngineView
from lib.attrdict import AttrDict
#import graphiques
import numpy as np
import plotly
import plotly.graph_objects as go

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

"""
FONCTIONNEMENT :
 


"""
class Graph(QWebEngineView):
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
        self.chart = '<html><body>'


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

        ##zone de test pour QWebEngine
        x = np.arange(1000)
        y= x**2

        fig = go.Figure(go.Scatter(x=x, y=y,name="Name Scatter"))
        #Pour ajouter les légends
        fig.update_layout(
            title="Scatter",
            xaxis_title="les x",
            yaxis_title="les y",
            legend_title="Legend title",
            font=dict(
                family="Courrier New",
                size =18,
                color="Red"
            ),
        )

        #permet d'avoir l'écriture scientifique / a enlever si on veut l'écriture simple en mettant ="none"
        fig.update_yaxes(exponentformat='E')
        ##
        self.chart += plotly.offline.plot(fig, output_type='div',include_plotlyjs='cdn')
        self.chart += '</body></html>'
        self.setHtml(self.chart)







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
