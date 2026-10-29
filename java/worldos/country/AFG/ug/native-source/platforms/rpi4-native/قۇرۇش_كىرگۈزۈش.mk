PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords يىراق_ئۇلاش
remote: build
	$(PYTHON) قوراللار/ئىجرا_قىلىش_بۇيرۇق.py --remote --resolution $(RESOLUTION) $(ARGS)
يىراق_ئۇلاش: remote
test-remote: build
	$(PYTHON) قوراللار/원격접속시험.py
test-passwords: build
	$(PYTHON) قوراللار/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter تور_دۆۋە -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) قوراللار/نۇسخا_سىستېما.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) قوراللار/COSL배포.py check
cosl-dist: build
	$(PYTHON) قوراللار/قۇرۇش_رەسىم.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) قوراللار/COSL배포.py bundle
	$(PYTHON) قوراللار/재연결시험.py
desktop: build
	$(PYTHON) قوراللار/ئىجرا_قىلىش_بۇيرۇق.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) قوراللار/셸시험.py
test-windows: build
	$(PYTHON) قوراللار/창시험.py
test-swing: build
	$(PYTHON) قوراللار/화면요소시험.py
test-stream: build
	$(PYTHON) قوراللار/흐름시험.py
test-ftp: build
	$(PYTHON) قوراللار/파일전송시험.py
test-elf: build
	$(PYTHON) قوراللار/실행파일시험.py
test-examples: build
	$(PYTHON) قوراللار/예제시험.py
network: build
	$(PYTHON) قوراللار/ئىجرا_قىلىش_بۇيرۇق.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) قوراللار/코딩시험.py
test-desktop: build
	$(PYTHON) قوراللار/바탕화면시험.py
run: build
	$(PYTHON) قوراللار/ئىجرا_قىلىش_بۇيرۇق.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) قوراللار/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) قوراللار/한글입력시험.py
	$(PYTHON) قوراللار/셸시험.py
	$(PYTHON) قوراللار/바탕화면시험.py
	$(PYTHON) قوراللار/창시험.py
	$(PYTHON) قوراللار/화면요소시험.py
	$(PYTHON) قوراللار/흐름시험.py
	$(PYTHON) قوراللار/코딩시험.py
	$(PYTHON) قوراللار/자바가상기계시험.py
	$(PYTHON) قوراللار/부팅시험.py
	$(PYTHON) قوراللار/꾸러미시험.py
	$(PYTHON) قوراللار/해상도시험.py
	$(PYTHON) قوراللار/창크기시험.py
image: build
	$(PYTHON) قوراللار/قۇرۇش_رەسىم.py --resolution $(RESOLUTION)
	$(PYTHON) قوراللار/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) قوراللار/개발꾸러미내보내기.py

.PHONY: 모두 نۇسخا_سىستېما ئىجرا_قىلىش_بۇيرۇق 시험 통신 ئۈستەليۈزى_كۆرۈنمە رەسىم_قىممىتى 개발꾸러미
모두: all
نۇسخا_سىستېما: build
ئىجرا_قىلىش_بۇيرۇق: run
시험: test
통신: network
ئۈستەليۈزى_كۆرۈنمە: desktop
رەسىم_قىممىتى: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) قوراللار/부팅시험.py
test-remmina: build
	$(PYTHON) قوراللار/원격한글시험.py
test-naming:
	$(PYTHON) قوراللار/명명검사.py --시언어
	$(PYTHON) قوراللار/직접호출검사.py
	$(PYTHON) قوراللار/مەنبە_تەكشۈرۈش.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) قوراللار/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) قوراللار/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) قوراللار/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) قوراللار/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) قوراللار/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) قوراللار/실행계층점검.py

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
