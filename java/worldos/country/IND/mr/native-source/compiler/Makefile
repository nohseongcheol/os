PYTHON ?= python3
.PHONY: all test openjdk-build-local openjdk-test-local
all: build/गणना

build/गणना: आगाऊ_संबंधित_वेळ.sh $(wildcard जावा_साधने/*) सामान्य_भाषा_रनटाइम_समर्थन.s लिनक्स_बूट.s उदाहरणे/गणना.java
	sh आगाऊ_संबंधित_वेळ.sh --target linux --entry गणना.सुरू_करा -o $@ उदाहरणे/गणना.java

test: all
	$(PYTHON) -m unittest discover -s चाचण्या -p 'test_*.py' -v

openjdk-build-local:
	$(PYTHON) openjdk_local.py build

openjdk-test-local:
	$(PYTHON) openjdk_local.py test

.PHONY: clean
clean:
	rm -rf -- build
