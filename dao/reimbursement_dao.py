from decouple import config  # to create environment variable.
import psycopg
import json  # to jsonify image which is stored in bytea format in the database
from datetime import datetime as dt  # to use in resolved_at column which has a data type of timestamptz in postgreSQL

API_HOST = config('host')
API_PORT = config('port')
API_DBNAME = config('dbname')
API_USER = config('user')
API_PASSWORD = config('password')


class ReimbursementDao:
    @staticmethod
    def get_user_reimbursement(user_id):
        if not ReimbursementDao.check_if_finance_manager(user_id):
            with psycopg.connect(host=API_HOST, port=API_PORT, dbname=API_DBNAME, user=API_USER,
                                 password=API_PASSWORD) as conn:
                with conn.cursor() as cur:
                    cur.execute("select * from expense_reimbursement_system.reimbursements where reimb_author=%s",
                                (user_id,))

                    users_all_list = cur.fetchall()
                    new_list = []

                    for user in users_all_list:
                        user_list = list(user)
                        new_list.append(user_list)

                    for user in new_list:
                        for data in user:
                            if type(data) == bytes:
                                my_img = data
                                index_of_each_item = user.index(data)
                                user.pop(index_of_each_item)
                                json_str = json.dumps(my_img.decode('utf-8'))
                                user.insert(index_of_each_item, json_str)

                    return new_list
        else:
            with psycopg.connect(host=API_HOST, port=API_PORT, dbname=API_DBNAME, user=API_USER,
                                 password=API_PASSWORD) as conn:
                with conn.cursor() as cur:
                    cur.execute("select * from expense_reimbursement_system.reimbursements")

                    users_all_list = cur.fetchall()
                    new_list = []

                    for user in users_all_list:
                        user_list = list(user)
                        new_list.append(user_list)

                    for user in new_list:
                        for data in user:
                            if type(data) == bytes:
                                my_img = data
                                index_of_each_item = user.index(data)
                                user.pop(index_of_each_item)
                                json_str = json.dumps(my_img.decode('utf-8'))
                                user.insert(index_of_each_item, json_str)

                    return new_list

    @staticmethod
    def get_user_reimbursement_args(user_id, args):
        if not ReimbursementDao.check_if_finance_manager(user_id):
            with psycopg.connect(host=API_HOST, port=API_PORT, dbname=API_DBNAME, user=API_USER,
                                 password=API_PASSWORD) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "select * from expense_reimbursement_system.reimbursements where reimb_author=%s and status=%s",
                        (user_id, args))

                    users_all_list = cur.fetchall()
                    new_list = []

                    for user in users_all_list:
                        user_list = list(user)
                        new_list.append(user_list)

                    for user in new_list:
                        for data in user:
                            if type(data) == bytes:
                                my_img = data
                                index_of_each_item = user.index(data)
                                user.pop(index_of_each_item)
                                json_str = json.dumps(my_img.decode('utf-8'))
                                user.insert(index_of_each_item, json_str)
                    print(new_list)
                    return new_list
        else:
            with psycopg.connect(host=API_HOST, port=API_PORT, dbname=API_DBNAME, user=API_USER,
                                 password=API_PASSWORD) as conn:
                with conn.cursor() as cur:
                    cur.execute("select * from expense_reimbursement_system.reimbursements where status=%s", (args,))

                    users_all_list = cur.fetchall()
                    new_list = []

                    for user in users_all_list:
                        user_list = list(user)
                        new_list.append(user_list)

                    for user in new_list:
                        for data in user:
                            if type(data) == bytes:
                                my_img = data
                                index_of_each_item = user.index(data)
                                user.pop(index_of_each_item)
                                json_str = json.dumps(my_img.decode('utf-8'))
                                user.insert(index_of_each_item, json_str)

                    print(new_list)
                    return new_list

    @staticmethod
    def check_if_finance_manager(user_id):
        role = 'finance_manager'
        with psycopg.connect(host=API_HOST, port=API_PORT, dbname=API_DBNAME, user=API_USER,
                             password=API_PASSWORD) as conn:
            with conn.cursor() as cur:
                cur.execute("select * from expense_reimbursement_system.users where username=%s and role=%s ",
                            (user_id, role))
                user_details = cur.fetchall()
                return user_details

    @staticmethod
    def create_reimbursement(user_id, data):
        try:
            reimbursement_amount = data["reimbursement_amount"]
            type_of_expense = data["type_of_expense"]
            description = data["description"]
            # receipt_img = data["receipt_img"]
            with psycopg.connect(host=API_HOST, port=API_PORT, dbname=API_DBNAME, user=API_USER,
                                 password=API_PASSWORD) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "insert into expense_reimbursement_system.reimbursements(reimbursement_amount, type, description,  reimb_author) values(%s, %s, %s, %s) RETURNING *",
                        (reimbursement_amount, type_of_expense, description, user_id))
                    reimbursement_just_created = cur.fetchone()
                    print(reimbursement_just_created)
                    return "New reimbursement successfully created"
        except psycopg.errors.ForeignKeyViolation:
            return None

    @staticmethod
    def update_reimbursement(user_id, reimb_author, reimb_id, status):
        if ReimbursementDao.check_if_finance_manager(user_id):
            with psycopg.connect(host=API_HOST, port=API_PORT, dbname=API_DBNAME, user=API_USER,
                                 password=API_PASSWORD) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE expense_reimbursement_system.reimbursements SET status = %s, resolved_at=%s WHERE reimb_id = %s AND reimb_author=%s RETURNING *",
                        (status, dt.now(), reimb_id, reimb_author))
                    updated_reimbursement_row = cur.fetchone()

                    if not updated_reimbursement_row:
                        return None

                    return {
                        "message": f"Reimbursement request having reimbursement id number {reimb_id} of {reimb_author} has been {status}"}
