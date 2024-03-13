#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright Martin Manns
# Distributed under the terms of the GNU General Public License

# --------------------------------------------------------------------
# pyspread is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyspread is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyspread.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

"""

pyspread
========

- Main Python spreadsheet application
- Run this script to start the application.

**Provides**

* MainApplication: Initial command line operations and application launch
* :class:`MainWindow`: Main windows class

"""

import os
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal, QEvent, QTimer, QRectF
from PyQt6.QtWidgets import (QWidget, QMainWindow, QApplication,
                             QMessageBox, QDockWidget, QVBoxLayout, QHBoxLayout,
                             QStyleOptionViewItem, QSplitter, QDialog, QGraphicsItem, QLineEdit )
try:
    from PyQt6.QtSvgWidgets import QSvgWidget
except ImportError:
    QSvgWidget = None
from PyQt6.QtGui import QColor, QFont, QPalette, QPainter, QUndoStack
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

try:
    from pyspread.__init__ import VERSION, APP_NAME
    from pyspread.settings import Settings, WEB_URL
    from pyspread.icons import Icon, IconPath
    from pyspread.graph import Graph
    from pyspread.grid_renderer import painter_save
    from pyspread.entryline import Entryline
    from pyspread.menus import GraphMenuBar
    from pyspread.toolbar import GraphMainToolBar
    from pyspread.actions import MainWindowActions
    from pyspread.graph_workflows import GraphWorkflows
    from pyspread.widgets import Widgets
    from pyspread.dialogs import (ApproveWarningDialog, PreferencesDialog,
                                  ManualDialog, TutorialDialog,
                                  PrintAreaDialog, PrintPreviewDialog)
    from pyspread.installer import DependenciesDialog
    from pyspread.interfaces.pys import qt62qt5_fontweights
    from pyspread.panels import MacroPanel
    from pyspread.lib.hashing import genkey
    from pyspread.model.model import CellAttributes
except ImportError:
    from __init__ import VERSION, APP_NAME
    from settings import Settings, WEB_URL
    from icons import Icon, IconPath
    from graph import Graph
    from grid_renderer import painter_save
    from entryline import Entryline
    from menus import GraphMenuBar
    from toolbar import GraphMainToolBar
    from actions import GraphWindowActions
    from graph_workflows import GraphWorkflows
    from widgets import Widgets, ShowParametersWidget, InsertModel
    from dialogs import (ApproveWarningDialog, PreferencesDialog, ManualDialog,
                         TutorialDialog, PrintAreaDialog, PrintPreviewDialog,CreateModel)
    from installer import DependenciesDialog
    from interfaces.pys import qt62qt5_fontweights
    from panels import MacroPanel
    from lib.hashing import genkey
    from model.model import CellAttributes
    import grid
    from cli import PyspreadArgumentParser
LICENSE = "GNU GENERAL PUBLIC LICENSE Version 3"

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"


