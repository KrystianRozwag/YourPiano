import psycopg2
from decouple import config
class DatabaseLoader:
    def __init__(self):
        self.DBNAME = config("DBNAME") 
        self.DBUSER = config("DBUSER") 
        self.DBPASS = config("DBPASS") 
        self.DBHOST = config("DBHOST") 
        self.DBPORT = config("DBPORT") 

    def connect(self):
        try:

            self.conn = psycopg2.connect(
            dbname=self.DBNAME,
            user=self.DBUSER,
            password=self.DBPASS,
            host=self.DBHOST,
            port=self.DBPORT
        )
            self.cur = self.conn.cursor()   
        except Exception as e:
            print(f"Could not connect to the database: {e}")
            return False
        return True

    def send_data_to_db(self,topic, desc, date, path):
        try:
            self.cur.execute(f"INSERT INTO diaries(user_id, date, topic, description, path)\
             VALUES(1,'{date}', '{topic}', '{desc}', '{path}');")
            self.conn.commit()
        except Exception as e:
            print(f"Could not pass data to the database: {e}")

    def read_data_from_db(self, date):
        try:
            self.cur.execute(f"SELECT topic, description, path FROM diaries WHERE date = '{date}'")
            row = self.cur.fetchone()
            return row
        except Exception as e:
            print(f"Data does not exist in the database: {e}")
            return False
    def update_data_in_db(self, topic, description, path, date):
        try:
            self.cur.execute(f"UPDATE diaries set topic = '{topic}', description = '{description}', path = '{path}' where date = '{date}';")
            self.conn.commit()
           # self.cur.execute(f"UPDATE diaries set topic = '{topic}', description = '{description}', path = '{path}' where date = '{date}';")
            #self.conn.commit()
        except Exception as e:
            print(f"Could not update data in the database: {e}")
    def disconnect(self):
        self.cur.close()
        self.conn.close()


