# start uvicorn server
run:
	uvicorn spotapp:app --reload --port 8000

# check syntax
lintapi:
	flake8 api

lint:
	flake8 tests

# run tests
test:
	pytest tests --cov-config=tests/.coveragerc