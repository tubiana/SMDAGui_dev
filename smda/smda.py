#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 08:57:43 2019

@author: tta_sur
"""
import sys
from PyQt5.QtWidgets import QApplication

try:
    from .ui.core import MainWindow
except:
    from ui.core import MainWindow


def main():
    app = QApplication(sys.argv)
    mainWindows = MainWindow()
    mainWindows.show()
    rc=app.exec()
    sys.exit(rc)

if __name__ == "__main__" and __package__ is None:
    __package__ = "smda"
    main()
