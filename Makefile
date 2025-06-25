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

# Utility scripts
VIEW	     = bin/view

.PHONY: test clean

test:
	$(PYTEST) -v

clean:
	rm -rf $(BUILDDIR)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# These must be directories that begin with "test-"
TEST-SOURCES != ls $(SOURCEDIR)

# Note that this doesn't actually do what I think it does.  My goal is
# to have `make view-basic` run through all these rules, which it
# currently does, but only because the intermediate files (while built)
# are never known to make because they're built so low down.  I suppose
# in a more perfect makefile it would be aware of the intermediate
# files, would rebuild them only when the directory contents changed,
# and would still pop up a viewer regardless of if anything needed
# rebuilding.  But I'm too tired to figure that out right now, and it's
# really not important.
.PHONY: $(TEST-SOURCES)

%.texi: test-%
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(SOURCEDIR)/$< $(TEXINFODIR) -E

%.info: %.texi
	$(MAKE) -C $(TEXINFODIR) $@

view-%: %.info
	$(VIEW) $(TEXINFODIR)/$<

# These don't belong in a Makefile.  They're more of a configure check.
# Whatever.  The recipes are here now, and I want them saved somewhere.
$(PYTHON) $(PIP):
	python3 -m venv venv

$(PYTEST) $(SPHINXBUILD): $(PIP)
	$(PIP) install sphinx pytest pytest-cov
	$(PIP) install -e .
