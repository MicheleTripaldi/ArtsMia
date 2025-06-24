import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model



    def handleCerca(self, e):
        pass




    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"il grafo ha: {self._model.getNumNodes()} nodi"))
        self._view.txt_result.controls.append(ft.Text(f"il grafo ha: {self._model.getNumEdges()} archi"))

        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False

        self._view.update_page()

    def handleCompConnessa(self,e):
        idInput = self._view._txtIdOggetto.value

        if idInput is None or idInput == "":
            self._view.create_alert("No idInput selected")
            return

        # converto l'idInput in intero
        try:
            idInput = int(idInput)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(" idInput non valida"))
            self._view.update_page()
            return

        connessione = self._model.getInfoConnessa(idInput)
        self._view.txt_result.controls.append(ft.Text(f"Size connessa: {connessione}"))
        self._view.update_page()



