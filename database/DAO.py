from database.DB_connect import DBConnect
from model.driver import Driver


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPiloti(anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select d.* from results re, races ra, drivers d  where re.`position` is not null
                and ra.raceId = re.raceId and d.driverId = re.driverId  and ra.`year`  >= %s and  ra.`year`  <= %s"""

        cursor.execute(query, (anno1, anno2))

        for row in cursor:
            results.append(Driver(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select re1.driverId as d1, re2.driverId as d2, count(*) as s from results re1, results re2, races ra 
                    where re1.`position` is not null and re2.`position` is not null
                    and ra.raceId = re1.raceId and ra.`year`  >= %s and  ra.`year`  <= %s
                    and re1.raceId = re2.raceId and re1.driverId < re2.driverId and re1.constructorId = re2.constructorId 
                    group by re1.driverId, re2.driverId """

        cursor.execute(query, (anno1, anno2))

        for row in cursor:
            results.append((row["d1"], row["d2"], row["s"]))

        cursor.close()
        conn.close()
        return results


