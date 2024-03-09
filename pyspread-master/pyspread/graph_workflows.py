
from contextlib import contextmanager



class GraphWorkflows:

    cell2dialog = {}
    def __init__(self, graph_window):
        self.graph_window = graph_window

    def update(self):

        self.graph_window.update()

    def new_modele(self):
       self.graph_window.modeleDialog()
###FONCTION EXEMPLE