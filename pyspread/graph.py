
from ast import literal_eval
from contextlib import contextmanager
from io import BytesIO
from typing import Any, Iterable, List, Tuple, Union

import numpy

from PyQt6.QtWidgets \
    import (QTableView, QStyledItemDelegate, QTabBar, QWidget, QMainWindow,
            QStyleOptionViewItem, QApplication, QStyle, QAbstractItemDelegate,
            QHeaderView, QFontDialog, QInputDialog, QLineEdit,
            QAbstractItemView,QGraphicsItem,QErrorMessage)
from PyQt6.QtGui \
    import (QColor, QBrush, QFont, QPainter, QPalette, QImage, QKeyEvent,
            QTextOption, QAbstractTextDocumentLayout, QTextDocument,
            QWheelEvent, QContextMenuEvent, QTextCursor)

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
from scipy.optimize import curve_fit, OptimizeWarning

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
        self.axisLabels = {}
        # shorting the accesser to data
        self.model = self.parent.grid.model
        # the figure supporting our model
        self.fig = go.Figure()

        #a variable to remember the type of axis
        self.typeAxis = 'linear'
        # array of values or maybe array for multiploting
        self.xValues = []
        self.yValues = []


        # creating another array to stock the modelisation
        self.modelisationCurves = []
        # data curves
        self.data_curves = []
        #bornes lines
        self.bornes = [] # append( ["y = 5",5 )

        self.get_series()
        # getting all the figures on a reload
        if figs is None:
            self.figs = []


        else:
            self.figs = figs
            self.rebuild()




        self.allParameters = {
            'polynomiale': [["Polynomiale",r'$y = ax⁷ + bx⁶ +cx⁵ +dx⁴ +ex³ +fx² +gx +h$'
                             ], "a", "b", "c", "d", "e", "f", "g", "h"],
            'linéaire': [["Linéaire",
                          r'$y=ax$'],'a'],
            'affine': [["Affine", r'$y=ax+b$'
                        ], "a", "b"],
            'logarithme': [["Logarithme", r'$y = aln(x+b)$'
                            ], "a", "b"],
            'exponentiale': [["Exponentiel", r'$y = exp(ax+b )$'
                              ], "a", "b"],
            'parabole': [
                ["Parabole", r'$y = ax² + bx + c$'
                 ], "a", "b", "c"],
            'sigmoïde': [["Sigmoïde",
                          r' $\frac{1}{1 + e^{-\lambda(x - x_{0})}}$'
                          ], "<span>&lambda;</span>", "x<sub>0</sub>"],
            'michaelis': [["Michaelis", r'$\frac{v_{max}\times x}{K_{M}+x}$'
                           ], "v<sub>max</sub>", "K<sub>M</sub>"],
            'gauss': [["Gauss", r'$\frac{e^{\frac{-(x-\mu)²}{\sigma²}}}{2\sqrt{\sigma}}$'
                       ], "<span>&sigma;</span>", "<span>&mu;</span>"],
            'lorentz': [["Lorentz",
                         r'$\frac{\frac{\Gamma}{2\pi}}{\frac{\Gamma²}{4} + (x-x_{0})²}$'
                         ], "<span>&Gamma;</span>", "x<sub>0</sub>;"]

        }

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





    def get_series(self, colIndexX :int = 0,colIndexY :int =1,parameters = None):
        """
        Getting the curve from X col and Y col
        """
        max = self.model.shape[0] # it matches the maximum row index
        inc = 1 # start at 1 to avoid getting the physical meaning of the column


        while inc < max :
            x = self.model.index(inc,colIndexX).data()
            y = self.model.index(inc,colIndexY).data()

            if x == "" or y == "":
                break

            self.xValues.append(float(x))
            self.yValues.append(float(y))

            inc += 1

        self.axisLabels[colIndexX] = self.model.index(0,colIndexX).data()
        self.axisLabels[colIndexY] = self.model.index(0,colIndexY).data()

        if len(self.xValues) > 0:
            self.data_curve(parameters,colIndexX,colIndexY)


    def rebuild(self):

        self.fig = go.Figure()#redefining the figure
        self.fig.update_layout(
            xaxis_title=self.axisLabels[0],
            yaxis_title=self.axisLabels[1],
            legend_title="Légende",

        )
        self.fig.update_yaxes(exponentformat='E')

        for i in range(len(self.figs)):
            self.fig.add_traces(self.figs[i][1])

        self.reload()


    def data_curve(self,parameters,colIndexX,colIndexY):
        """
        Update the chart with all the series
        """
        if parameters is None:
            self.fig.add_traces(go.Scatter(x=self.xValues,y=self.yValues,name=self.axisLabels[colIndexY] + " en fonction " + self.axisLabels[colIndexX]))
            self.data_curves.append([self.axisLabels[colIndexY] + " en fonction " + self.axisLabels[colIndexX],go.Scatter(x=self.xValues,y=self.yValues,name=self.axisLabels[1] + " en fonction " + self.axisLabels[0])])
        else:
            self.fig.add_traces(go.Scatter(x=self.xValues,y=self.yValues,name=self.axisLabels[colIndexY] + " en fonction " + self.axisLabels[colIndexX],line=go.scatter.Line(color=parameters[0],dash=parameters[1],width=parameters[2])))
        #Pour ajouter les légends
        self.fig.update_layout(
            xaxis_title=self.axisLabels[0],
            yaxis_title=self.axisLabels[1],
            legend_title="Légende",
        )
        #permet d'avoir l'écriture scientifique / a enlever si on veut l'écriture simple en mettant ="none"
        self.fig.update_yaxes(exponentformat='E')

        self.reload()



    def add_manual_modele(self,equation:str ,from_:int,to_:int):


        #create a np array from -100 to 100 and create the y array associated
        x = np.arange(from_,to_,0.1)
        y = eval(equation)


        self.fig.add_traces(go.Scatter(x=x,y=y,name=equation))
        #adding the trace in to the figs
        self.figs.append([equation,go.Scatter(x=x,y=y,name=equation)])

        self.reload()

    def add_common_modele(self,name:str , parameters, perso_choices,from_,to_):

        x = np.arange(from_,to_,0.1)
        y = self.functionDict[name.lower()](x,*parameters)

        for i in parameters:
            name += " " + str(i) +","
        trace = go.Scatter(x=x,y=y,name=name,line=go.scatter.Line(color=perso_choices[0],dash=perso_choices[1],width=perso_choices[2]))
        self.figs.append([name,trace])
        self.fig.add_traces(trace)
        self.reload()

    def add_bornes(self,axis:str,where:int,perso_choices):
        if axis =="x":
            self.fig.add_vline(x=where,line_width=perso_choices[2], line_dash=perso_choices[1], line_color=perso_choices[0])
            self.bornes.append([axis + " = " + str(where),axis,where,perso_choices])

        elif axis =="y":
            self.fig.add_hline(y=where,line_width=perso_choices[2], line_dash=perso_choices[1], line_color=perso_choices[0])
            self.bornes.append([axis + " = " + str(where),axis,where,perso_choices])
        self.reload()


    def scaling(self):

        if self.typeAxis =='linear':
            self.fig.update_layout(
                xaxis= go.layout.XAxis(type='log'),
                yaxis =  go.layout.YAxis(type='log')
            )
            self.typeAxis = 'log'

        elif self.typeAxis =='log':
            self.fig.update_layout(
                xaxis = go.layout.XAxis(type='linear'),
                yaxis = go.layout.YAxis(type='linear')
            )
            self.typeAxis = 'linear'

        self.fig.update_yaxes(exponentformat='E')
        self.fig.update_xaxes(exponentformat='E')
        self.reload()

    def scaling_disjoint(self,on_xaxis,on_yaxis):
        self.fig.update_layout(
            xaxis=go.layout.XAxis(type=on_xaxis),
            yaxis=go.layout.YAxis(type=on_yaxis)
        )
        self.typeAxis = on_xaxis #putting one or the other do not matter, it's just to prevent the use of the normal scaling button
        self.fig.update_yaxes(exponentformat='E')
        self.fig.update_xaxes(exponentformat='E')
        self.reload()


    def reload(self):

        self.chart = "<html><body>"
        self.chart += plotly.offline.plot(self.fig, output_type='div', include_plotlyjs='cdn')
        self.chart += "</body></html>"
        self.setHtml(self.chart)

    def reload_on_deletion(self):
        self.fig = go.Figure()  # redefining the figure
        self.fig.update_layout(
            xaxis_title=self.axisLabels[0],
            yaxis_title=self.axisLabels[1],
            legend_title="Légende",

        )
        self.fig.update_yaxes(exponentformat='E')

        #Adding all the curves except the ones deleted
        for i in range(len(self.figs)):
            self.fig.add_traces(self.figs[i][1])

        for i in range(len(self.modelisationCurves)):
            self.fig.add_traces(self.modelisationCurves[i][1])

        for i in range(len(self.data_curves)):
            self.fig.add_traces(self.data_curves[i][1])

        for i in range(len(self.bornes)):
            if self.bornes[i][1] == "x":
                self.fig.add_hline(x=self.bornes[i][2],line_width=self.bornes[i][3][2], line_dash=self.bornes[i][3][1], line_color=self.bornes[i][3][0])
            else:
                self.fig.add_vline(x=self.bornes[i][2],line_width=self.bornes[i][3][2], line_dash=self.bornes[i][3][1], line_color=self.bornes[i][3][0])


        self.reload()

    def evaluate(self, name:str):


        # testing if there is  data
        if self.xValues ==  [] or self.yValues == [] :
            return False
        else:

            if name.lower() == "logarithme" and min(self.xValues) <= 0:
                QErrorMessage(self).showMessage("Logarithme mais x <= 0")
                return True
            #getting the optimal parameters and the covariance matrix
            try:
                popt, pcov = curve_fit(self.functionDict[name.lower()],self.xValues,self.yValues)

            except RuntimeError:
                QErrorMessage(self).showMessage("Erreur: Le modèle ne peut pas être évaluer")
            except RuntimeWarning:
                print("Overflow")
            except OptimizeWarning:
                print("impossibilité de calculer la variance")

            maxX,minX = max(self.xValues),min(self.xValues)

            x = np.arange(minX-10,maxX+10,0.1)
            y = self.functionDict[name.lower()](x,*popt)

            if len(self.modelisationCurves) == 1 : # si il y a déjà une modélisation, on la remplace, on rebuild et paf
                self.modelisationCurves[0][1] = go.Scatter(x=x,y=y,name="Estimation de la courbe des données")
                self.rebuild()
            else:
                self.modelisationCurves.append(["Modélisation",go.Scatter(x=x,y=y,name="Estimation de la courbe des données")])


            self.fig.add_traces(self.modelisationCurves[0][1])


            #adding the modele
            self.reload()
            #sending the name and the array of parameters to the parameters widget
            self.parent.showParameters.setParameters(name.lower(),popt,sqrt(diag(pcov)))
            self.parent.showParameters.show()

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
                 if fct =="exponentiale" and max(self.xValues) > 50 :
                     continue
                 try:
                    popt, pcov = curve_fit(self.functionDict[fct], self.xValues, self.yValues)
                 except RuntimeError:
                     QErrorMessage(self).showMessage("Erreur: Le modèle ne peut pas être évaluer")
                 except RuntimeWarning:
                     print("Overflow")
                 except OptimizeWarning:
                     print("impossibilité de calculer la variance")

                 all_variances[fct] =sqrt(diag(pcov))


                 sum = 0
                 for var in sqrt(diag(pcov)):
                    sum += var
                 sum_variances[fct] = sum

        #debugging, uncomment to see
        #print(all_variances)
        #print(sum_variances)

        #then plotting the right modele
        self.evaluate( min(sum_variances, key=sum_variances.get))
        return True

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