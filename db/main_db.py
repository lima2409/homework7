import sqlite3
from db import queries
from config import path_db
from datetime import datetime


def init_db():
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.create_tasks)
        print('БД подключена')
        conn.commit()


def add_task(task):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.insert_task, (task, current_date))
        conn.commit()
        task_id = cursor.lastrowid

    return task_id, current_date


def update_task(task_id, new_task=None, completed=None):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()

        if new_task is not None:
            cursor.execute(queries.update_task, (new_task, task_id))

        if completed is not None:
            cursor.execute(
                queries.update_completed,
                (completed, task_id)
            )

        conn.commit()


def get_tasks(filter_type='all'):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()

        if filter_type == 'all':
            cursor.execute(queries.select_tasks)

        elif filter_type == 'completed':
            cursor.execute(queries.select_tasks_completed)

        elif filter_type == 'uncompleted':
            cursor.execute(queries.select_tasks_uncompleted)

        else:
            cursor.execute(queries.select_tasks)

        tasks = cursor.fetchall()

    return tasks

def delete_completed_tasks():
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.delete_completed_tasks)
        conn.commit()