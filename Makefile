.EXPORT_ALL_VARIABLES:
PROD_COMPOSE_FILE ?= docker-compose.yml
DEV_COMPOSE_FILE ?= docker-compose-dev.yml

up-dev:  ## Run dev containers
	docker-compose -f $(DEV_COMPOSE_FILE) up

down-dev: ## Stop dev containers
	docker-compose -f $(DEV_COMPOSE_FILE) down

build-dev: ## Build dev containers
	docker-compose -f $(DEV_COMPOSE_FILE) build

up:  ## Run prod containers
	docker-compose -f $(PROD_COMPOSE_FILE) up -d

down: ## Stop prod containers
	docker-compose -f $(PROD_COMPOSE_FILE) down

build: ## Build prod containers
	docker-compose -f $(PROD_COMPOSE_FILE) build

build-kafka:
	docker-compose -f $(PROD_COMPOSE_FILE) up -d zookeeper kafka

up-kafka:
	docker-compose -f $(PROD_COMPOSE_FILE) up -d zookeeper kafka