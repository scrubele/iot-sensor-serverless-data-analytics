
<b>Start gcloud</b>
```
gcloud services enable sqladmin
gcloud sql instances describe [YOUR_INSTANCE_NAME]
```
find <i>connectionName</i> in the results of previous script. For example: <i>gothic-sequence-257518:us-central1:cloud-course</i>


<i>To change local postgresql port:</i>
```
#Open file, find port, change and save:
/etc/postgresql/11/main/
#reload
/etc/init.d/postgresql restart
```
<b>Add code to the settings.py:</b>
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cloud',
        'USER': 'scrubele',
        'PASSWORD': 'scrubele',
        'PORT': '5432',
    }
}

DATABASES['default']['HOST'] = '/cloudsql/gothic-sequence-257518:us-central1:cloud-course'
if os.getenv('GAE_INSTANCE'):
    pass
else:
    DATABASES['default']['HOST'] = '127.0.0.1'
    DATABASES['default']['PORT'] = '5432' #the same port that proxy has
```
<b>Run proxy and don't turn off:</b></p> 
<i> proxy is running on 5432, local postgresql on 5433</i>

```
cloud_sql_proxy_x64.exe -instances="gothic-sequence-257518:us-central1:cloud-course"=tcp:3307
./cloud_sql_proxy -instances="gothic-sequence-257518:us-central1:cloud-course"=tcp:5432
```

<b>Connect to your local proxy db.</b>
```
psql "host=127.0.0.1 port=5432 sslmode=disable dbname=cloud user=scrubele"
```
```
\c cloud - connect to your cloud
    \dt - show all tables.
```
<b>Create migrations when proxy is running (IMPORTANT):</b>
```
python manage.py makemigrations
python manage.py makemigrations polls
python manage.py migrate
```
<b>Create a Cloud Storage bucket and make it public:</b><p>
<i>I created bucket named cloud-course</i>
```
gsutil mb gs://cloud-course
gsutil defacl set public-read gs://cloud-course
```
<b>Add static urls to settings.py:</b>
```
STATIC_ROOT = 'static'
STATIC_URL = '/static/'
if os.getenv('GAE_INSTANCE'):
    STATIC_URL = 'https://storage.googleapis.com/cloud-course/static/'
```
<b>Collect and upload static content:</b>
```
python manage.py collectstatic
gsutil rsync -R static/ gs://cloud-course/static
```
<b>Add static folder to .gcloudignore</b>
```
static/
```
    
add app.yaml:
```
runtime: python37
# env: flexpython manage.py createsuperuser
entrypoint: gunicorn -b :$PORT config.wsgi

beta_settings:
    cloud_sql_instances: gothic-sequence-257518:us-central1:cloud-course

runtime_config:
  python_version: 3

handlers:

- url: /static
  static_dir: static
- url: /.*
  script: auto

vpc_access_connector:
  name: "projects/gothic-sequence-257518/locations/europe-west1/connectors/django-vue"
```
make requirements.txt with all libs and add gunicorn:
```
gunicorn==19.3.0
```
<b>Deploy :) </b>
```
gcloud app deploy
```

<b> Deploy frontend-files </b>
```
gsutil rsync -R frontend-api/ gs://cloud-course/
```


