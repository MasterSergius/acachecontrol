init:
	pip install -e .

lint:
	pre-commit run -a
