#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Distributed under the terms of the GNU General Public License

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
import sys
import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

try:
    from pyspread.cli import PyspreadArgumentParser
    from pyspread.main_window import MainWindow

except ImportError:
    from cli import PyspreadArgumentParser
    from main_window import MainWindow


LICENSE = "GNU GENERAL PUBLIC LICENSE Version 3"

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"


def excepthook(exception_type, exception_value, exception_traceback):
    """Exception hook that prevents pyspread from crashing on exceptions"""

    traceback_msg = "".join(traceback.format_exception(exception_type,
                                                       exception_value,
                                                       exception_traceback))
    print(f"Error: {traceback_msg}\n")


def main():
    """Pyspread main"""

    sys.excepthook = excepthook

    parser = PyspreadArgumentParser()
    args, _ = parser.parse_known_args()

    app = QApplication(sys.argv)
    app.setDesktopFileName("io.gitlab.pyspread.pyspread")
    main_window = MainWindow(args.file, default_settings=args.default_settings)

    main_window.show()

    app.exec()

    sys.exit()


if __name__ == '__main__':
    main()
