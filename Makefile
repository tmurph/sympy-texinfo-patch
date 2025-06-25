# Python environment
PYTHON       = venv/bin/python
PIP          = venv/bin/pip
PYTEST       = venv/bin/pytest
SPHINXBUILD  = venv/bin/sphinx-build

# Sphinx options
SPHINXOPTS   =
BUILDDIR     = docs/_build
TEXINFODIR   = $(BUILDDIR)/texinfo
SOURCEDIR    = tests/testdata
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(SPHINXOPTS)

# These are directories that begin with "test-"
PROJECTS != ls $(SOURCEDIR)

.PHONY: $(PROJECTS)
.PHONY: test clean

%.texi: test-%
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(SOURCEDIR)/$< $(TEXINFODIR) -E

%.info: %.texi
	$(MAKE) -C $(TEXINFODIR) $@

view-%: %.info
	./view.sh $(TEXINFODIR)/$<

test:
	$(PYTEST) -v

clean:
	rm -rf $(BUILDDIR)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# These don't belong in a Makefile.  They're more of a configure check.
# Whatever.  The recipes are here now, and I want them saved somewhere.
$(PYTHON) $(PIP):
	python3 -m venv venv

$(PYTEST) $(SPHINXBUILD): $(PIP)
	$(PIP) install sphinx pytest pytest-cov
	$(PIP) install -e .
