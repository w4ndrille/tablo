"""
test_grid
=========

Unit tests for graph.py and graph_window.py

"""
import numpy as np
from contextlib import contextmanager
from os.path import abspath, dirname, join
import sys
from unittest import TestCase


from PyQt6.QtCore import QItemSelectionModel, QItemSelection
from PyQt6.QtWidgets import QApplication, QAbstractItemView
from PyQt6.QtGui import QFont, QColor


PYSPREADPATH = abspath(join(dirname(__file__) + "/.."))
LIBPATH = abspath(PYSPREADPATH + "/lib")


@contextmanager
def insert_path(path):
    sys.path.insert(0, path)
    yield
    sys.path.pop(0)




with insert_path(PYSPREADPATH):
    from main_window import MainWindow
    from graph_window import GraphWindow


app = QApplication.instance()
if app is None:
    app = QApplication([])
main_window = MainWindow()
graph_window = GraphWindow(main_window)
graph = graph_window.graph

class TestGraph():
    def test_novalue_evaluate(self):
        graph.xValues = []
        assert graph.evaluate("test") == False

    def test_evaluate_logarithm(self):
        graph.xValues = [-56,0]
        graph.yValues = [0,1] #random value
        assert graph.evaluate("logarithme") == True


    def test_polynomiale(self):
        x_test = np.linspace(0,1,100)
        expected = 2*x_test**7 + 3*x_test**6 + 4*x_test**5 + 9*x_test**4 + 8*x_test**3 +4*x_test**2 +6*x_test**1 +1

        for i in range(len(expected)-1):
            assert graph.polynomiale(x_test,2,3,4,9,8,4,6,1)[i] == expected[i]


    def test_linear(self):
        x_test = np.linspace(0,1,100)
        expected = 5*x_test
        for i in range(len(expected)-1):
            assert graph.linear(x_test,5)[i] == expected[i]


    def test_affine(self):
        x_test = np.linspace(0,1,100)
        expected = 8*x_test +6
        for i in range(len(expected)-1):
            assert graph.affine(x_test,8,6)[i] == expected[i]


    def test_logarithm(self):
        x_test = np.linspace(0,1,100)
        expected = 3*np.log(x_test+6)
        for i in range(len(expected)-1):
            assert graph.logarithm(x_test,3,6)[i] == expected[i]


    def test_exponential(self):
        x_test = np.linspace(0,1,100)
        expected = np.exp(2*x_test-23)
        for i in range(len(expected)-1):
            assert graph.exponential(x_test,2,-23)[i] == expected[i]


    def test_parabole(self):
        x_test = np.linspace(0,1,100)
        expected = 3*x_test**2+6*x_test +3
        for i in range(len(expected)-1):
            assert graph.parabole(x_test,3,6,3)[i] == expected[i]

    def test_sigmoide(self):
        x_test = np.linspace(0,1,100)
        expected = 1/(1+ np.exp(-2*(x_test-0.6)))
        for i in range(len(expected)-1):
            assert graph.sigmoide(x_test,2,0.6)[i] == expected[i]

    def test_michaelis(self):
        x_test = np.linspace(0,1,100)
        expected = (10*x_test )/(6+ x_test)
        for i in range(len(expected)-1):
            assert graph.michaelis(x_test,6,10)[i] == expected[i]

    def test_gauss(self):
        x_test = np.linspace(0,1,100)
        expected = np.exp(-(x_test-2)**2/(2*0.5**2))/(0.5*np.sqrt(2*np.pi))
        for i in range(len(expected)-1):
            assert graph.gauss(x_test,2,0.5)[i] == expected[i]

    def test_lorentz(self):
        x_test = np.linspace(0,1,100)
        expected = (4/2*np.pi)/((4**2/4)+(x_test-3)**2)
        for i in range(len(expected)-1):
            assert graph.lorentz(x_test,4,3)[i] == expected[i]

    def test_init_window(self):
        graph_window._init_window()

# testing directly the dialog pop ups
    def test_modeleDialog(self):
        graph_window.modeleDialog()

    def test_deleteDialog(self):
        graph_window.deleteDialog()

    def test_dataAddDialog(self):
        graph_window.dataAddDialog()

    def test_loglinscaleDialog(self):
        graph_window.loglinscaleDialog()

    def test_addBornesDialog(self):
        graph_window.addBornesDialog()

