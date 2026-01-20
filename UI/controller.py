import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            min_album = int(self._view.txtNumAlbumMin.value)
        except ValueError:
            self._view.show_alert("Inserire una numero valido")
            return

        self._model.load_artists_with_min_albums(min_album)
        self._model.load_artists_genre()
        self._model.build_graph()

        # aggiorna dropdown artista
        self._view.ddArtist.options = [ft.dropdown.Option(a.name) for a in self._model.artists_with_min_albums_list]

        # aggiorno view
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo creato: {len(self._model._graph.nodes)} nodi(artisti), {len(self._model._graph.edges)} archi")
        )
        self._view.ddArtist.disabled= False
        self._view.update_page()

    def get_selected_artist(self, e):
        """ Handler per gestire la selezione dell'artista dal dropdown """""

        name = e.control.value
        self._selected_artist = next((a for a in self._model.artists_with_min_albums_list if a.name == name), None)
        self._view.btnArtistsConnected.disabled = False

        self._view.update_page()

    def handle_connected_artists(self, e):
        if not self._selected_artist:
            self._view.show_alert("Selezionare un artista")
            return

        component = self._model.artisti_connessi(self._selected_artist)
        #peso_arco =

        # aggiorno view
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text("Artisti direttamente collegati all'artista")
        )
        for c in component:
            self._view.lista_visualizzazione_2.controls.append(
                ft.Text(f"{c.id}, {c.name} - Numero di generi in comune: {self._model._graph[self._selected_artist][c]['weight']}")
            )
        self._view.update_page()


    def handle_cammino(self, e):
        try:
            min_durata = float(self._view.txtMinDuration.value)
        except ValueError:
            self._view.show_alert("Inserire una numero valido")
            return

        try:
            max_num_artisti= int(self._view.txtMaxArtists.value)
        except ValueError:
            self._view.show_alert("Inserire una numero valido")
            return


        self._view.update_page()
