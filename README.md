# CRUD App using Vue.js and Django
<h1><i><b>In order to run Web App:</i></b></h1>

<h3>Create postgresql database:</h3>

Install postgresql

```
    sudo apt install postgresql postgresql-contrib
```
Create user and grant all privileges:
```
sudo -u postgres psql
postgres=# create database cloud;
postgres=# create user myuser with encrypted password 'mypass';
postgres=# grant all privileges on database cloud to myuser;
```

<h3>Create an isolated Python environment, and install dependencies:</h3>

```
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
```
Run the Django migrations to set up your models:
```python
python manage.py makemigrations
python manage.py makemigrations api
python manage.py migrate
```
Start a local web server:
```
python manage.py runserver
```
Browse http://localhost:8000
