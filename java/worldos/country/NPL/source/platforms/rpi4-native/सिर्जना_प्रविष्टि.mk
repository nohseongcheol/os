PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords दूर_कनेक्ट
remote: build
	$(PYTHON) उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py --remote --resolution $(RESOLUTION) $(ARGS)
दूर_कनेक्ट: remote
test-remote: build
	$(PYTHON) उपकरणहरू/원격접속시험.py
test-passwords: build
	$(PYTHON) उपकरणहरू/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter सञ्जाल_चाङ -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) उपकरणहरू/बनाउनुहोस्_प्रणाली.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) उपकरणहरू/COSL배포.py check
cosl-dist: build
	$(PYTHON) उपकरणहरू/सिर्जना_छवि.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) उपकरणहरू/COSL배포.py bundle
	$(PYTHON) उपकरणहरू/재연결시험.py
desktop: build
	$(PYTHON) उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) उपकरणहरू/셸시험.py
test-windows: build
	$(PYTHON) उपकरणहरू/창시험.py
test-swing: build
	$(PYTHON) उपकरणहरू/화면요소시험.py
test-stream: build
	$(PYTHON) उपकरणहरू/흐름시험.py
test-ftp: build
	$(PYTHON) उपकरणहरू/파일전송시험.py
test-elf: build
	$(PYTHON) उपकरणहरू/실행파일시험.py
test-examples: build
	$(PYTHON) उपकरणहरू/예제시험.py
network: build
	$(PYTHON) उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) उपकरणहरू/코딩시험.py
test-desktop: build
	$(PYTHON) उपकरणहरू/바탕화면시험.py
run: build
	$(PYTHON) उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) उपकरणहरू/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) उपकरणहरू/한글입력시험.py
	$(PYTHON) उपकरणहरू/셸시험.py
	$(PYTHON) उपकरणहरू/바탕화면시험.py
	$(PYTHON) उपकरणहरू/창시험.py
	$(PYTHON) उपकरणहरू/화면요소시험.py
	$(PYTHON) उपकरणहरू/흐름시험.py
	$(PYTHON) उपकरणहरू/코딩시험.py
	$(PYTHON) उपकरणहरू/자바가상기계시험.py
	$(PYTHON) उपकरणहरू/부팅시험.py
	$(PYTHON) उपकरणहरू/꾸러미시험.py
	$(PYTHON) उपकरणहरू/해상도시험.py
	$(PYTHON) उपकरणहरू/창크기시험.py
image: build
	$(PYTHON) उपकरणहरू/सिर्जना_छवि.py --resolution $(RESOLUTION)
	$(PYTHON) उपकरणहरू/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) उपकरणहरू/개발꾸러미내보내기.py

.PHONY: 모두 बनाउनुहोस्_प्रणाली कार्यान्वयन_गर्नुहोस्_आदेश 시험 통신 डेस्कटप_दृश्य छवि_मान 개발꾸러미
모두: all
बनाउनुहोस्_प्रणाली: build
कार्यान्वयन_गर्नुहोस्_आदेश: run
시험: test
통신: network
डेस्कटप_दृश्य: desktop
छवि_मान: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) उपकरणहरू/부팅시험.py
test-remmina: build
	$(PYTHON) उपकरणहरू/원격한글시험.py
test-naming:
	$(PYTHON) उपकरणहरू/명명검사.py --시언어
	$(PYTHON) उपकरणहरू/직접호출검사.py
	$(PYTHON) उपकरणहरू/स्रोत_समीक्षा.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) उपकरणहरू/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) उपकरणहरू/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) उपकरणहरू/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) उपकरणहरू/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) उपकरणहरू/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) उपकरणहरू/실행계층점검.py

.PHONY: clean
clean:
	# Keep device credentials and downloaded packages.
	@if test -d build/remote; then \
		find build/remote -mindepth 1 -maxdepth 1 ! -name access.json ! -name host-key.der -exec rm -rf -- {} +; \
	fi
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name remote ! -name pip-cache -exec rm -rf -- {} +; \
	fi
	rm -rf -- dist
