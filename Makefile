.PHONY: format lint test security build run push

format:
	black .
	isort .
	autopep8 --in-place --recursive .

lint:
	radon cc . -a
	flake8 .
	

security:
	bandit -r .

test:
	pytest

build:
	docker build -t geospatial-chat .

run:
	docker run -p 8501:8501 geospatial-chat

push:
	docker tag geospatial-chat botavalo/geospatial-chat:latest
	docker push botavalo/geospatial-chat:latest

pull:
	docker pull botavalo/geospatial-chat:latest

all: format lint security test build run