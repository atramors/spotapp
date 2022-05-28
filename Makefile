# start uvicorn server
run:
	uvicorn spotapp:app --reload --port 8000

# run tests
tests:
	cd tests $$ pytest