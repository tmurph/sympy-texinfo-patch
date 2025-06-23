.PHONY: test clean build-test install

install:
	pip install -e .

test:
	pytest -v

test-build:
	cd tests/test_docs && sphinx-build -b texinfo source build/texinfo -E

clean:
	rm -rf tests/test_docs/build
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

view-texi:
	cat tests/test_docs/build/texinfo/*.texi | less
