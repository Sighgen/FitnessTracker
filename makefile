lint:
	ruff check .
 
format:
	ruff format .
 
fix:
	ruff check . --fix
 
typecheck:
	python -m mypy .
 
test:
	python -m pytest -v
 
check: lint typecheck test