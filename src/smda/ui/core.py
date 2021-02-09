#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 11:06:59 2019

@author: tta_sur
"""
import json
import os

import mdtraj as md
import numpy as np
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import sip
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QImage, QKeySequence, QPixmap
from PyQt5.QtWidgets import (
    QFileDialog,
    QGraphicsScene,
    QMainWindow,
    QMessageBox,
    QShortcut,
)

# SMDA IMPORTS
import smda.analysis as anlz

from .design import Ui_Design
from .helpOnSelection import HelpSelection

ONTESTING = False


class MainWindow(QMainWindow, Ui_Design):
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.test_parameters_widget()
        self.add_analysis_on_TreeWidget()
        self.is_runOK = False
        # self.init_graphicsViewLayout()

        self.testShortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        self.testShortcut.activated.connect(self.runTest)
        self.trajSelectionTest = None
        self.parameters = {"class": self.__class__.__name__}
        self.tabResults = []  # List of results tab
        self._numReplica = 1
        self.saveOutput = False
        self.selectionOK = True
        self.LigandsTreeList = None

        # Installing evenFilter
        self.treeWidgetChoosenAnalysis.installEventFilter(self)
        self.treeWidgetAnalysisAvailable.installEventFilter(self)

    ###########################################################################
    # Test function to remove

    @pyqtSlot()
    def runTest(self):

        self.listWidgetInputTrajectories.item(0).setText("../test/example.xtc")
        self.lineEditInputTopologyPath.setText("../test/example.pdb")
        self.ONTESTING = True
        # RMSD
        item = anlz.RMSD.RMSD().__class__(
            self.treeWidgetChoosenAnalysis, self
        )  # Duplication of this item
        item.lineEditName.setText("ProteinTest")
        item.lineEditSelection.setText("protein")
        item.spinBoxRefFrame.setValue(0)
        item.checkBoxPrecentered.setChecked(False)
        # DISTANCES
        item = anlz.Distances.Distances().__class__(
            self.treeWidgetChoosenAnalysis, self
        )  # Duplication of this item
        item.lineEditName.setText("DistanceTest")
        item.lineEditSelection1.setText("residue 1 to 30")
        item.lineEditSelection2.setText("residue 31 to 60")
        # RMSF
        item = anlz.RMSF.RMSF().__class__(
            self.treeWidgetChoosenAnalysis, self
        )  # Duplication of this item
        item.lineEditName.setText("RMSFTest")
        item.lineEditSelection.setText("protein")
        item.checkBoxByResidue.setChecked(True)
        # HBONDS
        # item = anlz.HBonds.HBonds().__class__(self.treeWidgetChoosenAnalysis, self)  # Duplication of this item
        # item.lineEditName.setText("HbondTest")
        # item.lineEditSelection.setText("protein")
        # SS
        # item = anlz.SecondaryStructures().__class__(self.treeWidgetChoosenAnalysis, self)  # Duplication of this item
        # item.lineEditName.setText("Protein")
        # item.lineEditSelection.setText("protein")

        self.on_pushButtonRun_clicked()

    ###########################################################################
    # Tools function

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.FocusIn:
            if obj == self.treeWidgetAnalysisAvailable:
                self.tabParameters.setEnabled(False)
            if obj == self.treeWidgetChoosenAnalysis:
                self.tabParameters.setEnabled(True)
        return super(MainWindow, self).eventFilter(obj, event)

    def setTrajSelectionTest(self, traj):
        self.trajSelectionTest = traj

    @pyqtSlot()
    def on_actionQuit_triggered(self):
        self.close()

    @pyqtSlot()
    def on_actionAtomSelection_triggered(self):
        self.helpSelection = HelpSelection()

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        paramFile, filetype = QFileDialog.getOpenFileName(
            self, "Open parameter file", filter="Parameter file (*.json);; All (*.*)"
        )

        if not paramFile:
            return
        with open(paramFile, "r") as f:
            fileContent = f.read()
        try:
            allParameters = json.loads(fileContent)
        except Exception:
            QMessageBox.warning(self, "Error", "Error while reading saving file")
            return

        self.is_runOK = True  # May cause bugs or crash. solution : put this into parameters dict and save restore it ?
        itemLoaded = 0

        self.load_param_recurcive(
            allParameters, itemLoaded, "self.treeWidgetChoosenAnalysis"
        )
        # reset progressBar after wards

    def load_param_recurcive(self, allParameters, itemLoaded, parentWidget):
        """
        Subfunction to load parameters recurcivly
        Args:
            allParameters list(dict) : list of dictionnary with all analysis settings
            itemLoaded (int): number of item Loaded
            parentWidget (str): parent widget as a string (will be converted in object with eval function)
        Returns:

        """
        for param in allParameters:
            if list(param.keys())[0] == "LIGAND":
                self.LigandsTreeList = QtWidgets.QTreeWidgetItem(eval(parentWidget))
                self.LigandsTreeList.setText(0, "LIGAND")
                self.load_param_recurcive(
                    param["LIGAND"], itemLoaded, "self.LigandsTreeList"
                )
            else:
                # Restore Main WIndow parameters (trajectoryies, topologies, input/output options).
                if param["class"] == self.__class__.__name__:
                    self.copyIOParametersFromDict(param)
                    self.parameters = param
                else:
                    item = eval(
                        "anlz.{}.{}({}, self)".format(
                            param["class"], param["class"], parentWidget
                        )
                    )
                    item.loadFromDict(param)
                    self.on_treeWidgetChoosenAnalysis_itemSelectionChanged()
                self.update()
                itemLoaded += 1
                progression = (itemLoaded) / len(allParameters) * 100
                self.progressBarAnalyses.setValue(progression)

    @pyqtSlot()
    def on_actionSave_triggered(self):
        self.copyIOParametersToDict()

        (paramFile, filetype) = QFileDialog.getSaveFileName(
            self, "Save file", filter="Parameter file (*.json);; All (*.*)"
        )

        if os.path.exists(paramFile):
            os.remove(paramFile)

        if self.checkBoxReplicas.isChecked():
            numReplica = self.listWidgetInputTrajectories.count()
        else:
            numReplica = 1

        itemsToSaved = [self.parameters]
        self.parameters["numReplica"] = numReplica

        # update  paramete dictionnary of each analysis item and then update the itemsToSave list.

        def retrieve_recurcive(root, itemsToSave):

            child_count = root.childCount()
            for i in range(child_count):
                item = root.child(i)
                if not item.text(0) == "LIGAND":
                    item.retrieve_parameters()
                    item.add_outPath_in_parameters(numReplica)
                    item.parameters["numReplica"] = numReplica
                    itemsToSave.append(item.parameters)
                else:
                    treeDict = {item.text(0): []}
                    retrieve_recurcive(item, treeDict[item.text(0)])
                    itemsToSave.append(treeDict)

        root = self.treeWidgetChoosenAnalysis.invisibleRootItem()
        retrieve_recurcive(root, itemsToSaved)

        if not paramFile == "":
            with open(paramFile, "a") as f:
                f.write(json.dumps(itemsToSaved, indent=4))

    @pyqtSlot(str)
    def on_lineEditInputTopologyPath_textChanged(self, str):
        self.copyIOParametersToDict()

    @pyqtSlot(str)
    def on_lineEditOutputTrajectoryPath_textChanged(self, str):
        self.copyIOParametersToDict()

    @pyqtSlot(str)
    def on_lineEditOutputTopologyPath_textChanged(self, str):
        self.copyIOParametersToDict()

    @pyqtSlot(str)
    def on_lineEditLigandName_textChanged(self, str):
        self.check_selection(self.lineEditLigandName)
        self.copyIOParametersToDict()

    @pyqtSlot(int)
    def on_spinBoxInputDT_valueChanged(self, int):
        self.copyIOParametersToDict()

    @pyqtSlot(str)
    def on_lineEditInputStripping_textChanged(self, str):
        self.check_selection(self.lineEditInputStripping)
        self.copyIOParametersToDict()

    @pyqtSlot(str)
    def on_lineEditOutputStripping_textChanged(self, str):
        self.check_selection(self.lineEditOutputStripping)
        self.copyIOParametersToDict()

    @pyqtSlot(bool)
    def on_checkBoxHasLigand_toggled(self, bool):
        self.copyIOParametersToDict()

    @pyqtSlot(int)
    def on_spinBoxOutDT_valueChanged(self, int):
        self.copyIOParametersToDict()

    @pyqtSlot(int)
    def on_comboBoxOutputFormat_currentIndexChanged(self, int):
        self.copyIOParametersToDict()

        # Change trajectory format
        outputTrajectoryPath = self.lineEditOutputTrajectoryPath.text()
        format = self.comboBoxOutputFormat.currentText()
        if not outputTrajectoryPath == "":
            split = outputTrajectoryPath.split(".")
            if split[-1] != format:
                split[-1] = format
                self.lineEditOutputTrajectoryPath.setText(".".join(split))

    @pyqtSlot(int)
    def on_checkBoxReplicas_toggled(self, int):
        self.copyIOParametersToDict()

    def copyIOParametersToDict(self):
        self.parameters["inputTopologyPath"] = self.lineEditInputTopologyPath.text()
        self.parameters[
            "outputTrajectoryPath"
        ] = self.lineEditOutputTrajectoryPath.text()
        self.parameters["outputTopologyPath"] = self.lineEditOutputTopologyPath.text()
        self.parameters["inputDT"] = self.spinBoxInputDT.value()
        self.parameters["inputStripping"] = self.lineEditInputStripping.text()
        self.parameters["hasLigand"] = self.checkBoxHasLigand.isChecked()
        self.parameters["ligName"] = self.lineEditLigandName.text()
        self.parameters["outputDT"] = self.spinBoxOutDT.value()
        self.parameters["replicas"] = self.checkBoxReplicas.isChecked()
        self.parameters["format"] = (
            self.comboBoxOutputFormat.currentIndex(),
            self.comboBoxOutputFormat.itemText(
                self.comboBoxOutputFormat.currentIndex()
            ),
        )
        self.parameters["numReplica"] = self._numReplica
        inputTrajectories = []
        for i in range(self.listWidgetInputTrajectories.count()):
            inputTrajectories.append(self.listWidgetInputTrajectories.item(i).text())
        self.parameters["inputTrajectoriesPath"] = inputTrajectories

    def copyIOParametersFromDict(self, dictionnary):
        self.lineEditInputTopologyPath.setText(dictionnary["inputTopologyPath"])
        self.lineEditOutputTrajectoryPath.setText(dictionnary["outputTrajectoryPath"])
        self.lineEditOutputTopologyPath.setText(dictionnary["outputTopologyPath"])
        self.spinBoxInputDT.setValue(dictionnary["inputDT"])
        self.lineEditInputStripping.setText(dictionnary["inputStripping"])
        self.checkBoxHasLigand.setChecked(dictionnary["hasLigand"])
        self.lineEditLigandName.setText(dictionnary["ligName"])
        self.spinBoxOutDT.setValue(dictionnary["outputDT"])
        self.comboBoxOutputFormat.setCurrentIndex(dictionnary["format"][0])
        self.checkBoxReplicas.setChecked(dictionnary["replicas"])
        self._numReplica = dictionnary["numReplica"]

        if isinstance(dictionnary["inputTrajectoriesPath"], list):
            self.checkBoxReplicas.setEnabled(True)

        firstItem = self.listWidgetInputTrajectories.item(0)

        if firstItem.text() and firstItem.text() == "Add trajectory":
            self.listWidgetInputTrajectories.takeItem(0)
        self.listWidgetInputTrajectories.addItems(dictionnary["inputTrajectoriesPath"])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.on_toolButtonAddAnalysis_clicked()

        if event.key() == Qt.Key_Delete:
            if self.treeWidgetChoosenAnalysis.hasFocus():
                sip.delete(self.treeWidgetChoosenAnalysis.currentItem())
            elif self.listWidgetInputTrajectories.hasFocus():
                sip.delete(self.listWidgetInputTrajectories.currentItem())

    ###########################################################################
    # INPUT/OUTPUT READING
    @pyqtSlot()
    def on_pushButtonAddTrajectory_released(self):
        (file, filetype) = QFileDialog.getOpenFileNames(
            self,
            "Open Trajectory",
            filter="Valid Formats (*.arc *.dcd *.binpos *.xtc *.trr *.hdf5 *.h5 *.ncdf *.netcdf \
                                    *.nc *.pdb.gz *.pdb *.lh5 *.crd *.mdcrd *.inpcrd  *.restrt *.rst7 *.ncrst *.lammpstrj \
                                    *.dtr *.stk *.gro *.xyz.gz *.xyz *.tng *.xml *.mol2 *.hoomdxml);;",
        )
        if file:
            # If the "example line" is still here, delete it!
            if self.listWidgetInputTrajectories.count() == 1:
                firstItem = self.listWidgetInputTrajectories.item(0)
                if firstItem.text() == "Add trajectory":
                    self.listWidgetInputTrajectories.takeItem(0)

            self.listWidgetInputTrajectories.addItems(file)

        if self.listWidgetInputTrajectories.count() > 1:
            self.checkBoxReplicas.setEnabled(True)

    @pyqtSlot()
    def on_toolButtonInputTopologyButton_clicked(self):
        (file, filetype) = QFileDialog.getOpenFileName(
            self,
            "Open Topology",
            filter="Valid Formats ( *.binpos *.hdf5 *.h5 *.pdb.gz *.pdb *.lh5 *.crd *.mdcrd \
                                     *.inpcrd *.prmtop *.restrt *.rst7 *.gro *.xyz.gz \
                                     *.xyz *.tng *.xml *.mol2 *.hoomdxml);;",
        )
        self.lineEditInputTopologyPath.setText(file)

    @pyqtSlot()
    def on_toolButtonOutputTrajectoryButton_clicked(self):
        (file, filetype) = QFileDialog.getSaveFileName(
            self,
            "Save Trajectory",
            filter="Valid Formats (*.arc *.dcd *.binpos *.xtc *.trr *.hdf5 *.h5 *.ncdf *.netcdf \
                                    *.nc *.pdb.gz *.pdb *.lh5 *.crd *.mdcrd *.inpcrd  *.restrt *.rst7 *.ncrst *.lammpstrj \
                                    *.dtr *.stk *.gro *.xyz.gz *.xyz *.tng *.xml *.mol2 *.hoomdxml);;",
        )
        self.lineEditOutputTrajectoryPath.setText(file)

        # Updating formatComboBox
        trajFormat = file.split(".")[-1]
        comboIndex = self.comboBoxOutputFormat.findText(trajFormat)
        if comboIndex == -1:
            self.comboBoxOutputFormat.setCurrentIndex(0)  # Default is amber format
        else:
            self.comboBoxOutputFormat.setCurrentIndex(comboIndex)

    @pyqtSlot()
    def on_toolButtonOutputFiguresButton_clicked(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "OutputFigureFolder",
        )

        self.lineEditOutputFiguresPath.setText(folder)

        # Updating formatComboBox

    @pyqtSlot()
    def on_toolButtonOutputTopologyButton_clicked(self):
        (file, filetype) = QFileDialog.getSaveFileName(
            self, "Save Topology", filter="PDB (*.pdb);;"
        )
        # filter="All (*.*);;")
        split = os.path.splitext(file)
        if split[-1] != "pdb":
            file = split[0] + ".pdb"
        self.lineEditOutputTopologyPath.setText(file)

    def init_graphicsViewLayout_2(self):
        """
        tab
         | layout
         | tabWidgetResults (tabWidget)
         |   | graphicsViewWidget (tab)
         |   |   | layout
        """
        # For each "replica" (if single traj : only one).
        for i in range(self._numReplica):
            # Define tab name
            if self._numReplica < 2:
                tabName = "Resuts"
            else:
                tabName = f"Replica {i + 1}"

            # Create a new tab
            tab = QtWidgets.QWidget()
            tab.setObjectName(tabName)
            # And add it to the main tab window
            # Apply a grid layout for full screen compatibility
            layout = QtWidgets.QGridLayout(tab)
            layout.setContentsMargins(0, 0, 0, 0)

            # Add a tabWidget inside (because some analyses have several graphs)
            tabWidgetResults = QtWidgets.QTabWidget(tab)
            tabWidgetResults.setObjectName("graphicsTabWidget")
            tabWidgetResults.replica = tabName
            tabWidgetResults.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            tabWidgetResults.setTabBarAutoHide(True)
            layout.addWidget(tabWidgetResults, 1, 0, 1, 1)
            # tabWidgetResults.setCurrentIndex(-1)

            self.tabResults.append(tab)
            # Add the new tab in the mothertab
            self.tabWidgetParametersResults.addTab(tab, tabName)

    # def init_graphicsViewLayoutParent(self, parent):
    #     graphicsViewWidget = QtWidgets.QWidget()
    #     #THIBAULT : CONTINUE HERE
    #     self.graphicsViewLayout = QtWidgets.QVBoxLayout(self.tabWidgetResults)
    #     parent.addTab(graphicsViewWidget,"")
    #     graphicsViewLayout = QtWidgets.QVBoxLayout(parent)
    #     graphicsViewLayout.setContentsMargins(0, 0, 0, 0)

    def remove_content(self, ressource):
        for i in range(len(ressource.children())):  # for content in gridLayout
            try:
                ressource.children()[i].hide()
            except Exception:
                pass

    def clean_parameters(self):
        # TODO: remove grid ?
        # grid = self.gridLayoutParameters
        # grid.itemAt(0).hide()
        for i in range(len(self.tabParameters.children())):
            try:
                self.tabParameters.children()[i].hide()
            except Exception:
                pass

    ###########################################################################
    # UNSORTED FUNCTIONS
    @pyqtSlot()
    def on_toolButtonReset_clicked(self):
        QMessageBox.warning(self, "Error", "Function not implemented yet")

    def add_image(self):
        imagepath = "/mod_users/tta_sur/PROJETS/NCK1/modelling/simulations/NCK2/holo/scr/amber/replica_1/analysesMD/img/call_1/RMSD-on-pocketP1_Global.png"
        img = QPixmap.fromImage(QImage(imagepath))
        img = img.scaled(
            self.graphicsViewResults.width(),
            self.graphicsViewResults.height(),
            Qt.KeepAspectRatio,
            Qt.FastTransformation,
        )
        scene = QGraphicsScene(self)
        scene.addPixmap(img)
        self.graphicsViewResults.setScene(scene)
        print(dir(self.graphicsViewResults))

    @pyqtSlot()
    def on_toolButtonRemoveAnalysis_clicked(self):
        sip.delete(self.treeWidgetChoosenAnalysis.currentItem())

    def add_analysis_on_TreeWidget(self):
        # 1. Top menus
        fluctuationTreeMenu = QtWidgets.QTreeWidgetItem(
            self.treeWidgetAnalysisAvailable
        )
        distancesTreeMenu = QtWidgets.QTreeWidgetItem(self.treeWidgetAnalysisAvailable)
        toolsTreeMenu = QtWidgets.QTreeWidgetItem(self.treeWidgetAnalysisAvailable)
        anglesTreeMenu = QtWidgets.QTreeWidgetItem(self.treeWidgetAnalysisAvailable)
        conservationTreeMenu = QtWidgets.QTreeWidgetItem(
            self.treeWidgetAnalysisAvailable
        )
        geometryTreeMenu = QtWidgets.QTreeWidgetItem(self.treeWidgetAnalysisAvailable)

        distancesTreeMenu.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        fluctuationTreeMenu.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        toolsTreeMenu.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        anglesTreeMenu.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        conservationTreeMenu.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        geometryTreeMenu.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

        fluctuationTreeMenu.setText(0, "Fluctuations")
        distancesTreeMenu.setText(0, "Distances")
        toolsTreeMenu.setText(0, "Tools")
        anglesTreeMenu.setText(0, "Angles")
        conservationTreeMenu.setText(0, "Conservation")
        geometryTreeMenu.setText(0, "Geometry")

        # 2. Add Top menus on treeWidgets
        # rmsd = anlz.RMSD.RMSD(fluctuationTreeMenu, self)
        # rmsf = anlz.RMSF.RMSF(fluctuationTreeMenu, self)
        # sasa = anlz.Surface.Surface(fluctuationTreeMenu, self)
        # distance = anlz.Distances.Distances(distancesTreeMenu, self)
        # angle = anlz.Angles.Angles(anglesTreeMenu, self)
        # Dihedrals = anlz.Dihedrals.Dihedrals(anglesTreeMenu, self)
        # Contacts = anlz.Contacts.Contacts(distancesTreeMenu, self)
        # iac = anlz.IAC.IAC(toolsTreeMenu, self)
        # hbond = anlz.HBonds.HBonds(conservationTreeMenu, self)
        # alignement = anlz.Alignement.Alignement(toolsTreeMenu, self)
        # ss = anlz.SecondaryStructures.SecondaryStructures(conservationTreeMenu, self)
        # protrusion = anlz.Protrusions.Protrusions(geometryTreeMenu, self)

    ###########################################################################
    # CHECKIN FUNCTIONS

    @pyqtSlot()
    def on_treeWidgetAnalysisAvailable_itemSelectionChanged(self):
        print("Action on itemTreeWidget")
        item = self.treeWidgetAnalysisAvailable.currentItem()
        print(type(item))

        # This is important...  Menus (with an arrow) are PyQt5.QtWidgets.QTreeWidgetItem but
        # Analysis tools are "analysis.X.X". This is to differentiate categories objects and REAL analysis items.
        # If it is a REAL analysis items, It will update the views.
        if "analysis" not in str(type(item)):
            print("no action...leaving")
            return  # Leave the function

        self.remove_content(self.tabParameters)

        item.update_parent(self.tabParameters)

    def clean_graphicsView(self):
        for i in reversed(range(self.graphicsViewLayout.count())):
            self.graphicsViewLayout.itemAt(i).widget().deleteLater()

        # Clean tabs
        for i in reversed(range(self.tabWidgetResults.count())):
            self.tabWidgetResults.removeTab(i)

        # We removed all tabs. So now we have to create an empty one again.
        self.init_graphicsViewLayout()

    def clean_graphicsView_2(self):

        # delete old tabs.
        for tab in self.tabResults:
            tab.deleteLater()
        # Reset the list
        self.tabResults = []

        numTabs = self.tabWidgetParametersResults.count()
        for i in range(numTabs - 1, 0, -1):
            self.tabWidgetParametersResults.removeTab(i)

        # We removed all tabs. So now we have to create an empty one again.
        self.init_graphicsViewLayout_2()

    def init_tabResultsReplica(self, numberOfReplicas):
        # Todo : improve memory by avoiding creating again again tabs...
        self.tabsResults = []
        for i in numberOfReplicas:
            # Create main tab
            tabResult = QtWidgets.QWidget()
            tabResult.setObjectName(f"tabResultReplica{i}")

            # Create layout.
            gridLayout = QtWidgets.QGridLayout(tabResult)
            gridLayout.setContentsMargins(0, 0, 0, 0)
            gridLayout.addWidget(self.tabWidgetResults, 1, 0, 1, 1)

            tabWidgetResults = QtWidgets.QTabWidget(tabResult)
            tabWidgetResults.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            tabWidgetResults.setTabBarAutoHide(True)
            tabWidgetResults.setObjectName(f"tabWidgetResultsReplica{i}")
            gridLayout.addWidget(tabWidgetResults, 1, 0, 1, 1)
            tabWidgetResults.setCurrentIndex(-1)

            self.tabWidgetParametersResults.addTab(tabResult, f"replica{i}")
            self.tabsResults.append(tabResult)
            # createTab

    @pyqtSlot()
    def on_treeWidgetChoosenAnalysis_itemSelectionChanged(self):
        item = self.treeWidgetChoosenAnalysis.currentItem()
        tabPosition = self.tabWidgetParametersResults.currentIndex()

        # If no item was selectionned, leave
        if item is None:
            item = self.treeWidgetChoosenAnalysis.setCurrentItem(
                self.treeWidgetChoosenAnalysis.topLevelItem(0)
            )
            # If there is no item selected, leave.
            if item is None:
                return

        if "analysis" not in str(type(item)):
            return  # Leave the function

        # Clean tabparameter content and replace it with new selected one.
        self.remove_content(self.tabParameters)
        item.update_parent(self.tabParameters)

        # If we have results
        if self.is_runOK:
            # Remove old tabs
            self.clean_graphicsView_2()

            for i in range(self._numReplica):
                # Reset view
                """
                tab
                 | layout
                 | tabWidgetResults (tabWidget)
                 |   | graphicsViewWidget (tab)
                 |   |   | layout
                """

                # Get sub tabWidgets to put graph in.
                subtab = self.tabResults[i].findChild(
                    QtWidgets.QTabWidget, "graphicsTabWidget"
                )

                if self.checkBoxReplicas.isChecked():
                    item.show_graph(subtab, i)
                else:
                    item.show_graph(subtab)

        # restore current tab position
        self.tabWidgetParametersResults.setCurrentIndex(tabPosition)

    @pyqtSlot()
    def on_toolButtonAddAnalysis_clicked(self):
        if self.treeWidgetAnalysisAvailable.hasFocus():
            item = self.treeWidgetAnalysisAvailable.currentItem()
            if not item:
                return None
            try:
                # TODO: newitem not used
                # newitem = item.__class__(
                #     self.treeWidgetChoosenAnalysis, self
                # )  #
                item.__class__(
                    self.treeWidgetChoosenAnalysis, self
                )  # Duplication of this item
                self.is_runOK = False  # Reset run status.
            except Exception:
                pass

    def check_fill(self):
        """
        Check if every field used for analysis parametrization was filled.

        """
        # Check trajectories
        for i in range(self.listWidgetInputTrajectories.count()):
            if self.listWidgetInputTrajectories.item(i) in ["", "Add trajectory"]:
                QMessageBox.warning(self, "Error", "Missing Input Trajectory")
                return False
        if self.listWidgetInputTrajectories.count() == 0:
            QMessageBox.warning(self, "Error", "Missing Input Trajectory")
            return False

        if self.lineEditInputTopologyPath.text() == "":
            QMessageBox.warning(self, "Error", "Missing Input Topology")
            return False

        if self.checkBoxHasLigand.isChecked():
            if self.lineEditLigandName.text() == "":
                QMessageBox.warning(self, "Error", "Missing Ligand Name")
                return False

        if not self.selectionOK:
            QMessageBox.warning(
                self,
                "Error",
                "An atom selection is not OK. Please search for a red box and correct it",
            )
            return False

        return True  # Return True means that everything is ok for the next step

    def check_files_ok(self):
        """
        Check if files exist or directory exist
        """
        for i in range(self.listWidgetInputTrajectories.count()):
            path_ = self.listWidgetInputTrajectories.item(i).text()
            if not os.path.exists(path_):
                QMessageBox.warning(self, "Error", f"{path_} does not exist")
                return False

        if not os.path.exists(self.lineEditInputTopologyPath.text()):
            QMessageBox.warning(self, "Error", "Input Topology file not exists")
            return False

        if not self.lineEditOutputTrajectoryPath.text() == "":
            if not os.access(
                os.path.dirname(self.lineEditOutputTrajectoryPath.text()), os.W_OK
            ):
                QMessageBox.warning(
                    self, "Error", "I do not have write acces for Output Trajectory"
                )
                return False
            self.saveOutput = True

        if not self.lineEditOutputTopologyPath.text() == "":
            if not os.access(
                os.path.dirname(self.lineEditOutputTopologyPath.text()), os.W_OK
            ):
                QMessageBox.warning(
                    self, "Error", "I do not have write access for Output Topology "
                )
                return False

        return True  # Return True means that everything is ok for the next step

    @pyqtSlot()
    def on_pushButtonRun_clicked(self):
        # This is only for testing for now...
        if not self.check_fill():  # Check if everything was filed
            return
        if (
            not self.check_files_ok()
        ):  # CHeck if files exist and that we have write access
            return

        shouldIStart = True
        root = self.treeWidgetChoosenAnalysis.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            # Retrieve parameters
            item.retrieve_parameters()

            if not item.check_all_argument():
                shouldIStart = False
                QMessageBox.warning(self, "Error", f"A field is missing in {item.name}")
                break

        if shouldIStart:
            self.create_output_dirs()

            # Start Analysis
            self.start_Analysis()

    def create_output_dirs(self):
        print("creating output directories")

        if self.lineEditOutputFiguresPath.text() == "":
            topol_location = os.path.realpath(self.lineEditInputTopologyPath.text())
            folder_name = ".".join(
                os.path.basename(os.path.realpath(topol_location)).split(".")[:-1]
            )
            folder_location = os.path.dirname(topol_location)
            output_folder = folder_location + "/" + folder_name
        else:
            output_folder = self.lineEditOutputFiguresPath.text()

        self.output_folder = output_folder

        if self.checkBoxReplicas.isChecked():
            numReplica = self.listWidgetInputTrajectories.count()
        else:
            numReplica = 1

        if numReplica > 1:
            for i in range(numReplica):
                os.makedirs(output_folder + "/replica{}/CSV/".format(i), exist_ok=True)
                os.makedirs(output_folder + "/replica{}/IMG/".format(i), exist_ok=True)
        else:
            os.makedirs(output_folder + "/CSV/", exist_ok=True)
            os.makedirs(output_folder + "/IMG/", exist_ok=True)

    def get_numberOfChild_QTreeWidget(self, item, count=0):
        if item:
            for i in range(item.childCount()):
                child = item.child(i)
                if "analysis" in str(child.__class__):
                    count += 1
                count = self.get_numberOfChild_QTreeWidget(child, count)
            return count
        else:
            return 0

    def do_item_analysis(self, root, traj, replica=0):
        childCount = self.get_numberOfChild_QTreeWidget(root)

        for i in range(childCount):
            self.update()  # refresh the window.
            item = root.child(i)

            # some analyses like "ligand" have sub items. This is to run all analyses of all "child"
            traj = self.do_item_analysis(item, traj, replica)

            if "analysis" not in str(item.__class__):
                continue

            # Ignore if item is not a "analyses"
            if (item.__class__.__name__ == "HBonds") and ONTESTING is True:
                traj2 = md.load_pdb("2eqq.pdb")
                item.do_analysis(traj2)
            else:
                traj = item.do_analysis(traj, replica, self._numReplica)
                # traj = item.do_analysis(traj, replica) #TTA : backup
            self.numberOfAnalysisDone += 1
            progression = (
                (self.numberOfAnalysisDone)
                / (self.numberOfAnalysis * self._numReplica)
                * 100
            )
            self.progressBarAnalyses.setValue(progression)

        self.saveTrajectory(traj)
        return traj

    def returnAtomsIndexToRemove(self):

        removeIndexes = []
        hasAtomToRemove = False
        try:
            firstFrame = md.load_frame(
                self.listWidgetInputTrajectories.item(0).text(),
                self.lineEditInputTopologyPath.text(),
                index=0,
            )
        except Exception:
            return False

        if self.checkBoxRemoveWater.isChecked():
            hasAtomToRemove = True
            removeIndexes.append(firstFrame.top.select("not water"))

        if self.lineEditInputStripping.text() != "":
            hasAtomToRemove = True
            removeIndexes.append(
                firstFrame.top.select(f"not {self.lineEditInputStripping.text()}")
            )

        if hasAtomToRemove:
            return np.concatenate(removeIndexes)
        else:
            return None

    def read_single_traj(self, path):
        atomsToRemove = self.returnAtomsIndexToRemove()

        if atomsToRemove not in [None, False]:
            traj = md.load(
                path,
                top=self.lineEditInputTopologyPath.text(),
                stride=self.spinBoxInputDT.value(),
                atom_indices=atomsToRemove,
            )

        else:
            traj = md.load(
                path,
                top=self.lineEditInputTopologyPath.text(),
                stride=self.spinBoxInputDT.value(),
            )
        return traj

    def read_single_traj_from_listWidget(self, index=0, frame=None):
        atomsToRemove = self.returnAtomsIndexToRemove()

        if atomsToRemove not in [None, False]:
            traj = md.load(
                self.listWidgetInputTrajectories.item(index).text(),
                top=self.lineEditInputTopologyPath.text(),
                stride=self.spinBoxInputDT.value(),
                atom_indices=atomsToRemove,
                frame=frame,
            )

        else:
            traj = md.load(
                self.listWidgetInputTrajectories.item(index).text(),
                top=self.lineEditInputTopologyPath.text(),
                stride=self.spinBoxInputDT.value(),
                frame=frame,
            )
        return traj

    def read_and_return_traj(self):

        count = self.listWidgetInputTrajectories.count()
        if count > 1:
            trajs = []
            for i in range(count):
                trajs.append(self.read_single_traj_from_listWidget(i))
            if self.checkBoxReplicas.isChecked():
                return trajs
            else:
                traj = md.join(trajs)
                del trajs
                # Rework timestep
                try:
                    traj.time = np.arange(
                        traj.time[0], len(traj) * traj.timestep, traj.timestep
                    )
                except Exception:
                    traj.time = np.arange(0, len(traj), 1)
                    traj.timestep = 1
                return traj
        else:
            traj = self.read_single_traj_from_listWidget(0)

        # Last verification on trajectory timescale
        if traj.timestep == 0:
            traj.time = np.arange(0, len(traj), 1)
            traj.timestep = 1

        return traj

    def start_Analysis(self):

        self.statusbar.showMessage("Reading Trajectory")

        traj = self.read_and_return_traj()

        if self.checkBoxHasLigand.isChecked():
            self.statusbar.showMessage("Ligand mode activated! adding ligand analysis")
            self.addLigandAnalysis()

        self.statusbar.showMessage("Doing Analysis")
        # List all analysis

        # Loop on choosen analysis items
        root = self.treeWidgetChoosenAnalysis.invisibleRootItem()
        self.numberOfAnalysis = self.get_numberOfChild_QTreeWidget(root)
        self.numberOfAnalysisDone = 0

        if self.checkBoxReplicas.isChecked():
            self._numReplica = len(traj)
            for replica, t in enumerate(traj):
                self.do_item_analysis(root, t, replica)
        else:
            self._numReplica = 1
            self.do_item_analysis(root, traj)

        self.is_runOK = True

        # Instantiate graph tabs.
        self.init_graphicsViewLayout_2()

        # Show current item graph
        self.on_treeWidgetChoosenAnalysis_itemSelectionChanged()
        self.statusbar.showMessage(
            "Done! Click on an analysis to see results or check IMG folder."
        )

    def saveTrajectory(self, traj):
        """
        Save trajectory if output trajectory field are not empty
        :param traj: trajectory
        :return:
        """
        if self.saveOutput:
            trajout = self.lineEditOutputTrajectoryPath.text()
            topolOut = self.lineEditOutputTopologyPath.text()
            timestep = self.spinBoxOutDT.value()
            if timestep > 1:
                traj = traj[::timestep]

            if self.lineEditOutputStripping.text() != "":
                selection = "not " + self.lineEditOutputStripping.text()
                traj = traj.atom_slice(traj.top.select(selection))

            traj.save(trajout)

            # Now topology (if asked)
            if topolOut != "":
                traj[0].save(topolOut)
            self.statusbar.showMessage("Just saved a new trajectory")

    def check_selection(self, lineEditSelection):
        selection = lineEditSelection.text()

        if self.trajSelectionTest is None:
            try:
                trajPath = self.listWidgetInputTrajectories.item(0).text()
            except Exception:
                return
            topPath = self.lineEditInputTopologyPath.text()
            # if the path is not empty and not the example line in Qlistwidget.
            if trajPath not in ["", "Add trajectory"] and not topPath == "":
                if self.check_files_ok():
                    frame0 = self.read_single_traj_from_listWidget(0, 0)
                    self.setTrajSelectionTest(frame0)
            else:
                return

        try:

            sel = self.trajSelectionTest.top.select(selection)
            if len(sel) > 0:
                lineEditSelection.setStyleSheet("border: 2px solid green;")
                self.statusbar.showMessage("Selection OK")
                self.selectionOK = True
            else:
                lineEditSelection.setStyleSheet("border: 2px solid red;")
                self.statusbar.showMessage("ERROR : There is no atom selected")
                self.selectionOK = False
        except Exception:
            if selection == "":
                lineEditSelection.setStyleSheet("")
                self.selectionOK = True
            else:
                lineEditSelection.setStyleSheet("border: 2px solid red;")
                self.statusbar.showMessage("ERROR : no atom selected")
                self.selectionOK = False

    def addLigandAnalysis(self):
        #        HBONDS LIG-POCKET
        ligandName = self.lineEditLigandName.text()

        self.LigandsTreeList = QtWidgets.QTreeWidgetItem(self.treeWidgetChoosenAnalysis)
        self.LigandsTreeList.setText(0, "LIGAND")

        # Align on protein
        align1 = anlz.Alignement.Alignement().__class__(self.LigandsTreeList, self)
        align1.lineEditSelection.setText("protein")
        align1.retrieve_parameters()

        # RMSD on ligand aligned on protein
        rmsdLigOnProt = anlz.RMSD.RMSD().__class__(
            self.LigandsTreeList, self
        )  # Duplication of this item
        rmsdLigOnProt.lineEditName.setText("LIGAND - ref is prot")
        rmsdLigOnProt.lineEditSelection.setText(ligandName)
        rmsdLigOnProt.retrieve_parameters()

        # Align on ligand
        align2 = anlz.Alignement.Alignement().__class__(self.LigandsTreeList, self)
        align2.lineEditSelection.setText(ligandName)
        align2.retrieve_parameters()

        # RMSD ON LIGAND aligned on LIGAND
        rmsdLigOnProt = anlz.RMSD.RMSD().__class__(
            self.LigandsTreeList, self
        )  # Duplication of this item
        rmsdLigOnProt.lineEditName.setText("LIGAND - ref is ligand")
        rmsdLigOnProt.lineEditSelection.setText(ligandName)
        rmsdLigOnProt.retrieve_parameters()

        # RMSF on LIGAND
        rmsfLigand = anlz.RMSF.RMSF().__class__(
            self.LigandsTreeList, self
        )  # Duplication of this item
        rmsfLigand.lineEditName.setText("LIGAND")
        rmsfLigand.lineEditSelection.setText(ligandName)
        rmsfLigand.checkBoxByResidue.setChecked(False)
        rmsfLigand.retrieve_parameters()

        # RMSF on pocket
        rmsfPocket = anlz.RMSF.RMSF().__class__(
            self.LigandsTreeList, self
        )  # Duplication of this item
        rmsfPocket.lineEditName.setText("LIGAND - Pocket")
        rmsfPocket.lineEditSelection.setText(f"within 4 of {ligandName}")
        rmsfPocket.checkBoxByResidue.setChecked(True)
        rmsfPocket.retrieve_parameters()

        # SASA on Pockets residue
        SASAPocket = anlz.Surface.Surface().__class__(
            self.LigandsTreeList, self
        )  # Duplication of this item
        SASAPocket.lineEditName.setText("LIGAND - Pocket")
        SASAPocket.lineEditSelection.setText(f"within 4 of {ligandName}")
        SASAPocket.comboBoxMode.setCurrentIndex(1)  # Per residue
        SASAPocket.spinBoxPoints.setValue(400)
        SASAPocket.retrieve_parameters()

        # HBONDS
        Hbonds = anlz.HBonds.HBonds().__class__(
            self.LigandsTreeList, self
        )  # Duplication of this item
        Hbonds.lineEditName.setText("LIGAND -- pocket")
        Hbonds.lineEditSelection1.setText("protein")
        Hbonds.lineEditSelection2.setText(f"{ligandName}")
        Hbonds.retrieve_parameters()
