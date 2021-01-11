install:
	pip install -e .

lint:
	pre-commit run -a

test:
	pytest tests --cov-config pyproject.toml

upload:
	rm -rf dist
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*
