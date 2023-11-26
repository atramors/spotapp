# start uvicorn server
run:
	uvicorn spotapp:app --reload --port 8000 --host 0.0.0.0

# check syntax
lintapi:
	flake8 api

lint:
	flake8 tests

# run tests
test:
	pytest --cov-report term \
	--cov=. \
	--cov-config=tests/.coveragerc \
	tests/

cov:
	pytest --cov-report html \
	--cov=. \
	--cov-config=tests/.coveragerc \
	tests/
