SHELL = /usr/bin/env bash -xeuo pipefail

localstack-up:
	@docker-compose up -d localstack

localstack-stop:
	@docker-compose stop localstack

lint:
	@python -m flake8 src

validate:
	@aws cloudformation validate-template \
		--template-body file://sam.yml

.PHONY: \
	localstack-up \
	localstack-down \
	lint \
	validate
