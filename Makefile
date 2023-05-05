.PHONY: install
install:
	docker compose up -d
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirement.txt

.PHOME: migrate
migrate:
	. venv/bin/activate && python3 manage.py db init && python3 manage.py db migrate && python3 manage.py db upgrade

.PHONE: run
run:
	. venv/bin/activate && python3 manage.py runserver

.DEFAULT_GOAL := run