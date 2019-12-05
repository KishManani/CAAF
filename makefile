install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt &&\
	pip install -e .

test:
	black --diff --check . &&\
	flake8 &&\
	pytest -vv

format:
	black .
