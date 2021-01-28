#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 08:57:43 2019

@author: tta_sur
"""

import sys
from PyQt5.QtWidgets import QApplication
import ui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindows = ui.core.MainWindow()
    mainWindows.show()
    print("test")
    rc=app.exec()
    sys.exit(rc)