#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = walle
PYTHON_VERSION = 3.9.1
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################
## Set up python interpreter environment
.PHONY: create_environment
create_environment:
	python3.9 -m pip install virtualenv
	virtualenv venv
	source venv/bin/activate && \
	python3.9 -m pip install --upgrade pip setuptools wheel && \
	python3.9 -m pip install -e ".[dev]"

## Install Python Dependencies
.PHONY: requirements
requirements:
	source venv/bin/activate && \
	$(PYTHON_INTERPRETER) -m pip install -U pip  && \
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt


## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: style
style:
	flake8 agent_module
	isort --check --diff --profile black agent_module
	black --check agent_module





#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
