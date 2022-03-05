.PHONY: help deploy

define HELPER_CONTENT
Helper:
	- create-env   - Cretes the empty env folder.
	- install      - Install one dependency package. Ex: make install package=python-dotenv.
	- lock         - Lock all dependencies to the requirements.txt file.
	- deps         - Install all dependencies from the requirements.txt file. Run this after create-env.
	- fresh	       - Create the env folder and install all dependencies from the requirements.txt file.
	- docker-build - Build the docker image.
	- docker-run   - Run the docker container based on the image.
	- docker       - Build the image and also run the container in one go.
	- docker-stop  - Stops and removes the docker container.
endef

export HELPER_CONTENT

help:
	@echo "$$HELPER_CONTENT"

create-env:
	python3 -m venv env

install:
	./env/bin/pip3 install $(package)

lock:
	./env/bin/pip3 freeze > requirements.txt

deps:
	./env/bin/pip3 install -r requirements.txt

fresh: create-env deps

docker-build:
	docker build -t serbanblebea/trading-strategy:v1.0 .

docker-run:
	docker run -v ${PWD}/data:/app/data --env-file ./.env -d --name trading_strategy serbanblebea/trading-strategy:v1.0

docker: docker-build docker-run

docker-stop:
	docker stop trading_strategy && docker rm trading_strategy

test:
	./execute_test.sh
