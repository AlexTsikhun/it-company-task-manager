# IT Company Task Manager
I have a team of Developers, Designers, Project Managers, and QA specialists. 
Also, I have a lot of tasks connected with the IT-sphere. 
But somehow, I still haven't heard anything about Trello or ClickUp. 
So, I decided to implement my own Task Manager, which will handle all 
    possible problems during product development in my team. 
    Everyone from the team can create tasks, assign these tasks to team members,
    and mark the tasks as done (of course, better before the deadlines).


## Technologies Used

- Django
- Sqlite3
- HTML (Jinja)/CSS/Javascript
- Bootstrap
- django-admin-star library

### Installation
```shell
git clone https://github.com/AlexTsikhun/it-company-task-manager
cd it-company-task-manager
python3 -m venv .venv
pip install -r requirements.txt
python3 manage.py makemigations
python3 manage.py migate
python3 manage.py runserver

```

#### DB Structure:
![img.png](images/img.png)


#### Page example
![img.png](images/index.png)
![workers.png](images/workers.png)
![detail_worker.png](images%2Fdetail_worker.png)
![tasks.png](images%2Ftasks.png)
![create_task.png](images%2Fcreate_task.png)

### Ideas to add:

- For each worker it is shown separately: completed and not completed tasks.
- Add Tags (like landing-page-layout or python-refactoring) for tasks with Many-to-Many relationship.
- Add support for Projects and Teams, different teams can work on different projects, and also inside projects there are a lot of tasks to do (complicated).
- total visitors counter
- add search


toDo
- add which worker should do this task/ or has this position
- my task
- future work - add alternative solution (client side with JS) for completed/uncompleted tasks
- when in `all`, btn should be unactive, show selected tab in tasks
- add checkbox for tasks in the main task-list page (and save with js??)
- placeholder to fields in forms
- bigger font size?
- btns in form
- greeting when not login
- title
- in long table or list don't scroll all page - scroll olny table or list
- json file with data 
- add tests
