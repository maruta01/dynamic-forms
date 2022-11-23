.PHONY: build init start stop bash cleanup
COMPOSE_FILE := docker/docker-compose.yml
PROJECT_NAME := jamesite

build:
	docker-compose -f $(COMPOSE_FILE) build
	
init:
	docker-compose -f $(COMPOSE_FILE) run --rm app django-admin startproject $(PROJECT_NAME) .

start:
	docker-compose -f $(COMPOSE_FILE)  -p $(PROJECT_NAME) up -d

stop:
	docker compose -f $(COMPOSE_FILE)  -p $(PROJECT_NAME) stop

bash:
	docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) run --rm app bash

cleanup:
	docker-compose -f $(COMPOSE_FILE)  -p $(PROJECT_NAME) down
