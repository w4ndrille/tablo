
from pathlib import Path
from typing import Tuple

try:
    from markdown2 import markdown
except ImportError:
    markdown = None

from PyQt6.QtCore import pyqtSignal, QSize, Qt, QModelIndex, QPoint
from PyQt6.QtWidgets \
    import (QToolButton, QColorDialog, QFontComboBox, QComboBox, QSizePolicy,
            QLineEdit, QPushButton, QTextBrowser, QWidget, QMainWindow,
            QMenu, QTableView)
from PyQt6.QtGui import (QPalette, QColor, QFont, QIntValidator, QCursor,
                         QIcon, QAction)

try:
    from pyspread.actions import Action
    from pyspread.icons import Icon
    from pyspread.lib.csv import typehandlers, currencies
except ImportError:
    from actions import Action
    from icons import Icon
    from lib.csv import typehandlers, currencies





class Widgets:
    """Container class for widgets"""

    def __init__(self, graph_window: QMainWindow):
        """
        :param graph_window: Application graph_window

        """

        # Format toolbar widgets
"""
        self.font_combo = FontChoiceCombo(main_window)

        self.font_size_combo = FontSizeCombo(main_window)
""""""
        text_color = QColor("black")
        self.text_color_button = TextColorButton(text_color)

        background_color = QColor("white")
        self.background_color_button = BackgroundColorButton(background_color)

        line_color = QColor("black")
        self.line_color_button = LineColorButton(line_color)

        self.renderer_button = RendererButton(main_window)
        self.rotate_button = RotationButton(main_window)
        self.justify_button = JustificationButton(main_window)
        self.align_button = AlignmentButton(main_window"""