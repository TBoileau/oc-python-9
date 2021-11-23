VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python

freeze:
	${PYTHON} -m pip freeze > requirements.txt

prepare:
	python3 -m pip install --upgrade pip
	python3 -m venv $(VENV_NAME)

install:
	pip install --no-cache-dir wheel
	${PYTHON} -m pip install -r requirements.txt

run:
	${PYTHON} manage.py runserver

migration:
	${PYTHON} manage.py makemigrations

migrate:
	${PYTHON} manage.py migrate

tests:
	${PYTHON} manage.py test
