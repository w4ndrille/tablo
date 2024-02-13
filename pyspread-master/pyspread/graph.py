
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

from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QBarSet, QBarSeries, QPieSeries

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


        series= QPieSeries()
        series.append("Jane", 1)
        series.append("Joe", 2)
        series.append("Andy", 3)
        series.append("Barbara", 4)
        series.append("Axel", 5)

        chart = QChart()
        chart.addSeries(series)

        self.setChart(chart)



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