class GraphWindow(QMainWindow):
    """Pyspread main window"""

    gui_update = pyqtSignal(dict)

    def __init__(self,parent : QMainWindow, figs:list = None,
                 default_settings: bool = False):
        """
        :param filepath: File path for inital file to be opened
        :param default_settings: Ignore stored `QSettings` and use defaults

        """
        super().__init__()
        self.parent = parent
        #Only the first grid
        self.grid = parent.grid
        #storing all the figures displayed
        self.figs = figs

        self._loading = True  # For initial loading of pyspread
        self.prevent_updates = False  # Prevents setData updates in grid

        self.settings = Settings(self, reset_settings=default_settings)
        self.workflows = GraphWorkflows(self) #Workflows variable doen't change for code clarity
        self.undo_stack = QUndoStack(self)
        self.refresh_timer = QTimer()

        self._init_widgets()

        self.graph_window_actions = GraphWindowActions(self)
        self.graph_window_toolbar_actions = GraphWindowActions(self,
                                                             shortcuts=False)

        self._init_window()
        self._init_toolbars()

    def _init_window(self):
        """Initialize main window components"""
        self.resize(1200,600) # initial format
        self.setWindowTitle("Graph")
        self.setWindowIcon(Icon.pyspread)

        # Safe mode widget
        self.safe_mode_widget = QSvgWidget(str(IconPath.safe_mode),
                                           self.statusBar())
        msg = f"{APP_NAME} is in safe mode.\nExpressions are not evaluated."
        self.safe_mode_widget.setToolTip(msg)
        self.statusBar().addPermanentWidget(self.safe_mode_widget)
        self.safe_mode_widget.hide()

        self.setMenuBar(GraphMenuBar(self))

    def resizeEvent(self, event: QEvent):
        """Overloaded, aborts on self._loading
        :param event: Resize event
        """
        if self._loading:
            return
        super().resizeEvent(event)


    def _init_widgets(self):
        """Initialize widgets"""

        self.widgets = Widgets(self)

        # We have one main view that is used as default view
        self.graph = Graph(self,self.figs)
        self.main_panel = QWidget(self)

        self.central_layout = QVBoxLayout(self.main_panel)
        self._layout()

        #QApplication.instance().focusChanged.connect(self.on_focus_changed)
        self.gui_update.connect(self.on_gui_update)
        self.refresh_timer.timeout.connect(self.on_refresh_timer)

    def _layout(self):
        """Set all the layout in the Graph Window"""
        self.splitter = QSplitter(Qt.Orientation.Horizontal, self)
        modele_insertion = InsertModel(self)


        splitterBtResNInsert = QSplitter(Qt.Orientation.Vertical,self)
        # defining as self to be able to change it along the evaluation
        self.showParameters = ShowParametersWidget(self)
        splitterBtResNInsert.addWidget(self.showParameters)
        splitterBtResNInsert.addWidget(modele_insertion)
        splitterBtResNInsert.setSizes((100,100))

        self.splitter.addWidget(splitterBtResNInsert)
        self.splitter.addWidget(self.graph)


        self.splitter.setSizes((200,800))

        self.setCentralWidget(self.splitter)


    def modeleDialog(self):
        self.modele_dialog = CreateModel(self)






    def eventFilter(self, source: QWidget, event: QEvent) -> bool:
        """Overloaded event filter for handling QDockWidget close events

        Updates the menu if the macro panel is closed.

        :param source: Source widget of event
        :param event: Any QEvent

        """


        return super().eventFilter(source, event)

    def _init_toolbars(self):
        """Initialize the main window toolbars"""

        self.main_toolbar = GraphMainToolBar(self)

        self.addToolBar(self.main_toolbar)


    def update_action_toggles(self):
        """Updates the toggle menu check states"""

        actions = self.main_window_actions

        maintoolbar_visible = self.main_toolbar.isVisibleTo(self)
        actions.toggle_main_toolbar.setChecked(maintoolbar_visible)

        macrotoolbar_visible = self.macro_toolbar.isVisibleTo(self)
        actions.toggle_macro_toolbar.setChecked(macrotoolbar_visible)

        formattoolbar_visible = self.format_toolbar.isVisibleTo(self)
        actions.toggle_format_toolbar.setChecked(formattoolbar_visible)

        findtoolbar_visible = self.find_toolbar.isVisibleTo(self)
        actions.toggle_find_toolbar.setChecked(findtoolbar_visible)

        entryline_visible = self.entry_line_dock.isVisibleTo(self)
        actions.toggle_entry_line_dock.setChecked(entryline_visible)

        macrodock_visible = self.macro_dock.isVisibleTo(self)
        actions.toggle_macro_dock.setChecked(macrodock_visible)
    @property
    def safe_mode(self) -> bool:
        """Returns safe_mode state. In safe_mode cells are not evaluated."""

        return self.grid.model.code_array.safe_mode

    @safe_mode.setter
    def safe_mode(self, value: bool):
        """Sets safe mode.

        This triggers the safe_mode icon in the statusbar.

        If safe_mode changes from True to False then caches are cleared and
        macros are executed.

        :param value: Safe mode

        """

        if self.grid.model.code_array.safe_mode == bool(value):
            return

        self.grid.model.code_array.safe_mode = bool(value)

        if value:  # Safe mode entered
            self.safe_mode_widget.show()
            # Enable approval menu entry
            self.main_window_actions.approve.setEnabled(True)
        else:  # Safe_mode disabled
            self.safe_mode_widget.hide()
            # Disable approval menu entry
            self.main_window_actions.approve.setEnabled(False)
            # Clear result cache
            self.grid.model.code_array.result_cache.clear()
            # Execute macros
            self.macro_panel.on_apply()

    def on_fullscreen(self):
        """Fullscreen toggle event handler"""

        if self.windowState() == Qt.WindowState.WindowFullScreen:
            self.setWindowState(self._previous_window_state)
        else:
            self._previous_window_state = self.windowState()
            self.setWindowState(Qt.WindowState.WindowFullScreen)

    def on_approve(self):
        """Approve event handler"""

        if ApproveWarningDialog(self).choice:
            self.safe_mode = False

    def on_clear_globals(self):
        """Clear globals event handler"""

        self.grid.model.code_array.result_cache.clear()

        # Clear globals
        self.grid.model.code_array.clear_globals()
        self.grid.model.code_array.reload_modules()

    def on_preferences(self):
        """Preferences event handler (:class:`dialogs.PreferencesDialog`) """

        data = PreferencesDialog(self).data

        if data is not None:
            max_file_history_changed = \
                self.settings.max_file_history != data['max_file_history']

            # Dialog has been approved --> Store data to settings
            for key in data:
                if key == "signature_key" and not data[key]:
                    data[key] = genkey()
                self.settings.__setattr__(key, data[key])

            # Immediately adjust file history in menu
            if max_file_history_changed:
                self.menuBar().file_menu.history_submenu.update()

    def on_dependencies(self):
        """Dependancies installer (:class:`installer.InstallerDialog`) """

        dial = DependenciesDialog(self)
        dial.exec()

    def on_undo(self):
        """Undo event handler"""

        self.undo_stack.undo()

    def on_redo(self):
        """Undo event handler"""

        self.undo_stack.redo()

    def on_toggle_refresh_timer(self, toggled: bool):
        """Toggles periodic timer for frozen cells

        :param toggled: Toggle state

        """

        if toggled:
            self.grid.refresh_frozen_cells()
            self.refresh_timer.start(self.settings.refresh_timeout)
        else:
            self.refresh_timer.stop()

    def on_refresh_timer(self):
        """Event handler for self.refresh_timer.timeout

        Called for periodic updates of frozen cells.
        Does nothing if either the entry_line or a cell editor is active.

        """

        if not self.entry_line.hasFocus() \
           and self.grid.state() != self.grid.State.EditingState:
            self.grid.refresh_frozen_cells()

    def _toggle_widget(self, widget: QWidget, action_name: str, toggled: bool):
        """Toggles widget visibility and updates toggle actions

        :param widget: Widget to be toggled shown or hidden
        :param action_name: Name of action from Action class
        :param toggled: Toggle state

        """

        if toggled:
            widget.show()
        else:
            widget.hide()

        self.main_window_actions[action_name].setChecked(widget.isVisible())

    def on_toggle_main_toolbar(self, toggled: bool):
        """Main toolbar toggle event handler

        :param toggled: Toggle state

        """

        self._toggle_widget(self.main_toolbar, "toggle_main_toolbar", toggled)

    def on_toggle_macro_toolbar(self, toggled: bool):
        """Macro toolbar toggle event handler

        :param toggled: Toggle state

        """

        self._toggle_widget(self.macro_toolbar, "toggle_macro_toolbar",
                            toggled)

    def on_toggle_format_toolbar(self, toggled: bool):
        """Format toolbar toggle event handler

        :param toggled: Toggle state

        """

        self._toggle_widget(self.format_toolbar, "toggle_format_toolbar",
                            toggled)

    def on_toggle_find_toolbar(self, toggled: bool):
        """Find toolbar toggle event handler

        :param toggled: Toggle state

        """

        self._toggle_widget(self.find_toolbar, "toggle_find_toolbar", toggled)

    def on_toggle_entry_line_dock(self, toggled: bool):
        """Entryline toggle event handler

        :param toggled: Toggle state

        """

        self._toggle_widget(self.entry_line_dock, "toggle_entry_line_dock",
                            toggled)

    def on_toggle_macro_dock(self, toggled: bool):
        """Macro panel toggle event handler

        :param toggled: Toggle state

        """

        self._toggle_widget(self.macro_dock, "toggle_macro_dock", toggled)

    def on_manual(self):
        """Show manual browser"""

        dialog = ManualDialog(self)
        dialog.show()

    def on_tutorial(self):
        """Show tutorial browser"""

        dialog = TutorialDialog(self)
        dialog.show()

    def on_about(self):
        """Show about message box"""

        def devs_string(devs: list) -> str:
            """Get string from devs list"""

            devs_str = "".join(f"<li>{dev}</li>" for dev in devs)
            return f"<ul>{devs_str}</ul>"

        devs = ("Martin Manns", "Jason Sexauer", "Vova Kolobok", "mgunyho",
                "Pete Morgan")
        devs_str = devs_string(devs)

        doc_devs = ("Martin Manns", "Bosko Markovic", "Pete Morgan")
        doc_devs_str = devs_string(doc_devs)

        copyright_owner = "Martin Manns"

        about_msg = \
            f"""<b>{APP_NAME}</b><><p>
            A non-traditional Python spreadsheet application<p>
            Version:&emsp;{VERSION}<p>
            Created by:&emsp;{devs_str}<p>
            Documented by:&emsp;{doc_devs_str}<p>
            Copyright:&emsp;{copyright_owner}<p>
            License:&emsp;{LICENSE}<p>
            Web site:&emsp;<a href="{WEB_URL}">{WEB_URL}</a>
            """

        QMessageBox.about(self, f"About {APP_NAME}", about_msg)

    def on_focus_changed(self, old: QWidget, now: QWidget):
        """Handles grid clicks from entry line"""

        if old == self.grid and now == self.entry_line:
            self.grid.selection_mode = False

    def on_gui_update(self, attributes: CellAttributes):
        """GUI update that shall be called on each cell change

        :param attributes: Attributes of current cell

        """

        widgets = self.widgets
        menubar = self.menuBar()

        is_bold = attributes.fontweight is not None and \
            attributes.fontweight > qt62qt5_fontweights(QFont.Weight.Normal)
        self.main_window_actions.bold.setChecked(is_bold)
        self.main_window_toolbar_actions.bold.setChecked(is_bold)

        is_italic = attributes.fontstyle == QFont.Style.StyleItalic
        self.main_window_actions.italics.setChecked(is_italic)
        self.main_window_toolbar_actions.italics.setChecked(is_italic)

        self.main_window_actions.underline.setChecked(attributes.underline)
        self.main_window_toolbar_actions.underline.setChecked(
            attributes.underline)

        self.main_window_actions.strikethrough.setChecked(
            attributes.strikethrough)
        self.main_window_toolbar_actions.strikethrough.setChecked(
            attributes.strikethrough)

        renderer = attributes.renderer
        widgets.renderer_button.set_current_action(renderer)
        widgets.renderer_button.set_menu_checked(renderer)

        self.main_window_actions.freeze_cell.setChecked(attributes.frozen)
        self.main_window_toolbar_actions.freeze_cell.setChecked(
            attributes.frozen)

        self.main_window_actions.lock_cell.setChecked(attributes.locked)
        self.main_window_toolbar_actions.lock_cell.setChecked(
            attributes.locked)
        self.entry_line.setReadOnly(attributes.locked)

        self.main_window_actions.button_cell.setChecked(
            attributes.button_cell is not False)
        self.main_window_toolbar_actions.button_cell.setChecked(
            attributes.button_cell is not False)

        rotation = f"rotate_{int(attributes.angle)}"
        widgets.rotate_button.set_current_action(rotation)
        widgets.rotate_button.set_menu_checked(rotation)
        widgets.justify_button.set_current_action(attributes.justification)
        widgets.justify_button.set_menu_checked(attributes.justification)
        widgets.align_button.set_current_action(attributes.vertical_align)
        widgets.align_button.set_menu_checked(attributes.vertical_align)

        border_action = self.main_window_actions.border_group.checkedAction()
        if border_action is not None:
            icon = border_action.icon()
            menubar.format_menu.border_submenu.setIcon(icon)
            self.format_toolbar.border_menu_button.setIcon(icon)

        border_width_action = \
            self.main_window_actions.border_width_group.checkedAction()
        if border_width_action is not None:
            icon = border_width_action.icon()
            menubar.format_menu.line_width_submenu.setIcon(icon)
            self.format_toolbar.line_width_button.setIcon(icon)

        if attributes.textcolor is None:
            text_color = self.grid.palette().color(QPalette.ColorRole.Text)
        else:
            text_color = QColor(*attributes.textcolor)
        widgets.text_color_button.color = text_color

        if attributes.bordercolor_bottom is None:
            line_color = self.grid.palette().color(QPalette.ColorRole.Mid)
        else:
            line_color = QColor(*attributes.bordercolor_bottom)
        widgets.line_color_button.color = line_color

        if attributes.bgcolor is None:
            bgcolor = self.grid.palette().color(QPalette.ColorRole.Base)
        else:
            bgcolor = QColor(*attributes.bgcolor)
        widgets.background_color_button.color = bgcolor

        if attributes.textfont is None:
            widgets.font_combo.font = QFont().family()
        else:
            widgets.font_combo.font = attributes.textfont
        widgets.font_size_combo.size = attributes.pointsize

        self.main_window_actions.merge_cells.setChecked(
            attributes.merge_area is not None)
        self.main_window_toolbar_actions.merge_cells.setChecked(
            attributes.merge_area is not None)

    def update(self):

        self.close()
        self.parent.workflows.new_window(self.graph.figs[1:],True)
        self = None