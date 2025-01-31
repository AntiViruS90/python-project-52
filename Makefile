install:
	uv pip install -e .

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

dev:
	python manage.py runserver 8080

lint:
	ruff check .

test:
	python manage.py test

test-coverage:
	coverage run manage.py test
	coverage report
	coverage xml

selfcheck:
	uv pip check

check:
	make lint
	make test

build:
	./build.sh

start:
	python -m gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker

start_WNDS:
	uvicorn Task_Manager.asgi:application

.PHONY: install test lint selfcheck check build