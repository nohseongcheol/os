PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords दुर्मीळ_कनॅक्ट
remote: build
	$(PYTHON) साधनां/पाळो_दिवचो_आदेश.py --remote --resolution $(RESOLUTION) $(ARGS)
दुर्मीळ_कनॅक्ट: remote
test-remote: build
	$(PYTHON) साधनां/원격접속시험.py
test-passwords: build
	$(PYTHON) साधनां/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter नॅटवर्क_स्टॅक -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) साधनां/दाळचे_प्रणाली.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) साधनां/COSL배포.py check
cosl-dist: build
	$(PYTHON) साधनां/निर्माण_करचें_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) साधनां/COSL배포.py bundle
	$(PYTHON) साधनां/재연결시험.py
desktop: build
	$(PYTHON) साधनां/पाळो_दिवचो_आदेश.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) साधनां/셸시험.py
test-windows: build
	$(PYTHON) साधनां/창시험.py
test-swing: build
	$(PYTHON) साधनां/화면요소시험.py
test-stream: build
	$(PYTHON) साधनां/흐름시험.py
test-ftp: build
	$(PYTHON) साधनां/파일전송시험.py
test-elf: build
	$(PYTHON) साधनां/실행파일시험.py
test-examples: build
	$(PYTHON) साधनां/예제시험.py
network: build
	$(PYTHON) साधनां/पाळो_दिवचो_आदेश.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) साधनां/코딩시험.py
test-desktop: build
	$(PYTHON) साधनां/바탕화면시험.py
run: build
	$(PYTHON) साधनां/पाळो_दिवचो_आदेश.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) साधनां/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) साधनां/한글입력시험.py
	$(PYTHON) साधनां/셸시험.py
	$(PYTHON) साधनां/바탕화면시험.py
	$(PYTHON) साधनां/창시험.py
	$(PYTHON) साधनां/화면요소시험.py
	$(PYTHON) साधनां/흐름시험.py
	$(PYTHON) साधनां/코딩시험.py
	$(PYTHON) साधनां/자바가상기계시험.py
	$(PYTHON) साधनां/부팅시험.py
	$(PYTHON) साधनां/꾸러미시험.py
	$(PYTHON) साधनां/해상도시험.py
	$(PYTHON) साधनां/창크기시험.py
image: build
	$(PYTHON) साधनां/निर्माण_करचें_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) साधनां/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) साधनां/개발꾸러미내보내기.py

.PHONY: 모두 दाळचे_प्रणाली पाळो_दिवचो_आदेश 시험 통신 डॅस्कटॉप_दृश्य IMAGE_मोल 개발꾸러미
모두: all
दाळचे_प्रणाली: build
पाळो_दिवचो_आदेश: run
시험: test
통신: network
डॅस्कटॉप_दृश्य: desktop
IMAGE_मोल: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) साधनां/부팅시험.py
test-remmina: build
	$(PYTHON) साधनां/원격한글시험.py
test-naming:
	$(PYTHON) साधनां/명명검사.py --시언어
	$(PYTHON) साधनां/직접호출검사.py
	$(PYTHON) साधनां/स्त्रोत_नियाळ.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) साधनां/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) साधनां/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) साधनां/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) साधनां/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) साधनां/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) साधनां/실행계층점검.py

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
