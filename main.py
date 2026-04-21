import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = 'ToDoList'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=20)
    filter_type = 'all'

    def load_tasks():
        task_list.controls.clear()
        tasks = main_db.get_tasks(filter_type=filter_type)

        for task_id, task, task_date, completed in tasks:
            task_list.controls.append(
                view_tasks(
                    task_id=task_id,
                    task_text=task,
                    task_date=task_date,
                    completed=completed
                )
            )

        page.update()

    def view_tasks(task_id, task_text, task_date, completed=0):
        task_field = ft.TextField(
            read_only=True,
            value=task_text,
            expand=True
        )

        checkbox_task = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        date_text = ft.Text(task_date, size=12, color='grey')

        def enable_edit(_):
            task_field.read_only = not task_field.read_only
            page.update()

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            page.update()

        edit_button = ft.IconButton(
            icon=ft.Icons.EDIT,
            on_click=enable_edit
        )

        save_button = ft.IconButton(
            icon=ft.Icons.SAVE,
            on_click=save_task
        )

        return ft.Row([
            checkbox_task,
            task_field,
            edit_button,
            save_button,
            date_text
        ])

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        load_tasks()

    def add_task_db(_):
        if task_input.value:
            task_text = task_input.value

            task_id, task_date = main_db.add_task(task=task_text)

            task_list.controls.append(
                view_tasks(
                    task_id=task_id,
                    task_text=task_text,
                    task_date=task_date,
                    completed=0
                )
            )

            task_input.value = ""
            page.update()

    task_input = ft.TextField(
        label='Введите задачу',
        expand=True,
        on_submit=add_task_db
    )

    add_task_button = ft.ElevatedButton(
        'ADD',
        on_click=add_task_db,
        icon=ft.Icons.ADD
    )

    main_object = ft.Row([task_input, add_task_button])

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()
    
    def clear_completed(_):
        main_db.delete_completed_tasks()
        load_tasks()  

    filter_buttons = ft.Row([
        ft.ElevatedButton('Все задачи', on_click=lambda e: set_filter('all')),
        ft.ElevatedButton('В работе', on_click=lambda e: set_filter('uncompleted')),
        ft.ElevatedButton('Готово ✅', on_click=lambda e: set_filter('completed'))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    clear_button = ft.ElevatedButton(
    "Очистить выполненные",
    icon=ft.Icons.DELETE,
    on_click=clear_completed,
    color="white",
    bgcolor="red"
)

    page.add(main_object, filter_buttons, clear_button, task_list)

    load_tasks()


if __name__ == "__main__":
    main_db.init_db()
    ft.app(main)