
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
from scipy.optimize import curve_fit

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

        #creating another array to stock the modelisation
        self.modelisationCurves = []
        #array of values or maybe array for multiploting
        self.xValues= []
        self.yValues = []



        self.get_series()
        self._init_chart()


        self.update_chart()

        # a dict which contains all the possible functions to avoid the switch / infitite else if case

        self.functionDict = {
            'polynomiale': self.polynomiale,
            'linéaire': self.linear,
            'affine': self.affine,
            'logarithme': self.logarithm,
            'exponentiale': self.exponential,
            'parabole': self.parabole,
            'sigmoïde': self.sigmoide,
            'michaelis': self.michaelis,
            'gauss': self.gauss,
            'lorentz': self.lorentz
        }


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

            self.xValues.append(float(x))
            self.yValues.append(float(y))

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

        self.fig.add_traces(go.Scatter(x=self.xValues,y=self.yValues,name=self.axisLabels[1] + " en fonction " + self.axisLabels[0]))

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


        self.fig.add_traces(go.Scatter(x=x,y=y,name=equation))

        #adding the trace in to the figs
        self.figs.append(go.Scatter(x=x,y=y,name=equation))

        self.chart += plotly.offline.plot(self.fig, output_type='div', include_plotlyjs='cdn')
        self.chart += '</body></html>'
        self.setHtml(self.chart)


    def evaluate(self, name:str):


        # testing if there is  data
        if self.xValues ==  [] or self.yValues == [] :
            return False
        else:


            #getting the optimal parameters and the covariance matrix
            popt, pcov = curve_fit(self.functionDict[name.lower()],self.xValues,self.yValues)
            maxX,minX = max(self.xValues),min(self.xValues)

            x = np.arange(minX-10,maxX+10,0.1)
            y = self.functionDict[name.lower()](x,*popt)

            self.modelisationCurves.append(go.Scatter(x=x,y=y,name="Estimation de la courbe des données"))
            self.fig.add_traces(go.Scatter(x=x,y=y,name="Estimation de la courbe"))
            #adding the modele

            self.chart = "<html><body>"
            self.chart += plotly.offline.plot(self.fig,output_type='div', include_plotlyjs='cdn')
            self.chart += "</body></html>"
            self.setHtml(self.chart)

            return True


    def auto_evaluate(self):
        #try every function to chose the better one with the pcov parameters
        all_variances = {}
        #create an dict to contain the sum of all the variances of all the parameters
        sum_variances = {}
        if self.xValues == [] or self.yValues == []:
            return False
        else:
            for fct in self.functionDict.keys():


                # getting the optimal parameters and the covariance matrix
                 if fct =="logarithme" and min(self.xValues) <= 0 :
                    continue
                 popt, pcov = curve_fit(self.functionDict[fct], self.xValues, self.yValues)
                 all_variances[fct] =sqrt(diag(pcov))

                 sum = 0
                 for var in sqrt(diag(pcov)):
                    sum += var
                 sum_variances[fct] = sum
            return True


        #then plotting the right modele
        self.evaluate( min(sum_variances, key=sum_variances.get))

    # All functions to be evaluate
    def polynomiale(self,x,a:float, b:float, c:float,d:float,e:float,f:float,g:float,h:float):
        return a*x**7+b*x**6 + c*x**5 + d*x**4 + e*x**3 + f*x**2 + g*x + h
    def linear(self,x, a:float):
        return a*x

    def affine(self,x, a:float, b:float):
        return a*x + b
    def logarithm(self,x,a:float, b:float):
        return a*log(x+b)

    def exponential(self,x,a:float,b:float):
        return exp(a*x+b)

    def parabole(self,x,a:float,b:float,c:float):
        return a*x**2 + b*x + c

    def sigmoide(self, x, a : float, x0:float):
        return 1/(1+ exp(-a *(x-x0)))

    def michaelis(self,x,K_M:float,v_max:float):
        #where x = S0
        return (v_max*x )/(K_M + x)
    def gauss(self,x,mu:float,sigma:float):
        return exp(-(x-mu)**2/(2*sigma**2))/(sigma*sqrt(2*pi))
    def lorentz(self,x,gamma:float,x_0 : float):
        return (gamma/2*pi)/((gamma**2/4)+(x-x_0)**2)