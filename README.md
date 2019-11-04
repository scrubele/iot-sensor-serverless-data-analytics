# CRUD App using Vue.js and Django
<i><b>In order to run Web App:</i></b>

Create an isolated Python environment, and install dependencies:
```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```


Run the Django migrations to set up your models:
```python
python manage.py makemigrations
python manage.py makemigrations polls
python manage.py migrate
```
Start a local web server:
```
python manage.py runserver
```
Browse http://localhost:8000
