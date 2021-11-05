from .base import *

class TRRMSF(Analyses):
    def __init__(self, parent=None, mainWindows=None, numReplica=1):
        """
        Initialise the current analysis class.

        Args:
            parent (QtWidgets.QTreeWidgetItem): widget where this class belongs to (Tree widgets). This is needed to
                                                organise all the widgets analysis.
            mainWindows (core.MainWindow): Current main windows object, that contain needed functions for visualization
            numReplica (in): Replica number if we have several replicas.
        """
        super().__init__("TRRMSF", parent, mainWindows, numReplica)
        self.atomSelection = ""
        self.frameRef = 0
        self.widget = None
        self.init_widget()
        self.arguments = ["name", "selection", "alignement"]
        #self.fig = None
        #self.ax = None
        self.yAxisLabel = "RMSF (A)"
        self.xAxisLabel = "Residue"
        self.lineColor = "blue"

        self.lineEditName.textChanged.connect(self.on_lineEditName_textChanged)
        self.lineEditSelection.textChanged.connect(lambda: self.check_selection(self.lineEditSelection))
        self.pushButtonShowAtoms.clicked.connect(lambda: self.show_DataFrame(self.lineEditSelection))


    def local_RMSF(self, subtraj, average_coords = None):
        """
                Main calculation function. It has to return a dataframe object with the results
                Args:
                    traj (mdtraj.trajectory):  trajectory object
                    average_coords (np.array): average coords or None if the average coord is local.

                Returns:
                    rmsfDF (pandas.DataFrame):  DataFrame with all the results
        """
        if type(average_coords) == type(None):
            average_coords = np.mean(subtraj.xyz, axis=0)

        rmsf = np.sqrt(3 * np.mean((subtraj.xyz[:, :, :] - average_coords) ** 2, axis=(0, 2)))

        if self.checkBoxByResidue.isChecked():
            table, bonds = subtraj.top.to_dataframe()

            table["RMSF"] = rmsf
            rmsfByRes = table.groupby("resSeq").apply(lambda x: x["RMSF"].mean())

            rmsfDF = pd.DataFrame({self.xAxisLabel: list(rmsfByRes.index),
                                   self.yAxisLabel: rmsfByRes.values})
        else:
            rmsfDF = pd.DataFrame({self.xAxisLabel: [x.serial for x in subtraj.top.atoms],
                                   self.yAxisLabel: rmsf})

        # rmsfDF["Average"] = scipy.signal.savgol_filter(rmsf[self.yAxisLabel], 2, 3)
        return rmsfDF.set_index(self.xAxisLabel)

    def chunk_traj(self, traj, window):
        return ([traj[i:i + window] for i in range(0, len(traj), window)])


    def do_calculations(self, traj, average_coords = None):
        """
        Main calculation function. It has to return a dataframe object with the results
        Args:
            traj (mdtraj.trajectory):  trajectory object
            average_coords (np.array): average coords or None if the average coord is local.

        Returns:
            rmsfDF (pandas.DataFrame):  DataFrame with all the results
        """
        # Extract trajectory for time optimisation
        selected_atoms = self.improvedSelection(traj, self.parameters["selection"])

        subtraj = traj.atom_slice(selected_atoms)
        if self.checkBoxAlignement.isChecked():
            subtraj.superpose(subtraj)

        if self.checkBoxAverage.isChecked():
            average_coords = np.mean(subtraj.xyz, axis=0)
        else:
            average_coords = None


        #TAKE WINDOWS
        window = self.spinBoxWindow.value()
        chunked_traj = self.chunk_traj(subtraj, window)
        rmsfDF = pd.concat([self.local_RMSF(t, average_coords) for t in chunked_traj], axis=1)
        labels = list(range(0,len(traj), window))
        rmsfDF.columns=labels
        return rmsfDF

    def generate_graphs(self, resultsDF, replica=0):
        """
        Default function to generate XY graphs (most of graph types)
        :param resultsDF: Pandas DataFrame
        :return:
        """

        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        X = []
        Y = []
        Z = []
        nchunk=resultsDF.shape[1]
        for i in range(nchunk):
            X.append([i]*len([resultsDF.iloc[:,i]]))
            Y.append(list(resultsDF.index))
            Z.append(resultsDF.iloc[:,i].values)

        X = np.array(X)
        Y = np.array(Y)
        Z = np.array(Z)
        minval = Z.min()
        maxval = Z.max()

        # for i in range(len(X)):
        #     ax.plot(X[i],Y[i],Z[i])
        ax.plot_surface(X,Y,Z, cmap='coolwarm')



        self.figures.append([self.store_figure(ax=ax, fig=fig)])  # In a list because we will iterate over figures

    def retrieve_parameters(self, replica=None):
        """
        Get all parameters from PyQt widgets for this analysis class and save them into a dictionnary that will be used
        to save the parameters in a json file.

        Args:
            numReplica: Replica number. Not used for now.
        """
        if self.checkBoxByResidue.isChecked():
            self.xAxisLabel = "Residue"
        else:
            self.xAxisLabel = "Atom"

        self.parameters["xAxisLabel"] = self.xAxisLabel
        self.parameters["name"] = self.lineEditName.text()
        self.parameters["selection"] = self.lineEditSelection.text()
        self.parameters["alignement"] = self.checkBoxAlignement.isChecked()
        self.parameters["byResidue"] = self.checkBoxByResidue.isChecked()
        self.parameters["frame"] = self.spinBoxRefFrame.value()


    def loadFromDict(self, dictionnary):
        """
        Load all parameters from dict and then inject them inside PyQt widgets.

        Args:
            dictionnary (dict): dictionnary with all the parameters.
        """
        self.parameters = dictionnary

        self.lineEditName.setText(self.parameters["name"])
        self.lineEditSelection.setText(self.parameters["selection"])
        self.checkBoxAlignement.setChecked(self.parameters["alignement"])
        self.checkBoxByResidue.setChecked(self.parameters["byResidue"])
        self.spinBoxRefFrame.setValue(self.parameters["frame"])
        self.xAxisLabel = self.parameters["xAxisLabel"]

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
        self.pushButtonShowAtoms = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtoms.setText("Show selected atoms")
        self.pushButtonShowAtoms.setObjectName("pushButtonShowAtoms")


        self.checkBoxByResidue = QtWidgets.QCheckBox(self.widget)
        self.checkBoxByResidue.setText("Group by residues ?")
        self.checkBoxByResidue.setObjectName("checkBoxByResidue")
        self.checkBoxByResidue.setChecked(True)



        self.checkBoxAlignement = QtWidgets.QCheckBox(self.widget)
        self.checkBoxAlignement.setText("With Alignement ?")
        self.checkBoxAlignement.setObjectName("checkBoxAlignement")
        self.checkBoxAlignement.setChecked(True)


        self.checkBoxAverage = QtWidgets.QCheckBox(self.widget)
        self.checkBoxAverage.setText("whole trajectory average ?")
        self.checkBoxAverage.setObjectName("checkBoxAverage")
        self.checkBoxAverage.setChecked(True)

        self.labelWindow = QtWidgets.QLabel(self.widget)
        self.labelWindow.setText("Window (Number of frames)")
        self.spinBoxWindow = QtWidgets.QSpinBox(self.widget)
        self.spinBoxWindow.setMaximum(999999)
        self.spinBoxWindow.setValue(20)
        self.spinBoxWindow.setSingleStep(1)
        self.spinBoxWindow.setObjectName("spinBoxWindow")

        self.labelRefFrame = QtWidgets.QLabel(self.widget)
        self.labelRefFrame.setText("Reference Frame")
        self.spinBoxRefFrame = QtWidgets.QSpinBox(self.widget)
        self.spinBoxRefFrame.setMaximum(999999)
        self.spinBoxRefFrame.setValue(0)
        self.spinBoxRefFrame.setObjectName("spinBoxRefFrame")

        # Now the layout : 5 Horizontals layouts

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
        self.Hlayout4.addWidget(self.checkBoxAlignement)
        self.Hlayout4.addWidget(self.labelWindow)
        self.Hlayout4.addWidget(self.spinBoxWindow)
        self.Hlayout4.addStretch()

        self.Hlayout5 = QtWidgets.QHBoxLayout()
        self.Hlayout5.addWidget(self.checkBoxAverage)
        self.Hlayout5.addWidget(self.checkBoxByResidue)
        self.Hlayout5.addStretch()

        self.gridLayout.addLayout(self.Hlayout0, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout1, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout2, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout5, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout3, 4, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout4, 5, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2)
        # Now fill HTML Description
        self.textBrowserDescription.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600; text-decoration: underline;\">Tr-RMSF (Time resolved RMSF)</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Split the trajectory in mupltiple sub-trajectory of a specific size (window) and compute RMSF values in each subtrajectory. Note, this will center the conformations in place.</p>\n"
            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Name</span> : Name used for graphics. Please use an <span style=\" font-weight:600;\">unique</span> name.</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">AtomSelection</span> : atom selection for RMSD calculation</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Alignement</span> : Perform alignement on selection before RMSF calculation</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Group by residue</span> : instead of showing RMSF for each atoms, calculate the average RMSF for each residues</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Whole trajectory average</span> : Use one referenc for all windows : the average position of the trajectory. if unitcked, an average position will be computed for each windows</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Window size</span> : size of the windows (subtrajectory).</p></body></html>\n"
        )
