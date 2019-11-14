# Data processing of IoT sensors using serverless technologies

### Deploy an App Engine app:
> Follow steps in the [instruction.md](https://github.com/scrubele/cloud-labs/blob/django-vue-web-app/instruction.md)
  
### Cloud Endpoints for App Engine standart app:
Find:
<i>
* ESP_PROJECT_ID: iot-data-processing-258913 	
* ESP_PROJECT_NUMBER:  994414802550 
* APP_PROJECT_ID: iot-data-processing-258913
* IAP_CLIENT_ID: 

</i>

### Deploying ESP:
Set a region for Cloud Run (only <b>us-central</b> is supported):
```
gcloud config set run/region us-central1
```
Deploy ESP to Cloud RUN:<i> cloud-course - is the name that with I want to use for the service</i>
```
gcloud beta run deploy cloud-course \
    --image="gcr.io/endpoints-release/endpoints-runtime-serverless:1.30.0" \
    --allow-unauthenticated \
    --project=iot-data-processing-258913 	
```


* API gateway HOST: https://cloud-course-p5guh5uvlq-uc.a.run.app

Add <b>openapi-appengine.yaml</b>:
```
swagger: '2.0'
info:
  title: IoT data processing
  description: Data processing of IoT sensors using serverless technologies
  version: 1.0.0
host: cloud-course-osgbjo7jfa-uc.a.run.app
schemes:
  - https
produces:
  - application/json
x-google-backend:
  address: https://cloud-course-p5guh5uvlq-uc.a.run.app
paths:
  /api/sensors :
    get:
      summary: Get sensors' data
      operationId: get-sensors
      responses:
        '200':
          description: A successful response
          schema:
            type: string
    post:
      summary: Post sensor's data 
      operationId: post-sensors
      responses:
        '200':
          description: A successful response
          schema:
            type: string
```
Deploy ESP^
```
gcloud endpoints services deploy openapi-appengine.yaml \
  --project iot-data-processing-258913
```
