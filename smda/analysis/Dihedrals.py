from .base import *

class Dihedrals(Analyses):

    def __init__(self, parent=None, mainWindows=None, numReplica=1):
        """
        Initialise the current analysis class.

        Args:
            parent (QtWidgets.QTreeWidgetItem): widget where this class belongs to (Tree widgets). This is needed to
                                                organise all the widgets analysis.
            mainWindows (core.MainWindow): Current main windows object, that contain needed functions for visualization
            numReplica (in): Replica number if we have several replicas.
        """
        super().__init__("Dihedral", parent, mainWindows, numReplica)
        self.widget = None
        self.init_widget()

        self.arguments = ["name", "selection1", "selection2", "selection3", "selection4"]

        self.yAxisLabel = "Angle (°)"
        self.xAxisLabel = "Time (ns)"
        self.lineColor = "cyan"

        self.lineEditName.textChanged.connect(self.on_lineEditName_textChanged)
        self.lineEditSelection1.textChanged.connect(lambda: self.check_selection(self.lineEditSelection1))
        self.lineEditSelection2.textChanged.connect(lambda: self.check_selection(self.lineEditSelection2))
        self.lineEditSelection3.textChanged.connect(lambda: self.check_selection(self.lineEditSelection3))
        self.lineEditSelection4.textChanged.connect(lambda: self.check_selection(self.lineEditSelection4))
        self.pushButtonShowAtoms1.clicked.connect(lambda: self.show_DataFrame(self.lineEditSelection1))
        self.pushButtonShowAtoms2.clicked.connect(lambda: self.show_DataFrame(self.lineEditSelection2))
        self.pushButtonShowAtoms3.clicked.connect(lambda: self.show_DataFrame(self.lineEditSelection3))
        self.pushButtonShowAtoms4.clicked.connect(lambda: self.show_DataFrame(self.lineEditSelection4))

    def do_calculations(self, traj):
        """
        Main calculation function. It has to return a dataframe object with the results
        Args:
            traj (mdtraj.trajectory):  trajectory object

        Returns:
            resultsDF (pandas.DataFrame):  DataFrame with all the results
        """
        at1 = self.improvedSelection(traj, self.lineEditSelection1.text())
        at2 = self.improvedSelection(traj, self.lineEditSelection2.text())
        at3 = self.improvedSelection(traj, self.lineEditSelection3.text())
        at4 = self.improvedSelection(traj, self.lineEditSelection4.text())

        if len(at1) != 1 or len(at2) != 1 or len(at3) != 1 or len(at4) != 1:
            return False

        indices = np.array([[at1[0], at2[0], at3[0], at4[0]]])
        angles = md.compute_dihedrals(traj, indices)
        degrees = np.asarray(angles).flatten() * 180 / np.pi
        outAngles = degrees % 360

        resultsDF = pd.DataFrame({self.yAxisLabel: outAngles,
                                  self.xAxisLabel: traj.time / 1000})
        resultsDF["Average"] = scipy.signal.savgol_filter(resultsDF[self.yAxisLabel], 21, 3)
        return resultsDF

    def retrieve_parameters(self, replica=None):
        """
        Get all parameters from PyQt widgets for this analysis class and save them into a dictionnary that will be used
        to save the parameters in a json file.

        Args:
            numReplica: Replica number. Not used for now.
        """

        self.parameters["name"] = self.lineEditName.text()
        self.parameters["selection1"] = self.lineEditSelection1.text()
        self.parameters["selection2"] = self.lineEditSelection2.text()
        self.parameters["selection3"] = self.lineEditSelection3.text()
        self.parameters["selection4"] = self.lineEditSelection3.text()

    def loadFromDict(self, dictionnary):
        """
        Load all parameters from dict and then inject them inside PyQt widgets.

        Args:
           dictionnary (dict): dictionnary with all the parameters.
        """
        self.parameters = dictionnary

        self.lineEditName.setText(self.parameters["name"])
        self.lineEditSelection1.setText(self.parameters["selection1"])
        self.lineEditSelection2.setText(self.parameters["selection2"])
        self.lineEditSelection3.setText(self.parameters["selection3"])
        self.lineEditSelection4.setText(self.parameters["selection4"])

        self.restore_graphs()

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

        self.labelSelection1 = QtWidgets.QLabel(self.widget)
        self.labelSelection1.setText("Atoms Selection")
        self.lineEditSelection1 = QtWidgets.QLineEdit(self.widget)
        self.lineEditSelection1.setObjectName("lineEditSelection1")
        self.pushButtonShowAtoms1 = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtoms1.setText("Show selected atoms")
        self.pushButtonShowAtoms1.setObjectName("pushButtonShowAtoms1")

        self.labelSelection2 = QtWidgets.QLabel(self.widget)
        self.labelSelection2.setText("Atoms Selection")
        self.lineEditSelection2 = QtWidgets.QLineEdit(self.widget)
        self.lineEditSelection2.setObjectName("lineEditSelection2")
        self.pushButtonShowAtoms2 = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtoms2.setText("Show selected atoms")
        self.pushButtonShowAtoms2.setObjectName("pushButtonShowAtoms2")

        self.labelSelection3 = QtWidgets.QLabel(self.widget)
        self.labelSelection3.setText("Atoms Selection")
        self.lineEditSelection3 = QtWidgets.QLineEdit(self.widget)
        self.lineEditSelection3.setObjectName("lineEditSelection3")
        self.pushButtonShowAtoms3 = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtoms3.setText("Show selected atoms")
        self.pushButtonShowAtoms3.setObjectName("pushButtonShowAtoms3")

        self.labelSelection4 = QtWidgets.QLabel(self.widget)
        self.labelSelection4.setText("Atoms Selection")
        self.lineEditSelection4 = QtWidgets.QLineEdit(self.widget)
        self.lineEditSelection4.setObjectName("lineEditSelection4")
        self.pushButtonShowAtoms4 = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtoms4.setText("Show selected atoms")
        self.pushButtonShowAtoms4.setObjectName("pushButtonShowAtoms4")
        # Now the layout : 4 Horizontals layouts

        self.Hlayout0 = QtWidgets.QHBoxLayout()
        self.Hlayout0.addWidget(self.textBrowserDescription)

        self.Hlayout1 = QtWidgets.QHBoxLayout()
        self.Hlayout1.addWidget(self.labelName)
        self.Hlayout1.addWidget(self.lineEditName)
        # self.Hlayout1.addStretch()

        self.Hlayout2 = QtWidgets.QHBoxLayout()
        self.Hlayout2.addWidget(self.labelSelection1)
        self.Hlayout2.addWidget(self.lineEditSelection1)
        self.Hlayout2.addWidget(self.pushButtonShowAtoms1)
        self.Hlayout2.addStretch()

        self.Hlayout3 = QtWidgets.QHBoxLayout()
        self.Hlayout3.addWidget(self.labelSelection2)
        self.Hlayout3.addWidget(self.lineEditSelection2)
        self.Hlayout3.addWidget(self.pushButtonShowAtoms2)
        self.Hlayout3.addStretch()

        self.Hlayout4 = QtWidgets.QHBoxLayout()
        self.Hlayout4.addWidget(self.labelSelection3)
        self.Hlayout4.addWidget(self.lineEditSelection3)
        self.Hlayout4.addWidget(self.pushButtonShowAtoms3)
        self.Hlayout4.addStretch()

        self.Hlayout5 = QtWidgets.QHBoxLayout()
        self.Hlayout5.addWidget(self.labelSelection4)
        self.Hlayout5.addWidget(self.lineEditSelection4)
        self.Hlayout5.addWidget(self.pushButtonShowAtoms4)
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
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600; text-decoration: underline;\">Dihedrals</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Compute the angle between 4 atoms (dihedral angles).</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">PLEASE SELECT 1 ATOM ONLY PER SELECTION.</p>\n"
            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Name</span> : Name used for graphics. Please use an <span style=\" font-weight:600;\">unique</span> name.</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">AtomSelection1</span> : atom selection for first atom </p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">AtomSelection2</span> : atom selection for second atom </p></body></html>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">AtomSelection2</span> : atom selection for third atom </p></body></html>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">AtomSelection2</span> : atom selection for fourth atom </p></body></html>\n"
        )
