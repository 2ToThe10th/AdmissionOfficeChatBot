import psycopg2


class DataBaseTelegram:
    def __init__(self, db_name, db_user, password):
        self.data_base = psycopg2.connect(dbname=db_name, user=db_user,
                                          password=password, host='localhost')
        self.data_base.autocommit = True

        cursor = self.data_base.cursor()

        cursor.execute("Create table if not exists ABITU ("
                       "USER_ID INTEGER primary key, "
                       "STATUS TEXT DEFAULT NULL, "
                       "EMAIL varchar(100) DEFAULT NULL"
                       ");")

        cursor.close()

    def add_user(self, chat_id):
        cursor = self.data_base.cursor()

        cursor.execute("Select * "
                       "from abitu "
                       "where user_id = %(user_id)s",
                       {'user_id': chat_id})

        if not cursor.rowcount:
            cursor.execute("Insert into abitu (USER_ID, STATUS, EMAIL) "
                           "values(%(user_id)s, DEFAULT, DEFAULT )",
                           {'user_id': chat_id})

        cursor.close()

    def get_status(self, chat_id):
        cursor = self.data_base.cursor()

        cursor.execute("Select STATUS "
                       "from abitu "
                       "where user_id = %(user_id)s",
                       {'user_id': chat_id})

        ret = cursor.fetchone()
        cursor.close()

        if ret is None:
            return None
        return ret[0]

    def get_email(self, chat_id):
        cursor = self.data_base.cursor()

        cursor.execute("Select EMAIL "
                       "from abitu "
                       "where user_id = %(user_id)s",
                       {'user_id': chat_id})

        ret = cursor.fetchone()
        cursor.close()

        if ret is None: 
            return None
        return ret[0]

    def set_status(self, chat_id, status):
        cursor = self.data_base.cursor()

        cursor.execute("UPDATE abitu "
                       "set STATUS = %(status)s "
                       "where user_id = %(user_id)s",
                       {'user_id': chat_id, 'status': status})

        cursor.close()

    def set_email(self, chat_id, email):
        cursor = self.data_base.cursor()

        cursor.execute("SELECT * "
                       "FROM ladder "
                       "Where email = %(email)s",
                       {'email': email})

        if (not cursor.rowcount) and email is not None:
            return 1

        cursor.execute("UPDATE abitu "
                       "set EMAIL = %(email)s "
                       "where user_id = %(user_id)s",
                       {'user_id': chat_id, 'email': email})

        cursor.close()
        return 0