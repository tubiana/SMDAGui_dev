from .base import *

class HBonds(Analyses):
    def __init__(self, parent=None, mainWindows=None, numReplica=1):
        """
        Initialise the current analysis class.

        Args:
            parent (QtWidgets.QTreeWidgetItem): widget where this class belongs to (Tree widgets). This is needed to
                                                organise all the widgets analysis.
            mainWindows (core.MainWindow): Current main windows object, that contain needed functions for visualization
            numReplica (in): Replica number if we have several replicas.
        """
        super().__init__("HBonds", parent, mainWindows, numReplica)
        self.atomSelection = ""
        self.frameRef = 0
        self.widget = None
        self.init_widget()

        self.arguments = ["name", "selection1", "selection2", "freq", "excludeWaters", "sideChainOnly"]
        self.fig = []
        self.ax = []

        self.yAxisLabel = "Hbonds Count"
        self.xAxisLabel = "Frame"
        self.lineColor = "red"

        self.lineEditName.textChanged.connect(self.on_lineEditName_textChanged)
        self.lineEditSelection1.textChanged.connect(lambda: self.check_selection(self.lineEditSelection1))
        self.pushButtonShowAtoms1.clicked.connect(lambda: self.show_DataFrame(self.lineEditSelection1))
        self.lineEditSelection2.textChanged.connect(lambda: self.check_selection(self.lineEditSelection2))
        self.pushButtonShowAtoms2.clicked.connect(lambda: self.show_DataFrame(self.lineEditSelection2))
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
        print(f"HBOND {replica}")
        graphs = []
        ax, fig = self.graph_HBOND(resultsDF,
                                   self.parameters["name"],
                                   self.parameters["imgPath"][replica])
        graphs.append(self.store_figure(ax=ax, fig=fig))
        summedGraphPath = self.parameters["imgPath"][replica].split(".png")[0] + "_summed.png"
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
        count = pd.DataFrame({self.yAxisLabel: dat,
                              self.xAxisLabel: time})

        if len(count) > 100:
            count["Average"] = scipy.signal.savgol_filter(count[self.yAxisLabel], 21, 3)

        if not count.empty:
            ax, fig = self.graph_XY(count,
                                    self.__class__.__name__,
                                    self.parameters["name"],
                                    imgPath)

            return (ax, fig)
        else:
            return (None, None)

    def do_calculations(self, traj):
        """
        Main calculation function. It has to return a dataframe object with the results

        Args:
            traj (mdtraj.trajectory):  trajectory object

        Returns:
            results (pandas.DataFrame):  DataFrame with all the results
        """
        # filter with the selection

        if self.lineEditSelection1.text() == self.lineEditSelection2.text():
            selection = traj.top.select(self.lineEditSelection1.text())
            subtraj = traj.atom_slice(selection)
        else:
            sel1 = traj.top.select(self.lineEditSelection1.text())
            sel2 = traj.top.select(self.lineEditSelection2.text())
            # just a trick to save some times, the query will be the smallest group of atoms
            if len(sel1) >= len(sel2):
                query = sel2
            else:
                query = sel1
            contact = np.asarray(md.compute_neighbors(traj, 0.4, query, np.concatenate((sel1, sel2))))
            sel_U_sel2 = np.unique(np.concatenate(contact))
            subtraj = traj.atom_slice(sel_U_sel2)
            # Recalculate the atoms aindex because they will not be the same since the contact was made on a subset
            # of the trajectory
            subtrajAtomSelection1 = subtraj.top.select(self.lineEditSelection1.text())
            subtrajAtomSelection2 = subtraj.top.select(self.lineEditSelection2.text())



        hbondsAllFrames = md.geometry.hbond.wernet_nilsson(subtraj)

        # Delete intra-Hbonds if we are looking for Hbonds between 2 selections
        if self.lineEditSelection1.text() != self.lineEditSelection2.text():
            hbondsAllFramesTemp = []
            for frame in hbondsAllFrames:
                Hbonds_perframe = []
                for hbond in frame:
                    donor = hbond[0]
                    acceptor = hbond[2]
                    if donor in subtrajAtomSelection1 and acceptor in subtrajAtomSelection2:
                        Hbonds_perframe.append(hbond)
                    elif acceptor in subtrajAtomSelection1 and donor in subtrajAtomSelection2:
                        Hbonds_perframe.append(hbond)
                hbondsAllFramesTemp.append(Hbonds_perframe)
            hbondsAllFrames = np.asarray(hbondsAllFramesTemp)
            hbondsAllFramesTemp.clear()

        getLabel = lambda hbond: '%s -- %s' % (traj.topology.atom(hbond[0]), subtraj.topology.atom(hbond[2]))

        labelsAllFrames = []

        for hbonds in hbondsAllFrames:
            labels = []
            for hbond in hbonds:
                label = getLabel(hbond)
                labels.append(label)
            labelsAllFrames.append(labels)
        labelsAllFrames = np.array(labelsAllFrames)

        nFrames = len(labelsAllFrames)
        result = pd.DataFrame()
        for i in range(nFrames):
            for label in labelsAllFrames[i]:
                result.loc[label, i] = 1

        result = result.replace(np.NaN, 0)

        result["Freq"] = result.sum(axis=1) / traj.n_frames

        result = result.replace(np.NaN, 0)

        if subtraj.time.sum() < 0.000005 or subtraj.timestep == 1:
            time = list(range(traj.n_frames))
            self.xAxisLabel = "Frame"
        else:
            time = traj.time / 1000
            self.xAxisLabel = "Time (ns)"

        result.rename(columns=dict(zip(result.drop("Freq", axis=1).columns, time)))

        # self.resultsAll = result
        return result

    # def add_outPath_in_parameters(self, numReplica=None):
    #     """
    #     Overide add_outPath_in_parameters since for HBonds we have 2 graphics.
    #     This is to store imgPath and csvPath inside the parameter dict (used to load/save parameters)
    #     Note:
    #         No return, everything is saved in self.parameters
    #     Args:
    #         numReplica (int): replica number.
    #     """
    #     # Reset path in list.
    #     self.parameters["imgPath"] = []
    #     self.parameters["csvPath"] = []
    #
    #     if numReplica and numReplica > 1:
    #         for replica in range(numReplica):
    #             print(f"replica --- {replica}")
    #             strImgPath = "IMG/replica{}/{}_{}.png".format(replica, self.__class__.__name__, self.parameters["name"])
    #             strCsvPath = "CSV/replica{}/{}_{}.csv".format(replica, self.__class__.__name__, self.parameters["name"])
    #             self.parameters["imgPath"].append(strImgPath)
    #             self.parameters["csvPath"].append(strCsvPath)
    #     else:
    #         strImgPath = "IMG/{}_{}.png".format(self.__class__.__name__, self.parameters["name"])
    #         strCsvPath = "CSV/{}_{}.csv".format(self.__class__.__name__, self.parameters["name"])
    #         self.parameters["imgPath"].append(strImgPath)
    #         self.parameters["csvPath"].append(strCsvPath)

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
        self.parameters["freq"] = self.spinBoxFreq.value()
        self.parameters["excludeWaters"] = self.checkBoxExcludeWaters.isChecked()
        self.parameters["sideChainOnly"] = self.checkBoxSideChainOnly.isChecked()
        self.parameters["xAxisLabel"] = self.xAxisLabel

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
        self.lineEditSelection1.setText(self.parameters["selection1"])
        self.lineEditSelection2.setText(self.parameters["selection2"])
        self.spinBoxFreq.setValue(self.parameters["freq"])
        self.checkBoxExcludeWaters.setChecked(self.parameters["excludeWaters"])
        self.checkBoxSideChainOnly.setChecked(self.parameters["sideChainOnly"])
        self.xAxisLabel = self.parameters["xAxisLabel"]

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
        self.labelSelection1.setText("Atoms Selection 1")
        self.lineEditSelection1 = QtWidgets.QLineEdit(self.widget)
        self.lineEditSelection1.setObjectName("lineEditSelection1")
        self.pushButtonShowAtoms1 = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtoms1.setText("Show selected atoms")
        self.pushButtonShowAtoms1.setObjectName("pushButtonShowAtoms")

        self.labelSelection2 = QtWidgets.QLabel(self.widget)
        self.labelSelection2.setText("Atoms Selection 2")
        self.lineEditSelection2 = QtWidgets.QLineEdit(self.widget)
        self.lineEditSelection2.setObjectName("lineEditSelection2")
        self.pushButtonShowAtoms2 = QtWidgets.QPushButton(self.widget)
        self.pushButtonShowAtoms2.setText("Show selected atoms")
        self.pushButtonShowAtoms2.setObjectName("pushButtonShowAtoms")

        self.labelFreq = QtWidgets.QLabel(self.widget)
        self.labelFreq.setText("Cutoff Frequence")
        self.spinBoxFreq = QtWidgets.QDoubleSpinBox(self.widget)
        self.spinBoxFreq.setMaximum(1)
        self.spinBoxFreq.setSingleStep(0.01)
        self.spinBoxFreq.setValue(0.1)
        self.spinBoxFreq.setObjectName("spinBoxFreq")

        self.checkBoxExcludeWaters = QtWidgets.QCheckBox(self.widget)
        self.checkBoxExcludeWaters.setText("Exclude Waters ?")
        self.checkBoxExcludeWaters.setObjectName("checkBoxExcludeWaters")
        self.checkBoxExcludeWaters.setChecked(True)

        self.checkBoxSideChainOnly = QtWidgets.QCheckBox(self.widget)
        self.checkBoxSideChainOnly.setText("SideChain Only ? ?")
        self.checkBoxSideChainOnly.setObjectName("checkBoxSideChainOnly")
        self.checkBoxSideChainOnly.setChecked(True)

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

        self.Hlayout2bis = QtWidgets.QHBoxLayout()
        self.Hlayout2bis.addWidget(self.labelSelection2)
        self.Hlayout2bis.addWidget(self.lineEditSelection2)
        self.Hlayout2bis.addWidget(self.pushButtonShowAtoms2)
        self.Hlayout2bis.addStretch()

        self.Hlayout3 = QtWidgets.QHBoxLayout()
        self.Hlayout3.addWidget(self.labelFreq)
        self.Hlayout3.addWidget(self.spinBoxFreq)
        self.Hlayout3.addStretch()

        self.Hlayout4 = QtWidgets.QHBoxLayout()
        self.Hlayout4.addWidget(self.checkBoxExcludeWaters)
        self.Hlayout4.addStretch()

        self.Hlayout5 = QtWidgets.QHBoxLayout()
        self.Hlayout5.addWidget(self.checkBoxSideChainOnly)
        self.Hlayout5.addStretch()

        self.gridLayout.addLayout(self.Hlayout0, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout1, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout2, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout2bis, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout3, 4, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout4, 5, 0, 1, 1)
        self.gridLayout.addLayout(self.Hlayout5, 6, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2)
        # Now fill HTML Description
        self.textBrowserDescription.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600; text-decoration: underline;\">Hydrogen Bonds calculation</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Compute hydrogens bond within the selected atoms</p>\n"
            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Name</span> : Name used for graphics. Please use an <span style=\" font-weight:600;\">unique</span> name.</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">AtomSelection</span> : atom selection for atom group</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Freq</span> : Remove all Hbonds found with frequence bellow this cutoff</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Exclude Waters</span> : Exclude waters molecule in Hbonds analysis</p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline;\">Sidechain Only</span> : Use only residues side chain for Hbonds analysis</p></body></html>\n"
        )