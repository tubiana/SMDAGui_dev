import mdtraj as md
import numpy as np
import pandas as pd
import PyQt5.QtWidgets as QtWidgets
import scipy.signal

from .base import Analyses


class Protrusions(Analyses):
    def __init__(self, parent=None, mainWindows=None, numReplica=1):
        """
        Initialise the current analysis class.

        Args:
            parent (QtWidgets.QTreeWidgetItem): widget where this class belongs to (Tree widgets). This is needed to
                                                organise all the widgets analysis.
            mainWindows (core.MainWindow): Current main windows object, that contain needed functions for visualization
            numReplica (in): Replica number if we have several replicas.
        """

        super().__init__("Hydrophobic Protrusion", parent, mainWindows, numReplica)
        self.atomSelection = ""
        self.frameRef = 0
        self.widget = None
        self.init_widget()

        self.arguments = ["name", "selection", "density", "distance cut-off"]
        self.fig = []
        self.ax = []

        self.yAxisLabel = "Protrusions Count"
        self.xAxisLabel = "Frame"
        self.lineColor = "red"

        self.lineEditName.textChanged.connect(self.on_lineEditName_textChanged)
        self.lineEditSelection.textChanged.connect(
            lambda: self.check_selection(self.lineEditSelection)
        )
        self.pushButtonShowAtoms.clicked.connect(
            lambda: self.show_DataFrame(self.lineEditSelection)
        )
        self.tabGraphName = ["Time series", "H-bond count"]

    def generate_graphs(self, resultsDF, replica=0):
        """
        Override the base.generate_graphs function because since the basic one is not compatible with this kind of data.

        Note:
            No return but the figure is stored in the class (self.figures)
        Args:
            resultsDF (pandas.DataFrame): Dataframe with all the results
            replica (int): replica number
        """
        graphs = []
        ax, fig = self.graph_HBOND(
            resultsDF, self.parameters["name"], self.parameters["imgPath"][replica]
        )
        graphs.append(self.store_figure(ax=ax, fig=fig))
        summedGraphPath = (
            self.parameters["imgPath"][replica].split(".png")[0] + "_summed.png"
        )
        ax2, fig2 = self.calc_summed_graph(resultsDF, imgPath=summedGraphPath)
        if ax2 and fig2:
            graphs.append(self.store_figure(ax=ax2, fig=fig2))
        self.figures.append(graphs)

    def calc_summed_graph(self, resultsDF, imgPath):
        """
        Calculate the summed graphic (another graph that can be done on MD trajectories).
        Args:
            resultsDF (pandas.DataFrame): Dataframe with all the results
            imgPath (string): output folder for graphic saving.
        """

        dat = resultsDF.drop("Freq", axis="columns").sum(axis=0)
        time = list(resultsDF.drop("Freq", axis="columns").columns)
        count = pd.DataFrame({self.yAxisLabel: dat, self.xAxisLabel: time})

        if len(count) > 100:
            count["Average"] = scipy.signal.savgol_filter(count[self.yAxisLabel], 21, 3)

        if not count.empty:
            ax, fig = self.graph_XY(
                count, self.__class__.__name__, self.parameters["name"], imgPath
            )

            return (ax, fig)
        else:
            return (None, None)

    def do_calculations(self, traj):
        """
        Main calculation function. It has to return a dataframe object with the results

        Args:
            traj (mdtraj.trajectory):  trajectory object

        Returns:
            resultDF (pandas.DataFrame):  DataFrame with all the results
        """
        # TODO: should be removed ?
        # result = pd.DataFrame()

        hydrophobic_residue = ["MET", "CYS", "ILE", "LEU", "TYR", "PHE", "TRP"]
        # Select the atoms for the convexhul hull calculation
        selection = self.lineEditSelection.text()
        cutoff = self.spinBoxCutoff.value()
        density = self.spinBoxDensity.value()

        subtraj = traj.atom_slice(
            traj.top.select(f"{selection} and (name CA or name CB)")
        )

        labelDict = {}
        for atom in subtraj.top.atoms:
            labelDict[atom.index] = f"{atom.residue.name}-{atom.residue.resSeq}"

        resultNumpyArray = np.zeros((len(labelDict), subtraj.n_frames), dtype=int)

        import time

        start = time.time()
        for frame in range(subtraj.n_frames):
            coords = subtraj.xyz[frame]

            from scipy.spatial import ConvexHull

            hull = ConvexHull(coords)  # Calculation of the ConvexHull

            vertices = (
                hull.vertices
            )  # Vertices correspond to the atoms in the coordinates.
            neighbor = md.compute_neighborlist(
                subtraj, cutoff, frame
            )  # calculate the neighbors for each CA/CB for frame i

            # Keep only the protrusion
            # TODO: should be removed ?
            # protrusionIndex = []
            for vertex in vertices:
                if len(neighbor[vertex] < density):
                    if self.checkBoxHydrophobic.isChecked():
                        if labelDict[vertex][:3] in hydrophobic_residue:
                            # ADD ONLY CB ATOMS
                            if subtraj.top.atom(vertex).name == "CB":
                                resultNumpyArray[vertex, frame] = 1

        resultDF = pd.DataFrame(resultNumpyArray, index=labelDict.values())

        # Remove empty lines
        resultDF = resultDF.loc[
            (resultDF != 0).any(1),
        ]
        resultDF["Freq"] = resultDF.sum(axis=1) / subtraj.n_frames

        end = time.time()
        print(f"convhullCalculation = {end-start}")
        return resultDF

    def add_outPath_in_parameters(self, numReplica=None):
        """
        Overide add_outPath_in_parameters since for HBonds we have 2 graphics.
        This is to store imgPath and csvPath inside the parameter dict (used to load/save parameters)
        Note:
            No return, everything is saved in self.parameters
        Args:
            numReplica (int): replica number.
        """

        # Reset path in list.
        self.parameters["imgPath"] = []
        self.parameters["csvPath"] = []

        if numReplica and numReplica > 1:
            for replica in range(numReplica):
                print(f"replica --- {replica}")
                strImgPath = "IMG/replica{}/{}_{}.png".format(
                    replica, self.__class__.__name__, self.parameters["name"]
                )
                strCsvPath = "CSV/replica{}/{}_{}.csv".format(
                    replica, self.__class__.__name__, self.parameters["name"]
                )
                self.parameters["imgPath"].append(strImgPath)
                self.parameters["csvPath"].append(strCsvPath)
        else:
            strImgPath = "IMG/{}_{}.png".format(
                self.__class__.__name__, self.parameters["name"]
            )
            strCsvPath = "CSV/{}_{}.csv".format(
                self.__class__.__name__, self.parameters["name"]
            )
            self.parameters["imgPath"].append(strImgPath)
            self.parameters["csvPath"].append(strCsvPath)

    def retrieve_parameters(self, replica=None):
        """
        Get all parameters from PyQt widgets for this analysis class and save them into a dictionnary that will be used
        to save the parameters in a json file.

        Args:
            numReplica: Replica number. Not used for now.
        """
        self.parameters["name"] = self.lineEditName.text()
        self.parameters["selection"] = self.lineEditSelection.text()
        self.parameters["density"] = self.spinBoxDensity.value()
        self.parameters["distance cut-off"] = self.spinBoxCutoff.value()
        self.parameters["freq"] = self.spinBoxFreq.value()
        self.parameters["checkBoxHydrophobic"] = self.checkBoxHydrophobic.isChecked()

        # self.parameters["imgPath"] = ["IMG/{}_{}.png".format(self.__class__.__name__, self.parameters["name"]),
        #                               "IMG/{}-count_{}.png".format(self.__class__.__name__, self.parameters["name"])]
        # self.parameters["csvPath"] = "CSV/{}_{}.csv".format(self.__class__.__name__, self.parameters["name"])

    def loadFromDict(self, dictionnary):
        """
        Load all parameters from dict and then inject them inside PyQt widgets.

        Args:
            dictionnary (dict): dictionnary with all the parameters.
        """

        self.parameters = dictionnary

        self.lineEditName.setText(self.parameters["name"])
        self.lineEditSelection.setText(self.parameters["selection"])
        self.spinBoxDensity.setValue(self.parameters["density"])
        self.spinBoxCutoff.setValue(self.parameters["distance cut-off"])
        self.spinBoxFreq.setValue(self.parameters["freq"])
        self.checkBoxHydrophobic.setChecked(self.parameters["checkBoxHydrophobic"])
        self.restore_graphs()

    # redefine store_figure and show graph to take care of figure store in list.

    def init_widget(self):
        """
        Initialise all PyQt widgets
        """

        self.widget = QtWidgets.QWidget()  # Main Widget
        self.widget.setObjectName("widget")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
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

        self.labelSelection = QtWidgets.QLabel(self.widget)
        self.labelSelection.setText("Atoms Selection")
        self.lineEditSelection = QtWidgets.QLineEdit(self.widget)
        self.lineEditSelection.setObjectName("lineEditSelection")
        self.lineEditSelection.setText("protein")
        self.pushButtonShowAtoms = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtoms.setText("Show selected atoms")
        self.pushButtonShowAtoms.setObjectName("pushButtonShowAtoms")

        self.labelDensity = QtWidgets.QLabel(self.widget)
        self.labelDensity.setText("Density value")
        self.spinBoxDensity = QtWidgets.QDoubleSpinBox(self.widget)
        self.spinBoxDensity.setMaximum(30)
        self.spinBoxDensity.setMinimum(1)
        self.spinBoxDensity.setSingleStep(1)
        self.spinBoxDensity.setValue(22)
        self.spinBoxDensity.setObjectName("spinBoxDensity")

        self.labelCutoff = QtWidgets.QLabel(self.widget)
        self.labelCutoff.setText("Distance Cut-off")
        self.spinBoxCutoff = QtWidgets.QDoubleSpinBox(self.widget)
        self.spinBoxCutoff.setMaximum(5)
        self.spinBoxCutoff.setMinimum(0.2)
        self.spinBoxCutoff.setSingleStep(0.1)
        self.spinBoxCutoff.setValue(1)
        self.spinBoxCutoff.setObjectName("spinBoxCutoff")

        self.labelFreq = QtWidgets.QLabel(self.widget)
        self.labelFreq.setText("Cutoff Frequence")
        self.spinBoxFreq = QtWidgets.QDoubleSpinBox(self.widget)
        self.spinBoxFreq.setMaximum(1)
        self.spinBoxFreq.setSingleStep(0.01)
        self.spinBoxFreq.setValue(0.05)
        self.spinBoxFreq.setObjectName("spinBoxFreq")

        self.checkBoxHydrophobic = QtWidgets.QCheckBox(self.widget)
        self.checkBoxHydrophobic.setText("Keep only hydrophobic protrusion ?")
        self.checkBoxHydrophobic.setObjectName("checkBoxHydrophobic")
        self.checkBoxHydrophobic.setChecked(True)

        # Now the layout : 4 Horizontals layouts

        self.Hlayout0 = QtWidgets.QHBoxLayout()
        self.Hlayout0.addWidget(self.textBrowserDescription)

        self.Hlayout1 = QtWidgets.QHBoxLayout()
        self.Hlayout1.addWidget(self.labelName)
        self.Hlayout1.addWidget(self.lineEditName)
        # self.Hlayout1.addStretch()

        self.Hlayout2 = QtWidgets.QHBoxLayout()
        self.Hlayout2.addWidget(self.labelSelection)
        self.Hlayout2.addWidget(self.lineEditSelection)
        self.Hlayout2.addWidget(self.pushButtonShowAtoms)
        self.Hlayout2.addStretch()

        self.Hlayout3 = QtWidgets.QHBoxLayout()
        self.Hlayout3.addWidget(self.labelDensity)
        self.Hlayout3.addWidget(self.spinBoxDensity)
        self.Hlayout3.addStretch()

        self.Hlayout4 = QtWidgets.QHBoxLayout()
        self.Hlayout4.addWidget(self.labelCutoff)
        self.Hlayout4.addWidget(self.spinBoxCutoff)
        self.Hlayout4.addStretch()

        self.Hlayout5 = QtWidgets.QHBoxLayout()
        self.Hlayout5.addWidget(self.labelFreq)
        self.Hlayout5.addWidget(self.spinBoxFreq)
        self.Hlayout5.addStretch()

        self.Hlayout6 = QtWidgets.QHBoxLayout()
        self.Hlayout6.addWidget(self.checkBoxHydrophobic)
        self.Hlayout6.addStretch()

        self.gridLayout.addLayout(self.Hlayout0, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout1, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout2, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout3, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout4, 4, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout5, 5, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout6, 6, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout.addItem(spacerItem2)
        # Now fill HTML Description
        self.textBrowserDescription.setHtml(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
            '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
            '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:16pt; font-weight:600; text-decoration: underline;">PROTRUSION CALCULATION calculation</span></p>\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Calculate the protrusions of a convexhull according this paper : [1]E. Fuglebakk and N. Reuter, “A model for hydrophobic protrusions on peripheral membrane proteins,” PLOS Computational Biology, vol. 14, no. 7, p. e1006325, Jul. 2018. </p>\n'
            '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" text-decoration: underline;">Name</span> : Name used for graphics. Please use an <span style=" font-weight:600;">unique</span> name.</p>\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" text-decoration: underline;">AtomSelection</span> : atom selection for atom group</p>\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" text-decoration: underline;">Freq</span> : Remove all Hbonds found with frequence bellow this cutoff</p>\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" text-decoration: underline;">TODO</span> : TODO</p>\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" text-decoration: underline;">TODO</span> : TODO</p></body></html>\n'
        )
