import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self,e):
        self._view.txt_result.controls.clear()
        anno1 = self._view._ddAnno1.value
        anno2 = self._view._ddAnno2.value
        if anno1 is None:
            self._view.txt_result.controls.append(ft.Text("Inserire il primo anno", color="red"))
            self._view.update_page()
            return
        if anno2 is None:
            self._view.txt_result.controls.append(ft.Text("Inserire il secondo anno", color="red"))
            self._view.update_page()
            return
        try:
            anno1 = int(anno1)
            anno2 = int(anno2)
        except:
            self._view.txt_result.controls.append(ft.Text("Inserire anni validi", color="red"))
            self._view.update_page()
            return
        if anno1 > anno2:
            self._view.txt_result.controls.append(ft.Text("Inserire anni crescenti", color="red"))
            self._view.update_page()
            return

        self._model.creaGrafo(anno1, anno2)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente crato:", color="green"))
        n, m = self._model.dimGrafo()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {m}"))
        self._view._btnstampa.disabled = False
        self._view._btnCerca.disabled = False
        self._view.update_page()




    def handleDettagli(self, e):
        maggiori = self._model.archiMaggiori()
        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore:", color="green"))
        for a, b, w in maggiori:
            self._view.txt_result.controls.append(ft.Text(f"{a} -> {b} ({w})"))
        comp = self._model.compConnesse()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {comp[0]} componenti connesse:", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Componente più grande ({len(comp[1])} nodi):", color="green"))
        for c in comp[1]:
            self._view.txt_result.controls.append(ft.Text(f"{c}"))
        self._view.update_page()
        self._view.txt_result.controls.append(ft.Text("Componente connessa in ordine decrescente:", color="green"))
        for c in comp[2]:
            self._view.txt_result.controls.append(ft.Text(f"{c[0]} (grado={c[1]})"))
        self._view.update_page()

    def handleCerca(self, e):
        k = self._view._txtInK.value
        if k is None or k == "":
            self._view.txt_result.controls.append(ft.Text(f"Inserire un numero di piloti", color="red"))
            self._view.update_page()
            return
        try:
            k = int(k)
        except:
            self._view.txt_result.controls.append(ft.Text(f"Inserire un numero intero di piloti", color="red"))
            self._view.update_page()
            return

        if k < 0:
            self._view.txt_result.controls.append(ft.Text(f"Inserire un numero positivo di piloti", color="red"))
            self._view.update_page()
            return

        res = self._model.cercaPiloti(k)
        self._view.txt_result.controls.append(ft.Text(f"Trovato range minimo di {res[1]} anni ({res[2]}-{res[3]})", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Piloti compresi:", color="green"))
        for p in res[0]:
            self._view.txt_result.controls.append(ft.Text(f"{p} - {p.age}"))

        self._view.update_page()



    def fillDDAnni(self):
        anni = self._model.getAnni()
        for a in anni:
            self._view._ddAnno1.options.append(ft.dropdown.Option(a))
            self._view._ddAnno2.options.append(ft.dropdown.Option(a))

