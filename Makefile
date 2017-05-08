.PHONY: test
test:
	py.test --cov=midi --cov-report term-missing --cov-report html tests/

.PHONY: test-watch
test-watch:
	ptw -v --onpass 'py.test --cov=midi --cov-report term-missing --cov-report html tests/'
