import sqlite3
from db import queries
from config import path_db
from datetime import datetime



def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.create_tasks)
    print('БД подключена')
    conn.commit()
    conn.close()


def add_task(task):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    current_date = str(datetime.now())
    cursor.execute(queries.insert_task, (task, current_date))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id, current_date


def update_task(task_id, new_task=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.update_task, (new_task, task_id))
    conn.commit()
    conn.close()
