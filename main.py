from uuid import uuid4
from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, html, use_state
import reactpy


@component
def App():
    tasks, set_tasks = use_state([])
    title, set_title = use_state("")
    description, set_description = use_state("")

    editing, set_editing = use_state(False)
    task_id, set_task_id = use_state(None)

    @reactpy.event(prevent_default=True)
    def handle_submit(e):

        if not title or not description:
            return

        if not editing:
          new_task = {
              "title": title,
              "description": description,
              "id": uuid4()
          }
          print(tasks + [new_task])
          set_tasks(tasks + [new_task])
        else:
          print(task_id, title, description)
          updated_tasks = [task if task["id"] != task_id else {
              "title": title,
              "description": description,
              "id": task_id
          } for task in tasks]
          set_tasks(updated_tasks)


        set_title("")
        set_description("")
        set_editing(False)
        set_task_id(None)

    def handle_delete(task_id):
        print(task_id)
        filtered_tasks = [task for task in tasks if task["id"] != task_id]
        set_tasks(filtered_tasks)
    
    def handle_edit(task):
        print(task)
        set_editing(True)
        set_title(task["title"])
        set_description(task["description"])
        set_task_id(task["id"])


    list_items = [html.li({
        "key": index,
    },
    html.div(
        f"{task['title']}: {task['description']}",
        f"{task['id']}",
        html.button({
            "on_click": lambda e, task_id=task["id"]: handle_delete(task_id)
        },"delete"),
        html.button({
            "on_click": lambda e, task=task: handle_edit(task)
        },"edit"),
    )
    ) for index, task in enumerate(tasks)]

    return html.div(
        {
            "style": {
              "padding": "3rem",
            }
        },
        html.form(
            {
                "on_submit": handle_submit
            },
            html.input({
                "type": "text",
                "placeholder": "Title",
                "on_change": lambda e: set_title(e["target"]["value"]),
                "autofocus": True,
                "value": title,
            }),
            html.textarea({
                "placeholder": "Description",
                "on_change": lambda e: set_description(e["target"]["value"]),
                "rows": 3,
                "value": description,
            }),
            html.button({
                "type": "submit",
            }, "Create" if not editing else "Update"), 
        ),
        html.ul(
            list_items
        )
    )


app = FastAPI()
configure(app, App)
