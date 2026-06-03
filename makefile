lint:
	run ruff check .
 
format:
	run ruff format .
 
fix:
	run ruff check . --fix
 
typecheck:
	python -m mypy .
 
test:
	python -m pytest -v
 
check: lint typecheck test