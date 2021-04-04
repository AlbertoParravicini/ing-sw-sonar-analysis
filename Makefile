# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help run-tests

help: ## Show commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help


# COMMANDS
run-tests: ## Run all tests and export reports
	python m01_init_build.py
	./m02_build.sh
	python m03_clean_logs.py
	python m04_sonar_reports.py
