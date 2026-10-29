PYTHON ?= python3
.PHONY: all test openjdk-build-local openjdk-test-local
all: build/計算結果

build/計算結果: 提前所屬時間.sh $(wildcard Java工具/*) 運行時支持.s Linux啓動.s 範例/計算結果.java
	sh 提前所屬時間.sh --target linux --entry 計算結果.運行 -o $@ 範例/計算結果.java

test: all
	$(PYTHON) -m unittest discover -s 測試 -p 'test_*.py' -v

openjdk-build-local:
	$(PYTHON) openjdk_local.py build

openjdk-test-local:
	$(PYTHON) openjdk_local.py test

.PHONY: clean
clean:
	rm -rf -- build
