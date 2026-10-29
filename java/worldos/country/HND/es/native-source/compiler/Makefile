PYTHON ?= python3
.PHONY: all test openjdk-build-local openjdk-test-local
all: build/resultadoCálculo

build/resultadoCálculo: tiempoDeAnticipado.sh $(wildcard HerramientaJava/*) SoporteEntornoEjecución.s inicioSistemaLinux.s Ejemplos/resultadoCálculo.java
	sh tiempoDeAnticipado.sh --target linux --entry resultadoCálculo.ponerEnMarcha -o $@ Ejemplos/resultadoCálculo.java

test: all
	$(PYTHON) -m unittest discover -s Pruebas -p 'test_*.py' -v

openjdk-build-local:
	$(PYTHON) openjdk_local.py build

openjdk-test-local:
	$(PYTHON) openjdk_local.py test

.PHONY: clean
clean:
	rm -rf -- build
