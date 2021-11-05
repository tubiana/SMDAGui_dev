from .base import *

class SecondaryStructures(Analyses):
    def __init__(self, parent=None, mainWindows=None, numReplica=1):
        """
        Initialise the current analysis class.

        Args:
            parent (QtWidgets.QTreeWidgetItem): widget where this class belongs to (Tree widgets). This is needed to
                                                organise all the widgets analysis.
            mainWindows (core.MainWindow): Current main windows object, that contain needed functions for visualization
            numReplica (in): Replica number if we have several replicas.
        """

        super().__init__("Secondary Structures", parent, mainWindows, numReplica)
        self.atomSelection = ""
        self.frameRef = 0
        self.widget = None
        self.init_widget()

        self.arguments = ["name", "Selection", "Simplified"]
        # self.fig = None
        # self.ax = None
        self.lineEditName.textChanged.connect(self.on_lineEditName_textChanged)
        self.lineEditSelection.textChanged.connect(lambda: self.check_selection(self.lineEditSelection))
        self.pushButtonShowAtoms.clicked.connect(lambda: self.show_DataFrame(self.lineEditSelection))

    def generate_graphs(self, resultsDF, replica):
        """
        Override the base.generate_graphs function because since the basic one is not compatible with this kind of data.

        Note:
            No return but the figure is stored in the class (self.figures)
        Args:
            resultsDF (pandas.DataFrame): Dataframe with all the results
            replica (int): replica number
        """
        ax, fig = self.graph_SS(resultsDF,
                                self.parameters["name"],
                                self.parameters["imgPath"][replica],
                                )

        self.figures.append([self.store_figure(ax=ax, fig=fig)])

    def do_calculations(self, traj):
        """
        Main calculation function. It has to return a dataframe object with the results
        Args:
            traj (mdtraj.trajectory):  trajectory object

        Returns:
            rmsdDF (pandas.DataFrame):  DataFrame with all the results
        """
        atoms = self.improvedSelection(traj, self.lineEditSelection.text())

        # TODO CHECK TIMESTEP
        time = traj.time / 1000

        subtraj = traj.atom_slice(atoms)
        resSeq = [x.resSeq for x in list(subtraj.topology.residues)]
        time = ["{:.2f}".format(x) for x in subtraj.time / 1000]

        dss = md.compute_dssp(subtraj, self.checkBoxSimplified.isChecked())

        resultsDF = pd.DataFrame(dss.T, index=resSeq, columns=time)
        return resultsDF

    def retrieve_parameters(self, replica=None):
        """
        Get all parameters from PyQt widgets for this analysis class and save them into a dictionnary that will be used
        to save the parameters in a json file.

        Args:
            numReplica: Replica number. Not used for now.
        """
        self.parameters["name"] = self.lineEditName.text()
        self.parameters["Selection"] = self.lineEditSelection.text()
        self.parameters["Simplified"] = self.checkBoxSimplified.isChecked()

    def loadFromDict(self, dictionnary):
        """
        Load all parameters from dict and then inject them inside PyQt widgets.

        Args:
            dictionnary (dict): dictionnary with all the parameters.
        """
        self.parameters = dictionnary

        self.lineEditName.setText(self.parameters["name"])
        self.lineEditSelection.setText(self.parameters["Selection"])
        self.checkBoxSimplified.setChecked(self.parameters["Simplified"])

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

        self.labelSelection = QtWidgets.QLabel(self.widget)
        self.labelSelection.setText("Atoms Selection")
        self.lineEditSelection = QtWidgets.QLineEdit(self.widget)
        self.lineEditSelection.setObjectName("lineEditSelection")
        self.lineEditSelection.setText("protein")
        self.pushButtonShowAtoms = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtoms.setText("Show selected atoms")
        self.pushButtonShowAtoms.setObjectName("pushButtonShowAtoms")

        self.checkBoxSimplified = QtWidgets.QCheckBox(self.widget)
        self.checkBoxSimplified.setText("Simplified version of DSSP ?")
        self.checkBoxSimplified.setObjectName("checkBoxSimplified")
        self.checkBoxSimplified.setChecked(True)

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
        self.Hlayout3.addWidget(self.checkBoxSimplified)
        self.Hlayout3.addStretch()

        self.gridLayout.addLayout(self.Hlayout0, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout1, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout2, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout3, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2)
        # Now fill HTML Description
        self.textBrowserDescription.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600; text-decoration: underline;\">Secondary Structure Consevation</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Compute secondary structure through the trajectory</p>\n"
            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Name</span> : Name used for graphics. Please use an <span style=\" font-weight:600;\">unique</span> name.</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">AtomSelection</span> : atom selection for atom group</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Simplified</span> : Use a simplified version of secondary structure (only Helix, Sheet or Coil)</p>\n"
            "</body></html>\n")