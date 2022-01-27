test:
	python -m pytest tests --cov=./rf_network --cov-report=html
format-check:
	black --check .
format:
	isort src && black .
pre-commit-lint:
	SKIP=no-commit-to-branch pre-commit run --all-files
