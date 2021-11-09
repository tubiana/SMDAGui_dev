from .base import *

class Surface(Analyses):
    # TODO add radiilist (button, widget with table showing up with "ATOM" and "RADIUS"), then conversion into dictionnary
    def __init__(self, parent=None, mainWindows=None, numReplica=1):
        """
        Initialise the current analysis class.

        Args:
            parent (QtWidgets.QTreeWidgetItem): widget where this class belongs to (Tree widgets). This is needed to
                                                organise all the widgets analysis.
            mainWindows (core.MainWindow): Current main windows object, that contain needed functions for visualization
            numReplica (in): Replica number if we have several replicas.
        """
        super().__init__("SASA", parent, mainWindows, numReplica)

        self.atomSelection = ""
        self.frameRef = 0
        self.widget = None
        self.init_widget()

        self.arguments = ["name", "selection", "probe", "points", "mode"]
        # self.fig = None
        # self.ax = None

        self.yAxisLabel = "SASA (A²)"
        self.xAxisLabel = "Time (ns)"
        self.lineColor = "magenta"

        self.lineEditName.textChanged.connect(self.on_lineEditName_textChanged)
        self.lineEditSelection.textChanged.connect(lambda: self.check_selection(self.lineEditSelection))
        self.pushButtonShowAtoms.clicked.connect(lambda: self.show_DataFrame(self.lineEditSelection))

    def do_calculations(self, traj):
        """
        Main calculation function. It has to return a dataframe object with the results
        Args:
            traj (mdtraj.trajectory):  trajectory object

        Returns:
            rmsdDF (pandas.DataFrame):  DataFrame with all the results
        """
        selected_atoms = self.improvedSelection(traj, self.parameters["selection"])
        subtraj = traj.atom_slice(selected_atoms)

        try:
            sasa = md.shrake_rupley(subtraj,
                                    probe_radius=self.spinBoxProbe.value(),
                                    n_sphere_points=self.spinBoxPoints.value(),
                                    mode=self.comboBoxMode.currentText())
        except:
            return False
        # TODO : average sasa per atom/residues
        result = sasa.sum(axis=1)  # 1 = frames
        resultsDF = pd.DataFrame({self.yAxisLabel: result * 10,
                                  self.xAxisLabel: traj.time / 1000})
        resultsDF["Average"] = scipy.signal.savgol_filter(resultsDF[self.yAxisLabel], 21, 3)
        return resultsDF

    def loadFromDict(self, dictionnary):
        """
        Load all parameters from dict and then inject them inside PyQt widgets.

        Args:
            dictionnary (dict): dictionnary with all the parameters.
        """
        self.parameters = dictionnary

        self.lineEditName.setText(self.parameters["name"])
        self.lineEditSelection.setText(self.parameters["selection"])
        self.spinBoxProbe.setValue(self.parameters["probe"])
        self.comboBoxMode.setCurrentText(self.parameters["mode"])
        self.spinBoxPoints.setValue(self.parameters["points"])

        self.restore_graphs()

    def retrieve_parameters(self, replica=None):
        """
        Get all parameters from PyQt widgets for this analysis class and save them into a dictionnary that will be used
        to save the parameters in a json file.

        Args:
            numReplica: Replica number. Not used for now.
        """
        self.parameters["name"] = self.lineEditName.text()
        self.parameters["selection"] = self.lineEditSelection.text()
        self.parameters["mode"] = self.comboBoxMode.currentText()
        self.parameters["probe"] = self.spinBoxProbe.value()
        self.parameters["points"] = self.spinBoxPoints.value()

    def init_widget(self):
        """
        Initialise all PyQt widgets
        """
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

        self.labelSelection = QtWidgets.QLabel(self.widget)
        self.labelSelection.setText("Atoms Selection")
        self.lineEditSelection = QtWidgets.QLineEdit(self.widget)
        self.lineEditSelection.setObjectName("lineEditSelection")
        self.pushButtonShowAtoms = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtoms.setText("Show selected atoms")
        self.pushButtonShowAtoms.setObjectName("pushButtonShowAtoms")

        self.labelMode = QtWidgets.QLabel(self.widget)
        self.labelMode.setText("Mode :")
        self.comboBoxMode = QtWidgets.QComboBox(self.widget)
        self.comboBoxMode.addItem("atom")
        self.comboBoxMode.addItem("residue")
        self.comboBoxMode.setCurrentIndex(1)  # Residue per default

        self.labelProbe = QtWidgets.QLabel(self.widget)
        self.labelProbe.setText("Probe Radius (in nm)")
        self.spinBoxProbe = QtWidgets.QDoubleSpinBox(self.widget)
        self.spinBoxProbe.setMaximum(99)
        self.spinBoxProbe.setSingleStep(0.01)
        self.spinBoxProbe.setValue(0.14)
        self.spinBoxProbe.setObjectName("spinBoxProbe")

        self.labelPoints = QtWidgets.QLabel(self.widget)
        self.labelPoints.setText("Number of points in sphere")
        self.spinBoxPoints = QtWidgets.QSpinBox(self.widget)
        self.spinBoxPoints.setMaximum(1500)
        self.spinBoxPoints.setSingleStep(1)
        self.spinBoxPoints.setValue(960)
        self.spinBoxPoints.setObjectName("spinBoxPoints")

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
        self.Hlayout3.addWidget(self.labelMode)
        self.Hlayout3.addWidget(self.comboBoxMode)
        self.Hlayout3.addStretch()

        self.Hlayout4 = QtWidgets.QHBoxLayout()
        self.Hlayout4.addWidget(self.labelProbe)
        self.Hlayout4.addWidget(self.spinBoxProbe)
        self.Hlayout4.addStretch()

        self.Hlayout5 = QtWidgets.QHBoxLayout()
        self.Hlayout5.addWidget(self.labelPoints)
        self.Hlayout5.addWidget(self.spinBoxPoints)
        self.Hlayout5.addStretch()

        self.gridLayout.addLayout(self.Hlayout0, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout1, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout2, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout3, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout4, 4, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout5, 5, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2)
        # Now fill HTML Description
        self.textBrowserDescription.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600; text-decoration: underline;\">Accessible Surface Calculation</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Accessible surface calculation using Shrake and Rupley algorithm.</p>\n"
            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Name</span> : Name used for graphics. Please use an <span style=\" font-weight:600;\">unique</span> name.</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">AtomSelection</span> : atom selection for atom group</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Mode</span> : Calcul surface per atoms or per residues ?</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Probe Radius</span> : Size of the probe radius (default value = 1.4A)</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Number of points</span> : Number of points per sphere (each atom is converted in sphere)</p></body></html>\n"
        )