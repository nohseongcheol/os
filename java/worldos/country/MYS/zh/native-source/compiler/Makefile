PYTHON ?= python3
.PHONY: all test openjdk-build-local openjdk-test-local
all: build/计算结果

build/计算结果: 提前所属时间.sh $(wildcard Java工具/*) 运行时支持.s Linux启动.s 用例/计算结果.java
	sh 提前所属时间.sh --target linux --entry 计算结果.运行 -o $@ 用例/计算结果.java

test: all
	$(PYTHON) -m unittest discover -s 测试 -p 'test_*.py' -v

openjdk-build-local:
	$(PYTHON) openjdk_local.py build

openjdk-test-local:
	$(PYTHON) openjdk_local.py test

.PHONY: clean
clean:
	rm -rf -- build
