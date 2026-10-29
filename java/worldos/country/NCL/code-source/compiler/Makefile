PYTHON ?= python3
.PHONY: all test openjdk-build-local openjdk-test-local
all: build/calculRésultat

build/calculRésultat: tempsDeAnticipé.sh $(wildcard OutilJava/*) PriseEnChargeEnvironnementExécution.s démarrageLinux.s Exemples/calculRésultat.java
	sh tempsDeAnticipé.sh --target linux --entry calculRésultat.lancer -o $@ Exemples/calculRésultat.java

test: all
	$(PYTHON) -m unittest discover -s Tests -p 'test_*.py' -v

openjdk-build-local:
	$(PYTHON) openjdk_local.py build

openjdk-test-local:
	$(PYTHON) openjdk_local.py test

.PHONY: clean
clean:
	rm -rf -- build
