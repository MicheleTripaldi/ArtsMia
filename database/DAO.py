from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """select *
                    from objects o
                """

        cursor.execute(query)
        for row in cursor:
            result.append(ArtObject(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(v1, v2): # per edges 1
        pass

    @staticmethod
    def getAllArchi(idMap):  # mi trova tutti gli archi
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """SELECT eo.object_id as nodo1, eo2.object_id as nodo2, COUNT(*) as weight 
                    FROM exhibition_objects eo ,exhibition_objects eo2 
                    WHERE eo.object_id < eo2.object_id 
                    and eo.exhibition_id = eo2.exhibition_id 
                    GROUP BY nodo1, nodo2"""

        cursor.execute(query)
        for row in cursor:
            result.append(Arco(idMap[row["nodo1"]], idMap[row["nodo2"]], row["weight"]))

        cursor.close()
        conn.close()
        return result


