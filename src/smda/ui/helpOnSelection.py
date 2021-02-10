from PyQt5 import QtCore, QtWidgets


class HelpSelection:
    def __init__(self):
        # QtWidgets.QWidget.__init__(self, parent)

        # self.helpSelectionWindow = QtWidgets.QWidget()
        self.helpSelectionWindow = QtWidgets.QMainWindow()
        self.helpSelectionWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.helpSelectionWindow.setWindowTitle("Atoms Selection Syntax")
        self.helpSelectionWindow.resize(800, 850)

        self.centralWidget = QtWidgets.QWidget(self.helpSelectionWindow)

        self.grid = QtWidgets.QGridLayout(self.centralWidget)
        textBrowserHelpSelection = QtWidgets.QTextBrowser(self.centralWidget)
        self.grid.addWidget(textBrowserHelpSelection, 0, 0, 1, 1)
        self.helpSelectionWindow.setCentralWidget(self.centralWidget)

        textBrowserHelpSelection.setHtml(
            '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
            '<p align="center" style=" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><a name="atom-selection-dsl"></a><span style=" font-size:14pt; font-weight:600;">H</span><span style=" font-size:14pt; font-weight:600;">elp on Atom Selection </span></p>\n'
            '<p style=" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><a name="introduction"></a><span style=" font-size:12pt; font-weight:600;">I</span><span style=" font-size:12pt; font-weight:600;">ntroduction</span></p>\n'
            '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">The selection syntax is based on MDTRAJ Atom Selection DSL (since the analysys engine is MDTRAJ).</span><span style=" font-size:8pt; text-decoration: underline;">Most of this help is taken of MDTRAJ Atom Selection DSL webpage</span><span style=" font-size:8pt;">. For complete details, please read the Atom Selection DSL at </span><a href="http://mdtraj.org/latest/atom_selection.html"><span style=" font-size:8pt; text-decoration: underline; color:#0000ff;">http://mdtraj.org/latest/atom_selection.html</span></a><span style=" font-size:8pt;">.</span></p>\n'
            '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">MDTaj’s </span><a href="analysis.html#analysis"><span style=" font-size:8pt; font-style:italic; text-decoration: underline; color:#0000ff;">trajectory analysis</span></a><span style=" font-size:8pt;"> functions use 0-based arraysof “atom indices” to refer to subsets or groups of atoms in trajectories. Togenerate these index arrays, MDTraj includes a powerful text-based atomselection domain-specific language operating on the </span><span style=" font-family:\'Courier New\'; font-size:8pt;">Topology</span><span style=" font-size:8pt;">. Thefollowing are all valid selection queries:</span></p>\n'
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:8pt;\">top.select(&quot;water&quot;)top.select(&quot;resSeq 35&quot;)top.select(&quot;water and name O&quot;)top.select(&quot;mass 5.5 to 20&quot;)top.select(&quot;resname =~ 'C.*'&quot;)top.select(&quot;protein and (backbone or resname ALA)&quot;)</span></p>\n"
            '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">These queries return a numpy array of integers containing the indices of thematching atoms. Equivalent python code for every selection expressioncan be generated using </span><span style=" font-family:\'Courier New\'; font-size:8pt;">Topology.select_expression</span><span style=" font-size:8pt;">.</span></p>\n'
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:8pt;\">&gt;&gt;&gt; top.select_expression(&quot;water and name O&quot;)&quot;[atom.index for atom in topology.atoms if (atom.residue.is_water and (atom.name == 'O'))]&quot;</span></p>\n"
            '<p style=" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><a name="keywords-and-grammar"></a><span style=" font-size:11pt; font-weight:600;">K</span><span style=" font-size:11pt; font-weight:600;">eywords and Grammar</span></p>\n'
            '<p style=" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><a name="keywords"></a><span style=" font-size:10pt; font-weight:600;">K</span><span style=" font-size:10pt; font-weight:600;">eywords</span></p>\n'
            '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">MDTraj recognizes the following keywords. Each keyword maps directly to aproperty on the MDTraj topology object’s </span><span style=" font-family:\'Courier New\'; font-size:8pt;">Atom</span><span style=" font-size:8pt;">/</span><span style=" font-family:\'Courier New\'; font-size:8pt;">Residue</span><span style=" font-size:8pt;">/</span><span style=" font-family:\'Courier New\'; font-size:8pt;">Chain</span><span style=" font-size:8pt;"> tree.</span></p>\n'
            '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;"><br /></p>\n'
            '<table border="1" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;" cellspacing="2" cellpadding="0">\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Keyword</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Synonyms</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Type</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Description</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">all</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">everything</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">bool</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Matches everything</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">none</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">nothing</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">bool</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Matches nothing</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">backbone</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">is_backbone</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">bool</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Whether atom is in the backbone of a protein residue</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">within</span></p></td>\n'
            '<td style=" vertical-align:top;"></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">float</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Select atoms within X agstrom of a selection</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">sidechain</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">is_sidechain</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">bool</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Whether atom is in the sidechain of a protein residue</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">protein</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">is_protein</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">bool</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Whether atom is part of a protein residue</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">water</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">is_water</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">waters</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">bool</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Whether atom is part of a water residue</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">name</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;"> </span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">str</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Atom name</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">index</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;"> </span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">int</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Atom index</span><span style=" font-size:8pt; font-weight:600;"> (0-based)</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">n_bonds</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;"> </span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">int</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Number of bonds this atom participates in</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">type</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">element</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">symbol</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">str</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">1 or 2-letter chemical symbols from the periodic table</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">mass</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;"> </span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">float</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Element atomic mass (daltons)</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">residue</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">resSeq</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">int</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Residue Sequence record (generally 1-based, but depends on topology)</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">resid</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">resi</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">int</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Residue index </span><span style=" font-size:8pt; font-weight:600;">(0-based)</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">resname</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">resn</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">str</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Residue name</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">rescode</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">code</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">resc`</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">str</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">1-letter residue code</span></p></td></tr>\n'
            "<tr>\n"
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">chainid</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;"> </span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;">int</span></p></td>\n'
            '<td style=" vertical-align:top;">\n'
            '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Chain index </span><span style=" font-size:8pt; font-weight:600;">(0-based)</span></p></td></tr></table>\n'
            '<p style=" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><a name="literals"></a><span style=" font-size:10pt; font-weight:600;">D</span><span style=" font-size:10pt; font-weight:600;">istance (new in SMDA!)</span></p>\n'
            '<p style=" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">You can select atoms at X angstrom of distance from  a selection with the syntax </span><span style=" font-family:\'Courier New\'; font-size:8pt; vertical-align:top;">within &lt;x&gt; of &lt;selection&gt;.</span><span style=" font-size:8pt;"> The distance </span><span style=" font-family:\'Courier New\'; font-size:8pt; vertical-align:top;">&lt;x&gt;</span><span style=" font-size:8pt;">  is exprimed in agrom.<br />example : </span></p>\n'
            '<p style=" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt; vertical-align:top;">within 5 of resname LIG </span><span style=" font-size:8pt;">will select all atoms less than 5 angstrom of the residue LIG</span></p>\n'
            '<p style=" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><a name="literals"></a><span style=" font-size:10pt; font-weight:600;">L</span><span style=" font-size:10pt; font-weight:600;">iterals</span></p>\n'
            '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Integer, floating point, and string literals are also parsed. Both single-quoted,strings, double-quoted strings, and bare words are also parsed as stringliterals.</span></p>\n'
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:8pt;\"># The following queries are equivalenttop.select(&quot;symbol == O&quot;)top.select(&quot;symbol == 'O'&quot;)top.select('symbol == &quot;O&quot;')</span></p>\n"
            '<p style=" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><a name="operators"></a><span style=" font-size:10pt; font-weight:600;">O</span><span style=" font-size:10pt; font-weight:600;">perators</span></p>\n'
            '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Standard boolean operations (</span><span style=" font-family:\'Courier New\'; font-size:8pt;">and</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">or</span><span style=" font-size:8pt;">, and </span><span style=" font-family:\'Courier New\'; font-size:8pt;">not</span><span style=" font-size:8pt;">) as well as theirC-style aliases (</span><span style=" font-family:\'Courier New\'; font-size:8pt;">&amp;&amp;</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">||</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">!</span><span style=" font-size:8pt;">) are supported. The expected logicaloperators (</span><span style=" font-family:\'Courier New\'; font-size:8pt;">&lt;</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">&lt;=</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">==</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">!=</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">&gt;=</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">&gt;</span><span style=" font-size:8pt;">) are also available, asalong with their FORTRAN-style synonyms (</span><span style=" font-family:\'Courier New\'; font-size:8pt;">lt</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">le</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">eq</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">ne</span><span style=" font-size:8pt;">,</span><span style=" font-family:\'Courier New\'; font-size:8pt;">ge</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">gt</span><span style=" font-size:8pt;">).</span></p>\n'
            '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">A regular-expression matching operator, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">=~</span><span style=" font-size:8pt;">, is available. For example, tomatch any of the names </span><span style=" font-family:\'Courier New\'; font-size:8pt;">\'C1\'</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">\'C2\'</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">\'C3\'</span><span style=" font-size:8pt;">, </span><span style=" font-family:\'Courier New\'; font-size:8pt;">\'C4\'</span><span style=" font-size:8pt;">, you can use thefollowing query. The regular expression syntax is just the </span><a href="https://docs.python.org/3/library/re.html#regular-expression-syntax"><span style=" font-size:8pt; text-decoration: underline; color:#0000ff;">native python Regexsyntax</span></a></p>\n'
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:8pt;\">top.select(&quot;name =~ 'C[1-4]'&quot;)</span></p>\n"
            '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">An implicit equality relation is implied between adjacent expressions</span></p>\n'
            '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;"># The following queries are equivalenttop.select(&quot;resid 35&quot;)top.select(&quot;resid == 35&quot;)</span></p>\n'
            '<p style=" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><a name="range-queries"></a><span style=" font-size:10pt; font-weight:600;">R</span><span style=" font-size:10pt; font-weight:600;">ange queries</span></p>\n'
            '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Range queries are also supported. The range condition is an expression of theform </span><span style=" font-family:\'Courier New\'; font-size:8pt;">&lt;expression&gt; &lt;low&gt; to &lt;high&gt;</span><span style=" font-size:8pt;">, which resolves to </span><span style=" font-family:\'Courier New\'; font-size:8pt;">&lt;low&gt; &lt;= &lt;expression&gt; &lt;= &lt;high&gt;</span><span style=" font-size:8pt;">.For example</span></p>\n'
            '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Courier New\'; font-size:8pt;"># The following queries are equivalenttop.select(&quot;resid 10 to 30&quot;)top.select(&quot;(10 &lt;= resid) and (resid &lt;= 30)&quot;)</span></p>\n'
            '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>'
        )

        self.helpSelectionWindow.show()
