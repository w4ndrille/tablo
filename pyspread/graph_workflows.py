
from contextlib import contextmanager
from PyQt6.QtWidgets import QErrorMessage


class GraphWorkflows:


    def __init__(self, graph_window):
        self.parent = graph_window

    def update(self):
        self.parent.parent.workflows.new_window(self.parent.graph.figs,True)
        self.parent.close()
        self.parent = None

    def new_modele(self):
       self.parent.modeleDialog()

    def delete_dialog(self):
        self.parent.deleteDialog()

    def auto_evaluate(self):
        #Handle error du to no data
        if not self.parent.graph.auto_evaluate():
            QErrorMessage(self.parent.graph).showMessage("Erreur d'évaluation : Aucune donnée à évaluer")


###FONCTION EXEMPLE