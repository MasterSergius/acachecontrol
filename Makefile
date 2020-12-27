init:
	pip install -e .

lint:
	pre-commit run -a

test:
	pytest tests --cov-config pyproject.toml