from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:
    #commento di prova
    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artists_with_min_albums(n_alb):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT ar.id, ar.name
                FROM artist ar, album al
                WHERE ar.id = al.artist_id
                GROUP BY ar.id, ar.name
                HAVING COUNT(al.id) >= %s
                """

        try:
            cursor.execute(query, (n_alb,))
            for row in cursor:
                result.append(Artist(row['id'], row['name']))

        except Exception as e:
            print("Errore durante la query artisti")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista di oggetti Artisti connumero di album maggiore o uguale di n_album passato come parametro

    @staticmethod
    def get_artist_genre_map(artists): #artist è una lista di oggetti Artist
        cnx = DBConnect.get_connection()
        result = {a: set() for a in artists}  # dizionario con chiave: oggetto artista e valore: insieme vuoto
        # il set servirà per memorizzare i generi delle canzoni(senza duplicati)
        artists_ids = tuple(a.id for a in artists)  # estrae gli id degli artisti e li mette in una tupla(lista immutabile)
        if not artists_ids:
            return result

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = f"""
                SELECT a.artist_id, t.genre_id
                FROM track t, album a
                WHERE t.album_id = a.id AND a.artist_id IN {artists_ids}
                """

        try:
            cursor.execute(query)
            for row in cursor:
                artist = next((a for a in artists if a.id == row['artist_id']), None)
                # cerca nella lista artists l'oggetto artist con id uguale a album_id, se non lo trova restituisce none
                if artist:
                    result[artist].add(row['genre_id'])  # aggiunge il nome del genere al set dell’artista

        except Exception as e:
            print("Errore durante la query artist genre map")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # dizionario con chiave: oggetto Artist e valore: set di nomi dei generi delle canzoni di quell'artista
        # indica i generi dei brani di ogni artista