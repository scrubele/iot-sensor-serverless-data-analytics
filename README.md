
# Data processing of IoT sensors using serverless technologies
<h2><i><b>In order to run REST API:</i></b></h2>
<h4>Create a postgresql database:</h4>

Install postgresql:

```
    sudo apt install postgresql postgresql-contrib
```
Create a user and grant all privileges:
```
sudo -u postgres psql
postgres=# create database cloud;
postgres=# create user myuser with encrypted password 'passwordd';
postgres=# grant all privileges on database cloud to myuser;
```

<h4>Create an isolated Python environment, and install dependencies:</h4>
For psycopg2 install: 

```
sudo apt install libpq-dev python3-dev
```

```
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
```
Run the Django migrations to set up your models, create user:
```python
python manage.py makemigrations
python manage.py makemigrations api
python manage.py migrate
python manage.py createsuperuser
```
Start a local web server:
```
python manage.py runserver
```
Browse http://localhost:8000

### Next steps follow in [instruction.md](https://github.com/scrubele/cloud-labs/blob/django-iot-data-processing/Instruction.md)
