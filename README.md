# IT Company Task Manager
I have a team of Developers, Designers, Project Managers, and QA specialists. 
Also, I have a lot of tasks connected with the IT-sphere. 
But somehow, I still haven't heard anything about Trello or ClickUp. 
So, I decided to implement my own Task Manager, which will handle all 
    possible problems during product development in my team. 
    Everyone from the team can create tasks, assign these tasks to team members,
    and mark the tasks as done (of course, better before the deadlines).


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
![Screenshot_20240425_133118.png](..%2F..%2F..%2FPictures%2FScreenshot_20240425_133118.png)



Add a list of technologies used in the README.md;

Make sure that all images are loaded successfully in the project description;

Add blank lines to the end of the lines where needed;

Add a sample.env file with SECRET_KEY with dummy value and retrieve SECRET_KEY from an environment in the settings.py . Do not store it in a repository;

Include in .gitignore file only entities specific to your project, remove the rest;

Remove redundant comments and format properly urls.py files.