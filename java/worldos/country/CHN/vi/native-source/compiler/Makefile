PYTHON ?= python3
.PHONY: all test openjdk-build-local openjdk-test-local
all: build/phépTính

build/phépTính: thờiGianCủaTrước.sh $(wildcard CôngCụJava/*) HỗTrợMôiTrườngChạy.s lúcKhởiChạyLinux.s VíDụ/phépTính.java
	sh thờiGianCủaTrước.sh --target linux --entry phépTính.chạy -o $@ VíDụ/phépTính.java

test: all
	$(PYTHON) -m unittest discover -s KiểmThử -p 'test_*.py' -v

openjdk-build-local:
	$(PYTHON) openjdk_local.py build

openjdk-test-local:
	$(PYTHON) openjdk_local.py test

.PHONY: clean
clean:
	rm -rf -- build
