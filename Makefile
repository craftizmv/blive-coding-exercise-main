
.PHONY: test
test:
	docker build -t cucumber .
	docker run -it --rm -v ${PWD}/cucumber/logs:/task/cucumber/logs cucumber
