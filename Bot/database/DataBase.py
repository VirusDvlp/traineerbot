import pymysql.cursors
import os

from dotenv import load_dotenv


load_dotenv()

class DataBase:

    '''Class for database management'''


    def __init__(self):
        self.con = pymysql.connect( # connect to database
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            port=int(os.getenv('PORT')),
            database='traineerbot',
            cursorclass=pymysql.cursors.DictCursor
        )
    

    def check_user_exists(self, user_id: int) -> bool:
        '''Check if user is already in the db'''

        with self.con.cursor() as cur:
            cur.execute("""SELECT * FROM `users` WHERE `user_id` = %s""", (str(user_id),))
            
            return cur.fetchone() # if result is empty, func will return false
    
    
    def add_user(self, user_id: int, phone_number: str, weight: float, full_name: str, age: int) -> None:
        '''Add user(buyer) in the db'''
        with self.con.cursor() as cur:
            cur.execute(
                'INSERT INTO `users` (user_id, phone_number, weight, full_name, age) VALUES(%s, %s, %s, %s, %s)',
                (user_id, phone_number, weight, full_name, age)
            )
            self.commit()
    

    def get_user_id_list(self) -> tuple:
        '''Get list of users tg id for mailing'''
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `user_id` FROM `users`'
            )
            return cur.fetchall()
        
    
    def add_coach(self, name, exp, spec, photo, token) -> None:
        '''Add new coach in database'''
        with self.con.cursor() as cur:
            cur.execute(
                'INSERT INTO `coaches` (full_name, exp, specialization, photo, token) VALUES(%s, %s, %s, %s, %s)',
                (name, exp, spec, photo, token)
            )
        self.commit()
    
    def get_coach_id_list(self) -> list:
        res = []
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `user_id` FROM `coaches`'
            )
            id_list = cur.fetchall()
            for id in id_list:
                res.append(id['user_id'])
        return res
    
    def init_coach(self, user_id, token) -> None:
        '''Setting coach tg id'''
        with self.con.cursor() as cur:
            cur.execute(
                'UPDATE `coaches` SET `user_id` = %s WHERE `token` = %s',
                (user_id, token)
            )
        self.commit()
    

    def check_coach_init(self, user_id) -> bool:
        with self.con.cursor() as cur:
            cur.execute('SELECT `user_id` FROM `coaches` WHERE `user_id` = %s', (str(user_id),))
            return cur.fetchone()
        
    def get_coaches(self, all: bool, recomm: str = '') -> list:
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `id`, `user_id`, `full_name`, `exp`, `specialization`, `photo` FROM `coaches`'
            )
        fetch = cur.fetchall()
        res = []
        if all:
            return fetch
        else:
            recomm = recomm.split(',')
            for i in range(len(recomm)):
                recomm[i] = recomm[i].split('\t')
            for coach in fetch:
                for spec in coach['specialization'].split(','):
                    spec = spec.split('\t')
                    for rec in recomm:
                        if spec in rec:
                            if coach not in res:
                                res.append(coach)
        return res


    def commit(self) -> None:
        '''Saving changes in the db'''

        self.con.commit()
    

    def close_db(self) -> None:
        '''Close connection in the end of bot working'''
        self.con.close()
