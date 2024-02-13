
from contextlib import contextmanager



class GraphWorkflows:

    cell2dialog = {}

    def __init__(self, graph_window):
        self.graph_window = graph_window
    @contextmanager
    def add_cell(self):
        self.graph_window.settings.changed_since_save = False
###FONCTION EXEMPLE