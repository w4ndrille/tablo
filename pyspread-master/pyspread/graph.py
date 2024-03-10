
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
#import every math functions usable with np array
from numpy import *
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
    def __init__(self, parent:QMainWindow, figs = None):
        super().__init__()
        self.parent = parent
        self.axisLabels = []
        # shorting the accesser to data
        self.model = self.parent.grid.model
        # the figure supporting our model
        self.fig = go.Figure()
        #getting all the figures on a reload
        if figs is None:
            self.figs = []
        else:
            self.figs = figs
            self.rebuild()

        #array of values or maybe array for multiploting
        self.xValues= []
        self.yValues = []



        self.get_series()
        self._init_chart()


        self.update_chart()


    def _init_chart(self):
        #the first html balise for the widget
        self.chart = '<html><body>'


    def get_series(self, colIndexX :int = 0,colIndexY :int = 1):
        """
        Getting the curve from X col and Y col
        """
        max = 150 # it matches the maximum row index
        inc = 1 #start at 1 to avoid getting the physical meaning of the column


        while inc < max :
            x = self.model.index(inc,colIndexX).data()
            y = self.model.index(inc,colIndexY).data()

            if x == "" or y == "":
                break

            self.xValues.append(int(x))
            self.yValues.append(int(y))

            inc += 1

        self.axisLabels.append(self.model.index(0,colIndexX).data())
        self.axisLabels.append(self.model.index(0,colIndexY).data())


    def rebuild(self):
        self.chart = "<html><body>"
        #create a np array from -100 to 100 and create the y array associated

        for i in range(len(self.figs)):

            self.fig.add_traces(self.figs[i])

        self.chart += plotly.offline.plot(self.fig, output_type='div', include_plotlyjs='cdn')
        self.chart += '</body></html>'
        self.setHtml(self.chart)


    def update_chart(self):
        """
        Update the chart with all the series
        """

        self.fig.add_traces(go.Scatter(x=self.xValues, y=self.yValues,name="Name Scatter"))

        #Pour ajouter les légends
        self.fig.update_layout(
            xaxis_title=self.axisLabels[0],
            yaxis_title=self.axisLabels[1],
            legend_title="Legend title",
        )

        #permet d'avoir l'écriture scientifique / a enlever si on veut l'écriture simple en mettant ="none"
        self.fig.update_yaxes(exponentformat='E')

        self.chart += plotly.offline.plot(self.fig, output_type='div',include_plotlyjs='cdn')
        self.chart += '</body></html>'
        self.setHtml(self.chart)


    def add_modele(self,equation:str ,from_:int,to_:int):
        self.chart = "<html><body>"

        #create a np array from -100 to 100 and create the y array associated
        x = np.arange(from_,to_,0.1)
        y = eval(equation)


        self.fig.add_traces(go.Scatter(x=x, y=y,name=equation))

        #adding the trace in to the figs
        self.figs.append(go.Scatter(x=x, y=y,name=equation))
        self.chart += plotly.offline.plot(self.fig, output_type='div', include_plotlyjs='cdn')
        self.chart += '</body></html>'
        self.setHtml(self.chart)

