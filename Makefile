NAME=contours

.PHONY: list
list:
	@echo "dev - installs all packages needed for development"
	@echo "check:"
	@echo "  codestyle - run the PEP8 (style) checker on the project"
	@echo "  docstyle  - run the PEP257 (docstrings) checker on the project"
	@echo "  lint      - run pylint on the project"
	@echo "doc:"
	@echo "  html     - build HTML documentation"
	@echo "  pdf      - build PDF documentation (requires pdflatex)"
	@echo "  man      - build man page documentation"
	@echo "  info     - build texinfo documentation (requires makeinfo)"
	@echo "  doctest  - check documentation examples"
	@echo "  coverage - check documentation coverage"
	@echo "  server   - start a webserver serving the documentation (port=8000)"
	@echo "test - run all unit tests"

.PHONY: all
all: check doc test

.PHONY: dev
dev:
	pip install -r requirements.txt

.PHONY: check
check: codestyle docstyle lint

.PHONY: codestyle
codestyle:
	pycodestyle --exclude=.ropeproject,.eggs .

.PHONY: docstyle
docstyle:
	pydocstyle --match-dir='^(?!tests|docs|\.).*$$'

.PHONY: lint
lint:
	pylint $(NAME) setup.py docs/conf.py tests

.PHONY: doc
doc: html pdf man info doctest coverage 

.PHONY: html
html:
	$(MAKE) -C docs html

.PHONY: pdf
pdf:
	$(MAKE) -C docs latexpdf

.PHONY: man
man:
	$(MAKE) -C docs man

.PHONY: info
info:
	$(MAKE) -C docs info

.PHONY: doctest
doctest:
	$(MAKE) -C docs doctest

.PHONY: coverage
coverage:
	$(MAKE) -C docs coverage
	@echo ""
	@echo ""
	@echo ""
	@echo ""
	@echo "**************************************"
	@echo "*** Documentation Coverage Summary ***"
	@echo "**************************************"
	@echo ""
	@echo ""
	@cat docs/_build/coverage/c.txt
	@echo ""
	@cat docs/_build/coverage/python.txt

.PHONY: server
server:
	cd docs/_build/html; python -m http.server

.PHONY: test
test:
	coverage erase
	coverage run --branch --source $(NAME) -m unittest discover tests
	coverage html
	coverage report --fail-under=90 --show-missing

.PHONY: clean
clean:
	rm -rf `find -name "__pycache__"`
	rm -rf `find -name ".ropeproject"`
	rm -rf htmlcov
	$(MAKE) -C docs clean
