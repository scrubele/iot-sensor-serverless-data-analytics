GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: all
all: create-bucket create-cluster get-credentials create-secret-level proxy retrieve-image build docker-auth activate-account push template

.PHONY: test
test: push template deploy

.PHONY: create-bucket
create-bucket:
	gsutil mb gs://$(GCLOUD_PROJECT)1
	gsutil defacl set public-read gs://$(GCLOUD_PROJECT)1

.PHONY: create-cluster
create-cluster:
	-gcloud container clusters create cloud-lab2 \
		--scopes "https://www.googleapis.com/auth/userinfo.email","cloud-platform",bigquery,storage-rw,compute-rw
		--num-nodes 4 --zone "us-central1-a"


.PHONY: get-credentials
get-credentials:
	gcloud container clusters get-credentials cloud-lab2 --zone "europe-west1-b"

.PHONY: create-secret-level
create-secret-level:
	skubectl create secret generic cloudsql-oauth-credentials1 --from-file=credentials.json="cloudcourse-254413-b15a473f8152.json"

.PHONY: proxy
proxy: 
	kubectl create secret generic cloudsql --from-literal=username=scrubele --from-literal=password=qwer1234***

.PHONY: retrieve-image
retrieve-image:
	docker pull b.gcr.io/cloudsql-docker/gce-proxy:1.05

.PHONY: build
build:
	sudo docker build -t gcr.io/$(GCLOUD_PROJECT)1/cloud-lab2 .

.PHONY: docker-auth
docker-auth:
	gcloud auth configure-docker
	

.PHONY: activate-account
activate-account:
	gcloud auth activate-service-account \
  	273499743272-compute@developer.gserviceaccount.com \
          --key-file=cloudcourse-254413-b15a473f8152.json

.PHONY: change-scope
change-scope: gcloud compute instances set-service-account $(GCLOUD_PROJECT) --scopes=storage-rw

.PHONY: push
push: build
	sudo docker push -- gcr.io/$(GCLOUD_PROJECT)/cloud-lab2

.PHONY: template
template:
	sed -i ".tmpl" "s/\$$GCLOUD_PROJECT/$(GCLOUD_PROJECT)/g" cloud-lab.yaml

.PHONY: deploy
deploy: push template
	kubectl create -f cloud-lab.yaml

.PHONY: update
update:
	kubectl patch deployment cloud-lab2 -p "{\"spec\":{\"template\":{\"metadata\":{\"labels\":{\"date\":\"`date +'%s'`\"}}}}}"

.PHONY: delete
delete:
	kubectl delete rc cloud-lab2
	kubectl delete service cloud-lab2