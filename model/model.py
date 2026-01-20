import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.id_map = {}
        self.artist_genre_map = {}

        self.artists_with_min_albums_list= []
        self._artists_list = []
        self.load_all_artists()


    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        self.artists_with_min_albums_list = DAO.get_artists_with_min_albums(min_albums)

        self.id_map = {a.id: a for a in self.artists_with_min_albums_list}  # dizionario con chiave: id artist e valore: oggetto Artist

    def load_artists_genre(self):
        self.artist_genre_map = DAO.get_artist_genre_map(self.artists_with_min_albums_list)  # mappa artista -> generi


    def build_graph(self):
        self._graph.clear()

        self._graph.add_nodes_from(self.artists_with_min_albums_list)

        # creo gli archi
        for i, a1 in enumerate(self.artists_with_min_albums_list):  # prende l'artista a1 in posizione i
            for a2 in self.artists_with_min_albums_list[i + 1:]:  # prende gli artisti dopo a1
                if self.artist_genre_map[a1] & self.artist_genre_map[a2]:
                    #peso= numero di generi in comune
                    dict=self.artist_genre_map[a1] & self.artist_genre_map[a2]
                    lista=list(dict)
                    peso= len(lista)
                    self._graph.add_edge(a1, a2, weight=peso)

    def artisti_connessi(self, artista):
        if artista not in self._graph:  # verifico che l'artista sia un nodo del grafo
            return []
        return list(nx.node_connected_component(self._graph, artista))


    def cerca_cammino_da_artista(self, min_durata, max_num_artisti):
        pass