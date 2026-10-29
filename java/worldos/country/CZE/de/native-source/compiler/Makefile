PYTHON ?= python3
.PHONY: all test openjdk-build-local openjdk-test-local
all: build/berechnung

build/berechnung: vorabVonElementZeit.sh $(wildcard JavaWerkzeug/*) LaufzeitUnterstützung.s linuxAnlauf.s Beispiele/berechnung.java
	sh vorabVonElementZeit.sh --target linux --entry berechnung.ausführenVorgang -o $@ Beispiele/berechnung.java

test: all
	$(PYTHON) -m unittest discover -s Prüfungen -p 'test_*.py' -v

openjdk-build-local:
	$(PYTHON) openjdk_local.py build

openjdk-test-local:
	$(PYTHON) openjdk_local.py test

.PHONY: clean
clean:
	rm -rf -- build
