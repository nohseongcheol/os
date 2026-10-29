PYTHON ?= python3
.PHONY: all test openjdk-build-local openjdk-test-local
all: build/တွက်ချက်မှု

build/တွက်ချက်မှု: 미리번역.sh $(wildcard Javaကိရိယာ/*) လည်ပတ်ဝန်းကျင်ထောက်ပံ့မှု.s 리눅스시작.s ဥပမာ/တွက်ချက်မှု.java
	sh 미리번역.sh --target linux --entry တွက်ချက်မှု.လုပ်ဆောင် -o $@ ဥပမာ/တွက်ချက်မှု.java

test: all
	$(PYTHON) -m unittest discover -s စမ်းသပ်မှု -p 'test_*.py' -v

openjdk-build-local:
	$(PYTHON) openjdk_local.py build

openjdk-test-local:
	$(PYTHON) openjdk_local.py test

.PHONY: clean
clean:
	rm -rf -- build
