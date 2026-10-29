PYTHON ?= python3
.PHONY: all test openjdk-build-local openjdk-test-local
all: build/計算結果

build/計算結果: 事前用時間.sh $(wildcard Java道具/*) 実行環境支援.s Linux始動.s 用例/計算結果.java
	sh 事前用時間.sh --target linux --entry 計算結果.起動処理 -o $@ 用例/計算結果.java

test: all
	$(PYTHON) -m unittest discover -s 試験 -p 'test_*.py' -v

openjdk-build-local:
	$(PYTHON) openjdk_local.py build

openjdk-test-local:
	$(PYTHON) openjdk_local.py test

.PHONY: clean
clean:
	rm -rf -- build
