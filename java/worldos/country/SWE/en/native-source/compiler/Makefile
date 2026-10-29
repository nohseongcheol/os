PYTHON ?= python3
.PHONY: all test openjdk-build-local openjdk-test-local
all: build/calculation

build/calculation: aheadOfTime.sh $(wildcard JavaTools/*) RuntimeSupport.s linuxStartup.s examples/calculation.java
	sh aheadOfTime.sh --target linux --entry calculation.run -o $@ examples/calculation.java

test: all
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

openjdk-build-local:
	$(PYTHON) openjdk_local.py build

openjdk-test-local:
	$(PYTHON) openjdk_local.py test

.PHONY: clean
clean:
	rm -rf -- build
