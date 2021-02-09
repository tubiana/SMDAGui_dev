# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Design(object):
    def setupUi(self, SMDA):
        SMDA.setObjectName("SMDA")
        SMDA.setGeometry(QtCore.QRect(0, 0, 1074, 861))
        self.centralwidget = QtWidgets.QWidget(SMDA)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_10.addItem(spacerItem)
        self.checkBoxReplicas = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBoxReplicas.setEnabled(False)
        self.checkBoxReplicas.setObjectName("checkBoxReplicas")
        self.horizontalLayout_10.addWidget(self.checkBoxReplicas)
        self.gridLayout_2.addLayout(self.horizontalLayout_10, 1, 1, 1, 1)
        self.listWidgetInputTrajectories = QtWidgets.QListWidget(self.groupBox_4)
        self.listWidgetInputTrajectories.setObjectName("listWidgetInputTrajectories")
        item = QtWidgets.QListWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setFlags(
            QtCore.Qt.ItemIsSelectable
            | QtCore.Qt.ItemIsEditable
            | QtCore.Qt.ItemIsDragEnabled
            | QtCore.Qt.ItemIsUserCheckable
            | QtCore.Qt.ItemIsEnabled
        )
        self.listWidgetInputTrajectories.addItem(item)
        self.gridLayout_2.addWidget(self.listWidgetInputTrajectories, 0, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_4)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_39 = QtWidgets.QLabel(self.tab)
        self.label_39.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_39.setObjectName("label_39")
        self.horizontalLayout_4.addWidget(self.label_39)
        self.lineEditInputStripping = QtWidgets.QLineEdit(self.tab)
        self.lineEditInputStripping.setText("")
        self.lineEditInputStripping.setObjectName("lineEditInputStripping")
        self.horizontalLayout_4.addWidget(self.lineEditInputStripping)
        self.gridLayout_4.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.checkBoxRemoveWater = QtWidgets.QCheckBox(self.tab)
        self.checkBoxRemoveWater.setChecked(True)
        self.checkBoxRemoveWater.setObjectName("checkBoxRemoveWater")
        self.horizontalLayout_12.addWidget(self.checkBoxRemoveWater)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_12.addItem(spacerItem1)
        self.checkBoxHasLigand = QtWidgets.QCheckBox(self.tab)
        self.checkBoxHasLigand.setObjectName("checkBoxHasLigand")
        self.horizontalLayout_12.addWidget(self.checkBoxHasLigand)
        self.gridLayout_4.addLayout(self.horizontalLayout_12, 4, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_35 = QtWidgets.QLabel(self.tab)
        self.label_35.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_35.setObjectName("label_35")
        self.horizontalLayout_2.addWidget(self.label_35)
        self.lineEditInputTopologyPath = QtWidgets.QLineEdit(self.tab)
        self.lineEditInputTopologyPath.setObjectName("lineEditInputTopologyPath")
        self.horizontalLayout_2.addWidget(self.lineEditInputTopologyPath)
        self.toolButtonInputTopologyButton = QtWidgets.QToolButton(self.tab)
        self.toolButtonInputTopologyButton.setObjectName(
            "toolButtonInputTopologyButton"
        )
        self.horizontalLayout_2.addWidget(self.toolButtonInputTopologyButton)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_21 = QtWidgets.QLabel(self.tab)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_5.addWidget(self.label_21)
        self.lineEditLigandName = QtWidgets.QLineEdit(self.tab)
        self.lineEditLigandName.setEnabled(False)
        self.lineEditLigandName.setObjectName("lineEditLigandName")
        self.horizontalLayout_5.addWidget(self.lineEditLigandName)
        self.gridLayout_4.addLayout(self.horizontalLayout_5, 5, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_37 = QtWidgets.QLabel(self.tab)
        self.label_37.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_37.setObjectName("label_37")
        self.horizontalLayout_3.addWidget(self.label_37)
        self.spinBoxInputDT = QtWidgets.QSpinBox(self.tab)
        self.spinBoxInputDT.setMinimum(1)
        self.spinBoxInputDT.setMaximum(9999)
        self.spinBoxInputDT.setObjectName("spinBoxInputDT")
        self.horizontalLayout_3.addWidget(self.spinBoxInputDT)
        spacerItem2 = QtWidgets.QSpacerItem(
            54, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_3.addItem(spacerItem2)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.pushButtonAddTrajectory = QtWidgets.QPushButton(self.tab)
        self.pushButtonAddTrajectory.setObjectName("pushButtonAddTrajectory")
        self.gridLayout_4.addWidget(self.pushButtonAddTrajectory, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_34 = QtWidgets.QLabel(self.tab_2)
        self.label_34.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_34.setObjectName("label_34")
        self.horizontalLayout_6.addWidget(self.label_34)
        self.lineEditOutputTrajectoryPath = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditOutputTrajectoryPath.setObjectName("lineEditOutputTrajectoryPath")
        self.horizontalLayout_6.addWidget(self.lineEditOutputTrajectoryPath)
        self.toolButtonOutputTrajectoryButton = QtWidgets.QToolButton(self.tab_2)
        self.toolButtonOutputTrajectoryButton.setObjectName(
            "toolButtonOutputTrajectoryButton"
        )
        self.horizontalLayout_6.addWidget(self.toolButtonOutputTrajectoryButton)
        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_40 = QtWidgets.QLabel(self.tab_2)
        self.label_40.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_40.setObjectName("label_40")
        self.horizontalLayout_9.addWidget(self.label_40)
        self.comboBoxOutputFormat = QtWidgets.QComboBox(self.tab_2)
        self.comboBoxOutputFormat.setObjectName("comboBoxOutputFormat")
        self.comboBoxOutputFormat.addItem("")
        self.comboBoxOutputFormat.addItem("")
        self.comboBoxOutputFormat.addItem("")
        self.comboBoxOutputFormat.addItem("")
        self.comboBoxOutputFormat.addItem("")
        self.comboBoxOutputFormat.addItem("")
        self.horizontalLayout_9.addWidget(self.comboBoxOutputFormat)
        spacerItem3 = QtWidgets.QSpacerItem(
            56, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_9.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_9, 4, 0, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_41 = QtWidgets.QLabel(self.tab_2)
        self.label_41.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_41.setObjectName("label_41")
        self.horizontalLayout_13.addWidget(self.label_41)
        self.lineEditOutputStripping = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditOutputStripping.setText("")
        self.lineEditOutputStripping.setObjectName("lineEditOutputStripping")
        self.horizontalLayout_13.addWidget(self.lineEditOutputStripping)
        self.gridLayout.addLayout(self.horizontalLayout_13, 2, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_36 = QtWidgets.QLabel(self.tab_2)
        self.label_36.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_36.setObjectName("label_36")
        self.horizontalLayout_7.addWidget(self.label_36)
        self.lineEditOutputTopologyPath = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditOutputTopologyPath.setObjectName("lineEditOutputTopologyPath")
        self.horizontalLayout_7.addWidget(self.lineEditOutputTopologyPath)
        self.toolButtonOutputTopologyButton = QtWidgets.QToolButton(self.tab_2)
        self.toolButtonOutputTopologyButton.setObjectName(
            "toolButtonOutputTopologyButton"
        )
        self.horizontalLayout_7.addWidget(self.toolButtonOutputTopologyButton)
        self.gridLayout.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_38 = QtWidgets.QLabel(self.tab_2)
        self.label_38.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_38.setObjectName("label_38")
        self.horizontalLayout_8.addWidget(self.label_38)
        self.spinBoxOutDT = QtWidgets.QSpinBox(self.tab_2)
        self.spinBoxOutDT.setMinimum(1)
        self.spinBoxOutDT.setMaximum(9999)
        self.spinBoxOutDT.setObjectName("spinBoxOutDT")
        self.horizontalLayout_8.addWidget(self.spinBoxOutDT)
        spacerItem4 = QtWidgets.QSpacerItem(
            54, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_8.addItem(spacerItem4)
        self.gridLayout.addLayout(self.horizontalLayout_8, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_outputFolder = QtWidgets.QLabel(self.tab_2)
        self.label_outputFolder.setLocale(
            QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates)
        )
        self.label_outputFolder.setObjectName("label_outputFolder")
        self.horizontalLayout.addWidget(self.label_outputFolder)
        self.lineEditOutputFiguresPath = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditOutputFiguresPath.setObjectName("lineEditOutputFiguresPath")
        self.horizontalLayout.addWidget(self.lineEditOutputFiguresPath)
        self.toolButtonOutputFiguresButton = QtWidgets.QToolButton(self.tab_2)
        self.toolButtonOutputFiguresButton.setObjectName(
            "toolButtonOutputFiguresButton"
        )
        self.horizontalLayout.addWidget(self.toolButtonOutputFiguresButton)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 2, 1)
        self.gridLayout_5.addWidget(self.groupBox_4, 1, 4, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setObjectName("label_22")
        self.gridLayout_5.addWidget(self.label_22, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setObjectName("label_23")
        self.verticalLayout_2.addWidget(self.label_23)
        self.treeWidgetChoosenAnalysis = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.treeWidgetChoosenAnalysis.sizePolicy().hasHeightForWidth()
        )
        self.treeWidgetChoosenAnalysis.setSizePolicy(sizePolicy)
        self.treeWidgetChoosenAnalysis.setMinimumSize(QtCore.QSize(0, 256))
        self.treeWidgetChoosenAnalysis.setAcceptDrops(True)
        self.treeWidgetChoosenAnalysis.setDragEnabled(True)
        self.treeWidgetChoosenAnalysis.setDragDropOverwriteMode(False)
        self.treeWidgetChoosenAnalysis.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeWidgetChoosenAnalysis.setAlternatingRowColors(True)
        self.treeWidgetChoosenAnalysis.setColumnCount(1)
        self.treeWidgetChoosenAnalysis.setObjectName("treeWidgetChoosenAnalysis")
        self.treeWidgetChoosenAnalysis.headerItem().setText(0, "1")
        self.treeWidgetChoosenAnalysis.header().setVisible(False)
        self.verticalLayout_2.addWidget(self.treeWidgetChoosenAnalysis)
        self.gridLayout_5.addLayout(self.verticalLayout_2, 0, 3, 2, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem5 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_11.addItem(spacerItem5)
        self.pushButtonRun = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRun.setObjectName("pushButtonRun")
        self.horizontalLayout_11.addWidget(self.pushButtonRun)
        spacerItem6 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_11.addItem(spacerItem6)
        self.gridLayout_5.addLayout(self.horizontalLayout_11, 3, 2, 1, 2)
        self.progressBarAnalyses = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBarAnalyses.setProperty("value", 0)
        self.progressBarAnalyses.setObjectName("progressBarAnalyses")
        self.gridLayout_5.addWidget(self.progressBarAnalyses, 3, 4, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(12, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem7 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem7)
        self.toolButtonAddAnalysis = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonAddAnalysis.setText("")
        self.toolButtonAddAnalysis.setAutoRaise(False)
        self.toolButtonAddAnalysis.setArrowType(QtCore.Qt.RightArrow)
        self.toolButtonAddAnalysis.setObjectName("toolButtonAddAnalysis")
        self.verticalLayout.addWidget(self.toolButtonAddAnalysis)
        self.toolButtonRemoveAnalysis = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonRemoveAnalysis.setArrowType(QtCore.Qt.LeftArrow)
        self.toolButtonRemoveAnalysis.setObjectName("toolButtonRemoveAnalysis")
        self.verticalLayout.addWidget(self.toolButtonRemoveAnalysis)
        spacerItem8 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem8)
        self.gridLayout_5.addLayout(self.verticalLayout, 1, 1, 1, 1)
        self.toolButtonReset = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonReset.setObjectName("toolButtonReset")
        self.gridLayout_5.addWidget(self.toolButtonReset, 2, 1, 1, 1)
        self.treeWidgetAnalysisAvailable = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidgetAnalysisAvailable.setMaximumSize(QtCore.QSize(239, 16777215))
        self.treeWidgetAnalysisAvailable.setDragEnabled(False)
        self.treeWidgetAnalysisAvailable.setDragDropMode(
            QtWidgets.QAbstractItemView.NoDragDrop
        )
        self.treeWidgetAnalysisAvailable.setAlternatingRowColors(True)
        self.treeWidgetAnalysisAvailable.setAnimated(True)
        self.treeWidgetAnalysisAvailable.setHeaderHidden(False)
        self.treeWidgetAnalysisAvailable.setColumnCount(1)
        self.treeWidgetAnalysisAvailable.setObjectName("treeWidgetAnalysisAvailable")
        self.gridLayout_5.addWidget(self.treeWidgetAnalysisAvailable, 1, 0, 2, 1)
        self.tabWidgetParametersResults = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidgetParametersResults.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(252)
        sizePolicy.setHeightForWidth(
            self.tabWidgetParametersResults.sizePolicy().hasHeightForWidth()
        )
        self.tabWidgetParametersResults.setSizePolicy(sizePolicy)
        self.tabWidgetParametersResults.setMinimumSize(QtCore.QSize(761, 421))
        self.tabWidgetParametersResults.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidgetParametersResults.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidgetParametersResults.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidgetParametersResults.setDocumentMode(False)
        self.tabWidgetParametersResults.setTabsClosable(False)
        self.tabWidgetParametersResults.setMovable(False)
        self.tabWidgetParametersResults.setTabBarAutoHide(True)
        self.tabWidgetParametersResults.setObjectName("tabWidgetParametersResults")
        self.tabParameters = QtWidgets.QWidget()
        self.tabParameters.setObjectName("tabParameters")
        self.gridLayoutParameters = QtWidgets.QGridLayout(self.tabParameters)
        self.gridLayoutParameters.setObjectName("gridLayoutParameters")
        self.labelDescription = QtWidgets.QLabel(self.tabParameters)
        self.labelDescription.setObjectName("labelDescription")
        self.gridLayoutParameters.addWidget(self.labelDescription, 0, 0, 1, 1)
        self.tabWidgetParametersResults.addTab(self.tabParameters, "Parameters")
        self.gridLayout_5.addWidget(self.tabWidgetParametersResults, 2, 2, 1, 3)
        self.tabWidgetParametersResults.raise_()
        self.treeWidgetAnalysisAvailable.raise_()
        self.label_22.raise_()
        self.toolButtonReset.raise_()
        self.groupBox_4.raise_()
        self.progressBarAnalyses.raise_()
        SMDA.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SMDA)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1074, 21))
        self.menubar.setObjectName("menubar")
        self.menuFiles = QtWidgets.QMenu(self.menubar)
        self.menuFiles.setObjectName("menuFiles")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        SMDA.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SMDA)
        self.statusbar.setObjectName("statusbar")
        SMDA.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(SMDA)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(SMDA)
        self.actionSave.setObjectName("actionSave")
        self.actionQuit = QtWidgets.QAction(SMDA)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAtomSelection = QtWidgets.QAction(SMDA)
        self.actionAtomSelection.setObjectName("actionAtomSelection")
        self.actionGeneral_help = QtWidgets.QAction(SMDA)
        self.actionGeneral_help.setObjectName("actionGeneral_help")
        self.menuFiles.addAction(self.actionOpen)
        self.menuFiles.addAction(self.actionSave)
        self.menuFiles.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAtomSelection)
        self.menuHelp.addAction(self.actionGeneral_help)
        self.menubar.addAction(self.menuFiles.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(SMDA)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidgetParametersResults.setCurrentIndex(0)
        self.checkBoxHasLigand.toggled["bool"].connect(
            self.lineEditLigandName.setEnabled
        )
        QtCore.QMetaObject.connectSlotsByName(SMDA)

    def retranslateUi(self, SMDA):
        _translate = QtCore.QCoreApplication.translate
        SMDA.setWindowTitle(_translate("Design", "MainWindow"))
        self.groupBox_4.setTitle(_translate("Design", "Input / Output parameters"))
        self.checkBoxReplicas.setToolTip(
            _translate(
                "Design",
                "If several trajectories are given, are they replicas (same topology ?)",
            )
        )
        self.checkBoxReplicas.setText(_translate("Design", "Replicas ?"))
        __sortingEnabled = self.listWidgetInputTrajectories.isSortingEnabled()
        self.listWidgetInputTrajectories.setSortingEnabled(False)
        item = self.listWidgetInputTrajectories.item(0)
        item.setText(_translate("Design", "Add trajectory"))
        item.setToolTip(_translate("Design", "Double click to fill your trajectory"))
        self.listWidgetInputTrajectories.setSortingEnabled(__sortingEnabled)
        self.label_39.setToolTip(
            _translate(
                "Design",
                '<html><head/><body><p>Remove selected atoms from the initial trajectory. </p><p><span style=" font-weight:600;">Help to reduce memory</span></p></body></html>',
            )
        )
        self.label_39.setText(_translate("Design", "Stripping"))
        self.checkBoxRemoveWater.setToolTip(
            _translate(
                "Design",
                '<html><head/><body><p>Remove solvent/water if checked.</p><p><span style=" font-weight:600;">For big trajectory please check this! especially if you don\'t mind the solvent.</span></p></body></html>',
            )
        )
        self.checkBoxRemoveWater.setText(_translate("Design", "Remove water?"))
        self.checkBoxHasLigand.setToolTip(
            _translate("Design", "Click if you want automatic ligand analysis")
        )
        self.checkBoxHasLigand.setText(_translate("Design", "HasLigand ?"))
        self.label_35.setToolTip(_translate("Design", "Topology file"))
        self.label_35.setText(_translate("Design", "Topology"))
        self.toolButtonInputTopologyButton.setText(_translate("Design", "..."))
        self.label_21.setText(_translate("Design", "LigandName"))
        self.label_37.setToolTip(_translate("Design", "Read one frame on <x>"))
        self.label_37.setText(_translate("Design", "Timestep"))
        self.pushButtonAddTrajectory.setText(_translate("Design", "Add trajectory"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab), _translate("Design", "Input")
        )
        self.label_34.setToolTip(_translate("Design", "output trajectory"))
        self.label_34.setText(_translate("Design", "Trajectory"))
        self.lineEditOutputTrajectoryPath.setToolTip(
            _translate("Design", "output trajectory")
        )
        self.toolButtonOutputTrajectoryButton.setText(_translate("Design", "..."))
        self.label_40.setToolTip(_translate("Design", "Output format"))
        self.label_40.setText(_translate("Design", "Format"))
        self.comboBoxOutputFormat.setToolTip(_translate("Design", "Output format"))
        self.comboBoxOutputFormat.setItemText(0, _translate("Design", "nc"))
        self.comboBoxOutputFormat.setItemText(1, _translate("Design", "xtc"))
        self.comboBoxOutputFormat.setItemText(2, _translate("Design", "trr"))
        self.comboBoxOutputFormat.setItemText(3, _translate("Design", "ncrst"))
        self.comboBoxOutputFormat.setItemText(4, _translate("Design", "dcd"))
        self.comboBoxOutputFormat.setItemText(5, _translate("Design", "pdb"))
        self.label_41.setToolTip(
            _translate(
                "Design",
                '<html><head/><body><p>Remove selected atoms from the initial trajectory. </p><p><span style=" font-weight:600;">Help to reduce memory</span></p></body></html>',
            )
        )
        self.label_41.setText(_translate("Design", "Stripping"))
        self.lineEditOutputStripping.setToolTip(
            _translate(
                "Design",
                '<html><head/><body><p><span style=" font-weight:600;">OPTIONAL</span> : if you want to strip some part of the dynamic.</p></body></html>',
            )
        )
        self.label_36.setToolTip(_translate("Design", "output topology"))
        self.label_36.setText(_translate("Design", "Topology"))
        self.lineEditOutputTopologyPath.setToolTip(
            _translate("Design", "output topology")
        )
        self.toolButtonOutputTopologyButton.setText(_translate("Design", "..."))
        self.label_38.setToolTip(_translate("Design", "Save one frame on <x>"))
        self.label_38.setText(_translate("Design", "Timestep"))
        self.spinBoxOutDT.setToolTip(_translate("Design", "Save one frame on <x>"))
        self.label_outputFolder.setToolTip(
            _translate(
                "Design",
                "<html><head/><body><p>Output folder (for figures). Per default it's the name of the topology</p></body></html>",
            )
        )
        self.label_outputFolder.setText(_translate("Design", "Output Folder"))
        self.toolButtonOutputFiguresButton.setText(_translate("Design", "..."))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2), _translate("Design", "Output")
        )
        self.label_22.setText(_translate("Design", "Available Analyses"))
        self.label_23.setText(_translate("Design", "Choosen Analyses"))
        self.pushButtonRun.setText(_translate("Design", "RUN!"))
        self.toolButtonAddAnalysis.setToolTip(_translate("Design", "Add an analysis"))
        self.toolButtonRemoveAnalysis.setToolTip(
            _translate("Design", "Remove an analysis")
        )
        self.toolButtonRemoveAnalysis.setText(_translate("Design", "..."))
        self.toolButtonReset.setText(_translate("Design", "RESET"))
        self.treeWidgetAnalysisAvailable.setSortingEnabled(True)
        self.treeWidgetAnalysisAvailable.headerItem().setText(
            0, _translate("Design", "Analyses")
        )
        self.labelDescription.setText(
            _translate(
                "Design",
                '<html><head/><body><p align="center"><span style=" font-size:16pt; font-weight:600;">Welcome in SMDAgui!</span></p><p><span style=" text-decoration: underline;">To begin</span> : </p><p>1. Fill <span style=" font-weight:600;">INPUT</span> and/or <span style=" font-weight:600;">OUTPUT</span> parameters</p><p>2. Choose an Analysis from the <span style=" font-style:italic;">Analysis menu</span> (on the left)</p><p>3. Add it on the <span style=" font-style:italic;">Choosen Analysis list</span> (upside) by clicking on the <span style=" font-style:italic;">righ arrow</span></p><p>4. Fill parameters</p><p>5. Do it for each analysis you want</p><p>6. Click on <span style=" font-weight:600;">RUN!</span></p><p><br/></p></body></html>',
            )
        )
        self.menuFiles.setTitle(_translate("Design", "&Files"))
        self.menuHelp.setTitle(_translate("Design", "Help"))
        self.actionOpen.setText(_translate("Design", "&Open"))
        self.actionOpen.setShortcut(_translate("Design", "Ctrl+O"))
        self.actionSave.setText(_translate("Design", "&Save"))
        self.actionSave.setShortcut(_translate("Design", "Ctrl+S"))
        self.actionQuit.setText(_translate("Design", "&Quit"))
        self.actionQuit.setShortcut(_translate("Design", "Ctrl+Q"))
        self.actionAtomSelection.setText(_translate("Design", "Atom selection"))
        self.actionAtomSelection.setShortcut(_translate("Design", "Ctrl+A"))
        self.actionGeneral_help.setText(_translate("Design", "Genral help"))
        self.actionGeneral_help.setShortcut(_translate("Design", "Ctrl+H"))
