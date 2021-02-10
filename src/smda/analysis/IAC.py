import PyQt5.QtWidgets as QtWidgets

from .base import Analyses


class IAC(Analyses):
    """
    Imaging, Align and Center
    """

    def __init__(self, parent=None, mainWindows=None, numReplica=1):
        """
        Initialise the current analysis class.

        Args:
            parent (QtWidgets.QTreeWidgetItem): widget where this class belongs to (Tree widgets). This is needed to
                                                organise all the widgets analysis.
            mainWindows (core.MainWindow): Current main windows object, that contain needed functions for visualization
            numReplica (in): Replica number if we have several replicas.
        """

        super().__init__(
            "Imaging, Alignement, Centering", parent, mainWindows, numReplica
        )

        self.atomSelection = ""
        self.widget = None
        self.init_widget()

        self.arguments = ["lineEditSelectionAlignement"]
        # self.fig = None
        # self.ax = None

        self.lineEditSelectionAlignement.textChanged.connect(
            lambda: self.check_selection(self.lineEditSelectionAlignement)
        )
        self.pushButtonShowAtomsAlignement.clicked.connect(
            lambda: self.show_DataFrame(self.lineEditSelectionAlignement)
        )

        self.checkBoxAlignement.toggled["bool"].connect(
            self.lineEditSelectionAlignement.setEnabled
        )
        self.checkBoxAlignement.toggled["bool"].connect(
            self.pushButtonShowAtomsAlignement.setEnabled
        )

    def show_graph(self, parent, replica=None):
        """
        Override the base.show_graph function to avoid showing graphs : this is a tool function, no graph is generated

        Note:
            No return but the figure is stored in the class (self.figures)
        Args:
            parent (GraphicsViewResult): graphic view layout
            replica (int): replica number
        """
        return None

    def do_analysis(self, traj, replica=None, numReplica=1):
        """
        override the base.do_analysis function.
        alignment will modify the trajectory, no graph, no results outputs.
        Args:
            traj (mdtraj.trajectory):  trajectory object
            replica (int): Number of replicas
            numReplica (int): replica Number
        Returns:
            traj (mdtraj.trajectory):  trajectory object
        """

        self.mainWindows.statusbar.showMessage(
            "Imagine, Aligning and centering trajectory"
        )
        # 1 Get parameters
        self.retrieve_parameters()

        if self.checkBoxImaging.isChecked():
            traj.image_molecules(inplace=True)

        if self.checkBoxAlignement.isChecked():
            selectedAtoms = self.improvedSelection(
                traj, self.lineEditSelectionAlignement.text()
            )
            traj.superpose(traj, 0, selectedAtoms)

        if self.checkBoxCentering.isChecked():
            traj.center_coordinates()

        return traj

    def loadFromDict(self, dictionnary):
        """
        Load all parameters from dict and then inject them inside PyQt widgets.

        Args:
            dictionnary (dict): dictionnary with all the parameters.
        """

        self.parameters = dictionnary
        self.checkBoxImaging.setChecked(self.parameters["checkBoxImaging"])
        self.checkBoxAlignement.setChecked(self.parameters["checkBoxAlignement"])
        self.checkBoxCentering.setChecked(self.parameters["checkBoxCentering"])
        self.lineEditSelectionAlignement.setText(
            self.parameters["lineEditSelectionAlignement"]
        )

    def retrieve_parameters(self, replica=None):
        """
        Get all parameters from PyQt widgets for this analysis class and save them into a dictionnary that will be used
        to save the parameters in a json file.

        Args:
            numReplica: Replica number. Not used for now.
        """

        self.parameters["checkBoxImaging"] = self.checkBoxImaging.isChecked()
        self.parameters["checkBoxAlignement"] = self.checkBoxAlignement.isChecked()
        self.parameters[
            "lineEditSelectionAlignement"
        ] = self.lineEditSelectionAlignement.text()
        self.parameters["checkBoxCentering"] = self.checkBoxCentering.isChecked()

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

        self.labelSelectionAlignement = QtWidgets.QLabel(self.widget)
        self.labelSelectionAlignement.setText("Atoms Selection")
        self.lineEditSelectionAlignement = QtWidgets.QLineEdit(self.widget)
        self.lineEditSelectionAlignement.setObjectName("lineEditSelectionAlignement")
        self.lineEditSelectionAlignement.setText("protein")
        self.pushButtonShowAtomsAlignement = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtomsAlignement.setText("showSelectedAtoms")
        self.pushButtonShowAtomsAlignement.setObjectName(
            "pushButtonShowAtomsAlignement"
        )

        self.checkBoxImaging = QtWidgets.QCheckBox(self.widget)
        self.checkBoxImaging.setText("Imaging Trajectory ?")
        self.checkBoxImaging.setObjectName("checkBoxImaging")
        self.checkBoxImaging.setChecked(False)

        self.checkBoxAlignement = QtWidgets.QCheckBox(self.widget)
        self.checkBoxAlignement.setText("Align Trajectory ?")
        self.checkBoxAlignement.setObjectName("checkBoxAlignement")
        self.checkBoxAlignement.setChecked(True)

        self.checkBoxCentering = QtWidgets.QCheckBox(self.widget)
        self.checkBoxCentering.setText("Centering Trajectory ?")
        self.checkBoxCentering.setObjectName("checkBoxCentering")
        self.checkBoxCentering.setChecked(True)

        # Now the layout : 4 Horizontals layouts

        self.Hlayout0 = QtWidgets.QHBoxLayout()
        self.Hlayout0.addWidget(self.textBrowserDescription)

        self.Hlayout1 = QtWidgets.QHBoxLayout()
        self.Hlayout1.addWidget(self.checkBoxImaging)

        self.Hlayout2 = QtWidgets.QHBoxLayout()
        self.Hlayout2.addWidget(self.checkBoxAlignement)

        self.Hlayout3 = QtWidgets.QHBoxLayout()
        self.Hlayout3.addWidget(self.labelSelectionAlignement)
        self.Hlayout3.addWidget(self.lineEditSelectionAlignement)
        self.Hlayout3.addWidget(self.pushButtonShowAtomsAlignement)
        self.Hlayout3.addStretch()

        self.Hlayout4 = QtWidgets.QHBoxLayout()
        self.Hlayout4.addWidget(self.checkBoxCentering)

        self.gridLayout.addLayout(self.Hlayout0, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout1, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout2, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout3, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout4, 4, 0, 1, 1)

        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout.addItem(spacerItem2)
        # Now fill HTML Description
        self.textBrowserDescription.setHtml(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
            '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
            "</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
            '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:16pt; font-weight:600; text-decoration: underline;">I.A.C - Imaging, Align and Center</span></p>\n'
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">remove molecular 'breaks' caused by periodic conditions, align the system on a selection and center to the origin the system.</p>\n"
            '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" text-decoration: underline;">AtomSelection</span> : atom selection for Centering/Alignement.</p>\n'
            "</body></html>"
        )
