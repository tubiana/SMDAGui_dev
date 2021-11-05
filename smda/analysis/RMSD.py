from .base import *
try:
    from numba import jit, prange
except:
    pass

#@jit(nopython=True, parallel=False, cache=False, nogil=True)
def calc_rmsd_2frames(ref, frame):
    """
    THIS FUNCTION IS OUT OF THE CLASS BECAUSE OF NUMBA
    RMSD calculation between a reference and a frame.
    This function is "jitted" for better performances
    """
    # #Loop seems faster with numba
    dist = np.zeros(len(frame))
    for atom in range(len(frame)):
        dist[atom] = ((ref[atom][0] - frame[atom][0]) ** 2 +
                      (ref[atom][1] - frame[atom][1]) ** 2 +
                      (ref[atom][2] - frame[atom][2]) ** 2)

    return (np.sqrt(dist.mean()))

def calc_rmsd_2frames_noopti(ref, frame):
    """
    THIS FUNCTION IS THE NON NUMBA OPTIMIZED OUT OF
    THE CLASS BECAUSE OF NUMBA RMSD calculation
    between a reference and a frame.
    """
    dist = ((ref - frame)**2).sum(axis=1)
    return (np.sqrt(dist.mean()))



class RMSD(Analyses):


    def __init__(self, parent=None, mainWindows=None, numReplica=1):
        """
        Initialise the current analysis class.

        Args:
            parent (QtWidgets.QTreeWidgetItem): widget where this class belongs to (Tree widgets). This is needed to
                                                organise all the widgets analysis.
            mainWindows (core.MainWindow): Current main windows object, that contain needed functions for visualization
            numReplica (in): Replica number if we have several replicas.
        """
        super().__init__("RMSD", parent, mainWindows, numReplica)

        self.atomSelection = ""
        self.frameRef = 0
        self.widget = None
        self.init_widget()

        self.arguments = ["name", "selection", "precentered", "frame"]
        # self.fig = None
        # self.ax = None
        self.yAxisLabel = "RMSD (A)"
        self.xAxisLabel = "Time (ns)"
        self.lineColor = "red"

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


        atomsel = traj.top.select(self.parameters["selection"])
        referenceFrame = self.parameters["frame"]
        subtraj = traj.atom_slice(atomsel, inplace=False)

        import time
        a = time.time()

        rmsd = np.zeros(subtraj.n_frames)

        try:
            calc_function = jit(nopython=True, parallel=False, cache=False, nogil=True)(calc_rmsd_2frames)
        except:
            calc_function = calc_rmsd_2frames_noopti

        for i in range(subtraj.n_frames):
            rmsd[i] = calc_function(subtraj.xyz[referenceFrame], subtraj.xyz[i])

        b = time.time()
        print(b-a)

        rmsdDF = pd.DataFrame({self.yAxisLabel: rmsd * 10,
                               self.xAxisLabel: traj.time / 1000})
        # self.result = rmsd
        # rmsdDF["Average"] = scipy.signal.savgol_filter(rmsdDF["RMSD (A)"], 21, 3)
        rmsdDF["Average"] = scipy.signal.savgol_filter(rmsdDF[self.yAxisLabel], 21, 3)
        return rmsdDF

    def loadFromDict(self, dictionnary):
        """
        Load all parameters from dict and then inject them inside PyQt widgets.

        Args:
            dictionnary (dict): dictionnary with all the parameters.
        """
        self.parameters = dictionnary

        self.lineEditName.setText(self.parameters["name"])
        self.lineEditSelection.setText(self.parameters["selection"])
        self.spinBoxRefFrame.setValue(self.parameters["frame"])
        self.checkBoxPrecentered.setChecked(self.parameters["precentered"])

        self.restore_graphs()

    def retrieve_parameters(self, numReplica=None):
        """
        Get all parameters from PyQt widgets for this analysis class and save them into a dictionnary that will be used
        to save the parameters in a json file.

        Args:
            numReplica: Replica number. Not used for now.
        """
        self.parameters["name"] = self.lineEditName.text()
        self.parameters["selection"] = self.lineEditSelection.text()
        self.parameters["frame"] = self.spinBoxRefFrame.value()
        self.parameters["precentered"] = self.checkBoxPrecentered.isChecked()

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
        self.pushButtonShowAtoms.setText("showSelectedAtoms")
        self.pushButtonShowAtoms.setObjectName("pushButtonShowAtoms")

        self.labelRefFrame = QtWidgets.QLabel(self.widget)
        self.labelRefFrame.setText("Reference Frame")
        self.spinBoxRefFrame = QtWidgets.QSpinBox(self.widget)
        self.spinBoxRefFrame.setMaximum(999999)
        self.spinBoxRefFrame.setValue(0)
        self.spinBoxRefFrame.setSingleStep(1)
        self.spinBoxRefFrame.setObjectName("spinBoxRefFrame")

        self.checkBoxPrecentered = QtWidgets.QCheckBox(self.widget)
        self.checkBoxPrecentered.setText("Precentered ?")
        self.checkBoxPrecentered.setObjectName("checkBoxPrecentered")
        self.checkBoxPrecentered.setChecked(False)

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
        self.Hlayout3.addWidget(self.labelRefFrame)
        self.Hlayout3.addWidget(self.spinBoxRefFrame)
        self.Hlayout3.addStretch()

        self.Hlayout4 = QtWidgets.QHBoxLayout()
        self.Hlayout4.addWidget(self.checkBoxPrecentered)
        self.Hlayout4.addStretch()

        self.gridLayout.addLayout(self.Hlayout0, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout1, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout2, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout3, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout4, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2)
        # Now fill HTML Description
        self.textBrowserDescription.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600; text-decoration: underline;\">RMSD</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Compute RMSD of all conformations in target to a reference conformation. Note, this will center the conformations in place.</p>\n"
            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Name</span> : Name used for graphics. Please use an <span style=\" font-weight:600;\">unique</span> name.</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">AtomSelection</span> : atom selection for RMSD calculation</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Reference Frame</span> : Frame of reference (usually the first one). <span style=\" font-weight:600;\">Start at 0!</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Precentered</span> : Asume that the protein is already precentered</p></body></html>")
