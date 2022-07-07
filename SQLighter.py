import sqlite3
from datetime import datetime

# This class is to make changes in a database, gives a current database info.

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_all_scores(self):
        with self.connection:
            base = self.cursor.execute('SELECT name,score,location,time FROM scores').fetchall()
            res = []
            for row in base :
                res.append(f'{row[0]} - {row[1]} балл(-ов). В последний раз он(а) убирал(а) {row[3]} {row[2]} ')
            return res

    def up_score(self, chat_id, points, place):

        current_date = str(datetime.now().date())[-2:]+'.'+str(datetime.now().date())[-5:-3]

        with self.connection:
            base = self.cursor.execute(f'SELECT chat_id, score FROM scores WHERE chat_id = {chat_id}').fetchall()
            points = base[0][1] + points

            base = self.cursor.execute('UPDATE scores SET location=?, time=?, score=? WHERE chat_id =?',(place, current_date, points, chat_id))


    def close(self):
        self.connection.close()