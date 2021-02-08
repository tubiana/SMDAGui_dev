from PyQt5.QtWidgets import QLabel

from .base import *


class Alignement(Analyses):
    """
    Class used to ALIGN a trajectory.
    """


    def __init__(self, parent=None, mainWindows=None, numReplica=1):
        """
        Initialise the current analysis class : align the trajectory

        Args:
            parent (QtWidgets.QTreeWidgetItem): widget where this class belongs to (Tree widgets). This is needed to
                                                organise all the widgets analysis.
            mainWindows (core.MainWindow): Current main windows object, that contain needed functions for visualization
            numReplica (in): Replica number if we have several replicas.
        """
        super().__init__("Alignement", parent, mainWindows, numReplica)

        self.atomSelection = ""
        self.widget = None
        self.init_widget()

        self.arguments = ["Selection", "RefFrame"]
        # self.fig = None
        # self.ax = None

        self.lineEditSelection.textChanged.connect(lambda: self.check_selection(self.lineEditSelection))
        self.pushButtonShowAtoms.clicked.connect(lambda: self.show_DataFrame(self.lineEditSelection))

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
        self.mainWindows.statusbar.showMessage("Imagine, Aligning and centering trajectory")
        # 1 Get parameters
        self.retrieve_parameters()

        selectedAtoms = self.improvedSelection(traj, self.lineEditSelection.text())
        refFrame = self.spinBoxRefFrame.value()
        traj.superpose(traj, refFrame, selectedAtoms)

        return traj

    def loadFromDict(self, dictionnary):
        """
        Load all parameters from dict and then inject them inside PyQt widgets.

        Args:
            dictionnary (dict): dictionnary with all the parameters.
        """
        self.parameters = dictionnary
        self.spinBoxRefFrame.setValue(self.parameters["RefFrame"])
        self.lineEditSelection.setText(self.parameters["Selection"])

    def retrieve_parameters(self, replica=None):
        """
        Get all parameters from PyQt widgets for this analysis class and save them into a dictionnary that will be used
        to save the parameters in a json file.

        Args:
            numReplica: Replica number. Not used for now.
        """
        self.parameters["Selection"] = self.lineEditSelection.text()
        self.parameters["name"] = "alignment"
        self.parameters["RefFrame"] = self.spinBoxRefFrame.value()

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

        self.labelSelection = QtWidgets.QLabel(self.widget)
        self.labelSelection.setText("Atoms Selection")
        self.lineEditSelection = QtWidgets.QLineEdit(self.widget)
        self.lineEditSelection.setObjectName("lineEditSelection")
        self.pushButtonShowAtoms = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtoms.setText("showSelectedAtoms")
        self.pushButtonShowAtoms.setObjectName("pushButtonShowAtoms")

        self.labelRefFrame = QtWidgets.QLabel(self.widget)
        self.labelRefFrame.setText("Reference Frame")
        self.spinBoxRefFrame = QtWidgets.QSpinBox(self.widget)
        self.spinBoxRefFrame.setMaximum(999999)
        self.spinBoxRefFrame.setSingleStep(1)
        self.spinBoxRefFrame.setValue(0)
        self.spinBoxRefFrame.setObjectName("spinBoxRefFrame")

        # Now the layout : 4 Horizontals layouts
        self.Hlayout0 = QtWidgets.QHBoxLayout()
        self.Hlayout0.addWidget(self.textBrowserDescription)

        self.Hlayout1 = QtWidgets.QHBoxLayout()
        self.Hlayout1.addWidget(self.labelSelection)
        self.Hlayout1.addWidget(self.lineEditSelection)
        self.Hlayout1.addWidget(self.pushButtonShowAtoms)
        self.Hlayout1.addStretch()

        self.Hlayout2 = QtWidgets.QHBoxLayout()
        self.Hlayout2.addWidget(self.labelRefFrame)
        self.Hlayout2.addWidget(self.spinBoxRefFrame)
        self.Hlayout2.addStretch()

        self.gridLayout.addLayout(self.Hlayout0, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout1, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout2, 2, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2)
        # Now fill HTML Description
        self.textBrowserDescription.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600; text-decoration: underline;\">Self Alignement</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Align each frame of the trajectory on a particular frame (default : First one - 0 )</p>\n"
            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">AtomSelection</span> : atom selection for RMSD calculation</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Reference Frame</span> : Frame of reference (usually the first one). <span style=\" font-weight:600;\">Start at 0!</span></p>\n"
            "</body></html>")
