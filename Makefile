#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = walle
PYTHON_VERSION = 3.11.9
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################
## Set up python interpreter environment
## python3.11.9 is not via pyenv
.PHONY: create_environment
create_environment:
	python3.11 -m pip install virtualenv
	virtualenv venv
	source venv/bin/activate && \
	venv/bin/python -m pip install --upgrade pip setuptools wheel && \
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install notebook

.PHONY: tool_ollama .FORCE
tool_ollama:
	@export OLLAMA_BASE_URL="http://localhost:11434" && ollama serve

# aka memGPT
# Assuming tool_ollama has been executed in the other window
.PHONY: tool_letta_backend
tool_letta_backend:
	@export OLLAMA_BASE_URL="http://localhost:11434" && \
	cd /Users/chang/Documents/dev/git/project/walle && \
	source venv/bin/activate && \
	letta server

.PHONY: tool_letta_agent
tool_letta_agent:
	@export OLLAMA_BASE_URL="http://localhost:11434" && \
		cd /Users/chang/Documents/dev/git/project/walle && \
    	source venv/bin/activate && \
    	letta run


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
