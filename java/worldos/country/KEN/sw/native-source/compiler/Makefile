PYTHON ?= python3
.PHONY: all test openjdk-build-local openjdk-test-local
all: build/계산

build/계산: 미리번역.sh $(wildcard 자바도구/*) muda_wa_kuendesha_lugha_ya_kawaida_Auni.s 리눅스시작.s 예제/계산.java
	sh 미리번역.sh --target linux --entry 계산.endesha -o $@ 예제/계산.java

test: all
	$(PYTHON) -m unittest discover -s 시험 -p 'test_*.py' -v

openjdk-build-local:
	$(PYTHON) openjdk_local.py build

openjdk-test-local:
	$(PYTHON) openjdk_local.py test

.PHONY: clean
clean:
	rm -rf -- build
