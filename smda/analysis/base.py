#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#TODO : save only fig ?
#TODO : update hbond graph when changing cutoff values
#TODO : check if angle is OK.
#TODO : Hbonds, use the selection....
#TODO : analyse
#       - RG
#       - RDF
#       - salt bridges
#       - cation-pi
import io
import os
import pickle
import scipy.signal
import PyQt5.QtWidgets as QtWidgets
import matplotlib

# matplotlib.use('QT5Agg')
# import matplotlib.pylab as plt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import colors

plt.switch_backend("Agg")
import mdtraj as md
import numpy as np
import pandas as pd
import re

import json
import scipy.interpolate as interpolate
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from collections import defaultdict
plt.style.use('ggplot')


# plt.rcParams["figure.dpi"] = 300
# from main_window_analyseMD import Main_window_analyseMD


class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to insert pandas dataframe in pyqt widget
    From
    https://stackoverflow.com/questions/44603119/how-to-display-a-pandas-data-frame-with-pyqt5
    """

    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()
        try: #df.ix was removed in pandas 1.0.0
            return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))
        except:
            return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending=order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


class Analyses(QtWidgets.QTreeWidgetItem):
    signal = pyqtSignal()

    def __init__(self, analyseName="AnalyseName", parent=None, mainWindows=None, numReplica=1):
        super(QtWidgets.QTreeWidgetItem, self).__init__(parent)
        # super(Analyses,self).__init__()
        self.name = analyseName
        self.setText(0, analyseName)
        self.init_widget()
        self.arguments = []
        ##self.fig = None
        ##self.ax = None
        self.parameters = {"class": self.__class__.__name__}
        self.mainWindows = mainWindows
        self.figures = []
        self.numReplica = numReplica


        # self.lineEditName.textChanged.connect(self.on_lineEditName_textChanged)

    def saveInFile(self, fileObject):
        fileObject.write(json.dumps(self.parameters))

    def init_widget(self):
        self.widget = QtWidgets.QWidget()  # Main Widget
        self.widget.setObjectName("widget")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)

        # WidgetDefinition
        self.textBrowserDescription = QtWidgets.QTextBrowser(self.widget)
        self.textBrowserDescription.setObjectName("textBrowserDescription")

        self.labelName = QtWidgets.QLabel(self.widget)
        self.labelName.setText("Analysis Name")
        self.lineEditName = QtWidgets.QLineEdit(self.widget)
        self.lineEditName.setObjectName("lineEditName")

        self.Hlayout0 = QtWidgets.QHBoxLayout()
        self.Hlayout0.addWidget(self.textBrowserDescription)

        self.Hlayout1 = QtWidgets.QHBoxLayout()
        self.Hlayout1.addWidget(self.labelName)
        self.Hlayout1.addWidget(self.lineEditName)

        self.gridLayout.addLayout(self.Hlayout0, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout1, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2)
        # Now fill HTML Description
        self.textBrowserDescription.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600; text-decoration: underline;\">This analyse was not configured yet</span></p>\n"
        )

    def update_parent(self, parent):
        self.widget.setParent(parent)
        self.widget.show()

    def get_name(self):
        return self.name

    def get_parameters(self):
        return self.parameters

    def do_analysis(self, traj, replica=0, numReplica=1):
        self.mainWindows.statusbar.showMessage("Calculating {} - {}".format(self.__class__.__name__,
                                                                            self.parameters["name"]))
        # 1 Get parameters
        self.retrieve_parameters(numReplica)
        self.add_outPath_in_parameters(numReplica)

        resultsDF = self.do_calculations(traj)

        #If there is no results (or fails) resultsDF = None. To ignore None object I use try
        # try:
        if not resultsDF is None:
            if not resultsDF.empty:
                resultsDF.to_csv(self.parameters["csvPath"][replica], sep=";", index=True)
                self.generate_graphs(resultsDF, replica)
        # except (ValueError,AttributeError):
        else:
            return traj
    
        return traj

    def generate_graphs(self, resultsDF, replica=0):
        """
        Default function to generate XY graphs (most of graph types)
        :param resultsDF: Pandas DataFrame
        :return:
        """
        ax, fig = self.graph_XY(resultsDF,
                                self.__class__.__name__,
                                self.parameters["name"],
                                self.parameters["imgPath"][replica])
        
        self.figures.append([self.store_figure(ax=ax,fig=fig)]) #In a list because we will iterate over figures

    def graph_XY(self, results, aType, name, imgPath):
        aType = self.__class__.__name__
        X = self.xAxisLabel
        Y = self.yAxisLabel
        col = self.lineColor

        if "Average" in results.columns:
            if len(results[X]) > 100:  # For big dataset, average the graph
                ax1 = results.plot(x=X, y=Y, legend=False, title="{} for {}".format(aType, name),
                                   figsize=(7, 4), color="gray")
                ax1.set(ylabel=Y)

                ax = results.plot(x=X, y="Average", ax=ax1, legend=False, color=col)
                ax.set_xlabel(X)
                fig = ax.get_figure()
            else:
                ax = results.plot(x=X, y=Y, legend=False, title="{} for {}".format(aType, name),
                                  figsize=(7, 4), color=col)
                ax.set(ylabel=Y)
                fig = ax.get_figure()
        else:
            ax = results.plot(x=X, y=Y, legend=False, title="{} for {}".format(aType, name),
                              figsize=(7, 4), color=col)
            ax.set(ylabel=Y)
            fig = ax.get_figure()

        plt.savefig(imgPath, dpi=300)
        return (ax, fig)

    def improvedSelection(self, traj, selection):
        if "within" in selection.lower():
            sepRegex = r"(and|or)"
            separator = re.findall(sepRegex, selection)
            split = re.split(sepRegex, selection)
            topology = traj[0].topology
            selectionString = "[atom.index for atom in topology.atoms if ("
            for sel in split:
                if sel not in ["or", "and", "OR", "AND", "&&", "||"]:
                    if "within" in sel.lower():
                        withinRegex = re.search(r"within (\d.?\d*) of (.+)", sel)
                        # Distance unit are in nm.
                        # So convert A to NM.
                        cutoff = float(withinRegex.group(1)) / 10
                        withinOf = withinRegex.group(2)
                        withinIndex = md.compute_neighbors(traj[0],
                                                           cutoff=cutoff,
                                                           query_indices=traj[0].top.select(withinOf))[0]
                        closeIndexes = "("
                        closeIndexes += ' or '.join([f"(atom.index == {index})" for index in withinIndex])
                        closeIndexes += ")"
                        selectionString += closeIndexes

                    else:
                        match = re.search(r"(\(.+\))", traj[0].top.select_expression(sel))
                        if match:
                            selectionString += match.group(1)
                        else:
                            match = re.search(r"atom\.index for atom in topology\.atoms if (.*)]$",
                                              traj[0].top.select_expression(sel))
                            selectionString += match.group(1)

                else:
                    selectionString += f" {sel} "
            selectionString += ')]'

            selectedAtoms = eval(selectionString)
        else:
            selectedAtoms = traj.top.select(selection)

        return selectedAtoms


    def show_graph(self, tab, replica=0):
        # Adjust borders
        if len(self.figures) == 0:
            return
        #reset graphs
        plt.close()

        CurrentFigAx = self.figures[replica]
        from matplotlib.figure import Figure

        for i in range(len(CurrentFigAx)):
            graphicsViewWidget = QtWidgets.QWidget()
            tab.addTab(graphicsViewWidget, f"results {i}")
            layout = QtWidgets.QVBoxLayout(graphicsViewWidget)
            layout.setContentsMargins(0, 0, 0, 0)


            fig = CurrentFigAx[i][0]
            # fig=Figure()
            # CurrentFigAx[i][1].mouse_init()
            fig.subplots_adjust(bottom=0.140)
            # axes = fig.add_subplot(111, projection='3d')

            self.plotWidget = FigureCanvas(fig)
            self.plotWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)





            layout.addWidget(self.plotWidget)


            # add toolbar
            layout.addWidget(NavigationToolbar(self.plotWidget, graphicsViewWidget))


    def graph_HBOND(self, data, name, imgPath):
        """
        Data Has to be a dataframe
        """
        #RESET HBONDS GRAPH
        #self.figures = []
        plt.clf()
        plt.style.use('seaborn-white')
        data.sort_values("Freq", inplace=True, ascending=False)

        cutoff = self.spinBoxFreq.value() #self.parameters["freq"]
        filteredData = data.query("Freq > @cutoff")

        indexes = list(filteredData.index)
        # Add percentage

        percentage = np.array(filteredData["Freq"].values * 100)

        labels = []
        for i in range(len(indexes)):
            index = indexes[i]
            percent = percentage[i]
            labels.append("{} | {:3.1f}%".format(indexes[i], percentage[i]))

        values = filteredData.drop("Freq", axis=1).to_numpy()

        fig, ax = plt.subplots()

        ax.set_xlabel(self.xAxisLabel)
        ax.set_ylabel("")
        ax.set_title(f"{self.__class__.__name__} for {name}")
        ax.set_yticks(list(range(len(labels))))
        ax.set_yticklabels(labels)

        plt.imshow(values, cmap="gray_r", aspect="auto", interpolation='None')

        fig.tight_layout()

        # Copy figure to avoid overlap
        #elf.store_figure(ax, fig)

        plt.savefig(imgPath, dpi=300)
        plt.style.use('ggplot')  # Restore previous style
        return (ax,fig)


    def graph_SS(self, dss, name, imgPath):
        """

        """
        plt.clf()
        plt.style.use('seaborn-white')

        conversionDict = {"H": 0, "E": 1, "C": 2, "": 3, "B": 4, "G": 5, "I": 6, "T": 7, "S": 8, ' ': 3}

        colorDict = {0: "red", 1: "yellow", 2: "white", 3: "white", 4: "orange", 5: "magenta", 6: "pink", 7: "cyan",
                     8: "green", }

        labelDict = {0: "Helix", 1: "Sheet", 2: "Coil", 3: "Loop", 4: "Beta-Bridge", 5: "3/10 helix", 6: "pi helix",
                     7: "Turn", 8: "Bend", }

        for key in conversionDict.keys():
            dss[dss == key] = conversionDict[key]
        dss = dss.astype(int)

        # Define matplotlib colors
        col = ['r', '#FFFF00', 'w', '#DCDCDC', '#FFA500', 'm', '#FFC0CB', 'c', 'b']
        cmap = colors.ListedColormap(col)
        boundaries = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        norm = colors.BoundaryNorm(boundaries, cmap.N, clip=True)
        patches = [mpatches.Patch(color=col[i], label=labelDict[i]) for i in range(len(labelDict.values()))]

        fig, ax = plt.subplots()

        ax.set_xlabel("Frame")
        ax.set_ylabel("Residue")
        ax.set_title("Secondary Structure Conservation for {}".format(name))

        plt.imshow(dss, cmap=cmap, norm=norm, aspect="auto", interpolation="None")
        plt.legend(handles=patches, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5)

        # fig.tight_layout()

        # Copy figure to avoid overlap

        plt.savefig(imgPath, dpi=300)
        plt.style.use('ggplot')  # Restore previous style
        return (ax,fig)

    def store_figure(self, ax, fig):
        """
        Store matplotlib Axes and Figure to be redraw after.
        :param ax: Matplotlib Axes
        :param fig: Matplotlib Figure
        :return:
        """
        bufAx = io.BytesIO()
        bufFig = io.BytesIO()
        pickle.dump(fig, bufFig)
        pickle.dump(ax, bufAx)
        bufAx.seek(0)
        bufFig.seek(0)
        pickleFig = pickle.load(bufFig)
        pickleAx = pickle.load(bufAx)

        return [pickleFig, pickleAx]

    def check_all_argument(self):
        for argument in self.arguments:
            if not argument in self.parameters:
                print(self.parameters)
                print(argument)
                print("false arguement")
                return False
            else:
                if self.parameters[argument] == "":
                    print(self.parameters)
                    print("void argument")
                    return False
        return True

    # @pyqtSlot()
    def on_lineEditName_textChanged(self):
        name = self.__class__.__name__
        name = "{} - {}".format(name, self.lineEditName.text())
        self.setText(0, name)

    # def update_path_and_create_dir_for_replica(self, replica):
    #     if replica == None:
    #         return
    #
    #     # recalculating path for csv and img
    #     path = self.parameters["csvPath"].split("/")
    #
    #     path[-1] = f"replica{replica}/" + path[-1]
    #     if not os.path.exists(f"CSV/replica{replica}"):
    #         os.mkdir(f"CSV/replica{replica}")
    #     self.parameters["csvPath"] = '/'.join(path)
    #
    #
    #
    #     if not os.path.exists(f"IMG/replica{replica}"):
    #                 os.mkdir(f"IMG/replica{replica}")
    #
    #     imgPaths = self.parameters["imgPath"]
    #     if type(imgPaths) == type([]):
    #         for i in range(len(imgPaths)):
    #             path = imgPaths[i].split("/")
    #             path[-1] = f"replica{replica}/" + path[-1]
    #             self.parameters["imgPath"][i] = '/'.join(path)
    #
    #     else:
    #         path = imgPaths.split("/")
    #         path[-1] = f"replica{replica}/" + path[-1]
    #         self.parameters["imgPath"] = '/'.join(path)

    def restore_graphs(self):
        for replica, path in enumerate(self.parameters["csvPath"]):
            if os.path.exists(path):
                resultsDF = pd.read_csv(path, sep=";")
                self.generate_graphs(resultsDF, replica)

    def add_outPath_in_parameters(self, numReplica=None):

        #Reset path in list.
        self.parameters["imgPath"] = []
        self.parameters["csvPath"] = []

        if numReplica and numReplica > 1:
            for replica in range(numReplica):
                print(f"replica --- {replica}")

                if "name" in self.parameters:
                    strImgPath = "{}/replica{}/IMG/{}_{}.png".format(self.mainWindows.output_folder,replica,self.__class__.__name__, self.parameters["name"])
                    strCsvPath = "{}/replica{}/CSV/{}_{}.csv".format(self.mainWindows.output_folder,replica,self.__class__.__name__, self.parameters["name"])
                    self.parameters["imgPath"].append(strImgPath)
                    self.parameters["csvPath"].append(strCsvPath)
        else:
            if "name" in self.parameters: #alignment object dosn't generate graphs and doesn't have "name"
                strImgPath = "{}/IMG/{}_{}.png".format(self.mainWindows.output_folder,self.__class__.__name__, self.parameters["name"])
                strCsvPath = "{}/CSV/{}_{}.csv".format(self.mainWindows.output_folder,self.__class__.__name__, self.parameters["name"])
                self.parameters["imgPath"].append(strImgPath)
                self.parameters["csvPath"].append(strCsvPath)


    @pyqtSlot()
    def check_selection(self, lineEditSelection):
        # TODO : do it on trajectory writing instead to avoid slow writting
        selection = lineEditSelection.text()
        #if no trajectory already loaded.
        if self.mainWindows.trajSelectionTest is None:
            try:
                trajPath = self.mainWindows.listWidgetInputTrajectories.item(0).text()
            except:
                return
            topPath = self.mainWindows.lineEditInputTopologyPath.text()
            if not trajPath in ["", "Add trajectory"] and not topPath == "":
                if self.mainWindows.check_files_ok():
                    frame0 = self.mainWindows.read_single_traj_from_listWidget(0, 0)
                    #register the trajectory test in mainWindows object (just 1 frame).
                    self.mainWindows.setTrajSelectionTest(frame0)
            else:
                return

        try:
            # sel = self.mainWindows.trajSelectionTest.top.select(selection)
            #self.mainWindows.trajSelectionTest = First frame of a trajectory
            #selection = selection string
            #sel list of selected atom.
            sel = self.improvedSelection(self.mainWindows.trajSelectionTest, selection)


            if len(sel) > 0:
                lineEditSelection.setStyleSheet("border: 2px solid green;")
                self.mainWindows.selectionOK = True
            else:
                lineEditSelection.setStyleSheet("border: 2px solid red;")
                self.mainWindows.selectionOK = False
        except:
            if selection == "":
                lineEditSelection.setStyleSheet("")
                self.mainWindows.selectionOK = True
            else:
                lineEditSelection.setStyleSheet("border: 2px solid red;")
                self.mainWindows.statusbar.showMessage("ERROR : no atom selected")
                self.mainWindows.selectionOK = False

    def show_DataFrame(self, lineEditSelection):
        selection = lineEditSelection.text()
        if self.mainWindows.trajSelectionTest is None:
            return

        sel = self.improvedSelection(self.mainWindows.trajSelectionTest, selection)
        # sel = self.mainWindows.trajSelectionTest.top.select(selection)
        if len(sel) == 0:
            return

        tempTraj = self.mainWindows.trajSelectionTest.atom_slice(sel)
        df, bond = tempTraj.top.to_dataframe()

        self.pandasTV = QtWidgets.QTableView()
        self.pandasTV.resize(750, 300)
        gridLayout = QtWidgets.QGridLayout(self.pandasTV)
        gridLayout.setContentsMargins(10, 10, 10, 10)
        gridLayout.addWidget(self.pandasTV, 0, 0, 1, 1)

        model = PandasModel(df)
        self.pandasTV.setModel(model)
        self.pandasTV.show()













