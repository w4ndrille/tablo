
from contextlib import contextmanager
from PyQt6.QtWidgets import QErrorMessage


class GraphWorkflows:

    cell2dialog = {}
    def __init__(self, graph_window):
        self.graph_window = graph_window

    def update(self):
        self.graph_window.update()

    def new_modele(self):
       self.graph_window.modeleDialog()

    def auto_evaluate(self):
        #Handle error du to no data
        if not self.graph_window.graph.auto_evaluate():
            QErrorMessage(self.graph_window.graph).showMessage("Erreur d'évaluation : Aucune donnée à évaluer")


###FONCTION EXEMPLE