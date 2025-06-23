# Python environment
PYTHON       = venv/bin/python
PIP          = venv/bin/pip
PYTEST       = venv/bin/pytest
SPHINXBUILD  = venv/bin/sphinx-build

# Sphinx options
SPHINXOPTS   =
BUILDDIR     = tests/test_docs/build
SOURCEDIR    = tests/test_docs/source
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(SPHINXOPTS)

.PHONY: test clean build-test install view-texi venv

venv: $(PYTHON)
	python3 -m venv venv
	$(PIP) install sphinx pytest pytest-cov
	$(PIP) install -e .

install: venv
	$(PIP) install -e .

test:
	$(PYTEST) -v

test-build:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/texinfo -E

clean:
	rm -rf $(BUILDDIR)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

view-texi:
	cat $(BUILDDIR)/texinfo/*.texi | less
