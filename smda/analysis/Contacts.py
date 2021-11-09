from .base import *

class Contacts(Analyses):
    def __init__(self, parent=None, mainWindows=None, numReplica=1):
        super().__init__("Contacts", parent, mainWindows, numReplica)

    # 1. md.compute_contacts()
    # 2. md.geometry.squareform()
    # 3. animate
    # 4. Save as gif.