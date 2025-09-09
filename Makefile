APP=mini-netflix
REGISTRY?=
TAG?=local
.PHONY: install run lint test docker-build docker-run tf-init tf-apply tf-destroy ansible-deploy
install:
	pip install -U pip
	pip install -r backend/requirements.txt
run:
	uvicorn backend.app:app --reload
lint:
	ruff check backend tests
test:
	pytest -q
docker-build:
	docker build -t $(APP):$(TAG) .
docker-run:
	docker run --rm -p 8000:8000 -v $(PWD)/data:/data $(APP):$(TAG)
tf-init:
	cd infra/terraform && terraform init
tf-apply:
	cd infra/terraform && terraform apply -auto-approve -var="project_name=$(APP)"
tf-destroy:
	cd infra/terraform && terraform destroy -auto-approve -var="project_name=$(APP)"
ansible-deploy:
	cd infra && ./generate_inventory.sh && cd ansible && ansible-playbook -i inventory.ini playbook.yml -e "app_image=$(REGISTRY)/$(APP):$(TAG)"
