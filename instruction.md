
<b>Start gcloud</b>
```
gcloud services enable sqladmin
gcloud sql instances describe [YOUR_INSTANCE_NAME]
```
find <i>connectionName</i> in the results of previous script. For example: <i>gothic-sequence-257518:us-central1:cloud-course</i>

<b>Run proxy and don't turn off:</b></p> 
<i> proxy is running on 5432, local postgresql on 5433</i>

```
cloud_sql_proxy_x64.exe -instances="gothic-sequence-257518:us-central1:cloud-course"=tcp:3307
./cloud_sql_proxy -instances="gothic-sequence-257518:us-central1:cloud-course"=tcp:5432
```

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
    DATABASES['default']['PORT'] = '5433'
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
<b>Deploy :) </b>
```
gcloud app deploy
```



