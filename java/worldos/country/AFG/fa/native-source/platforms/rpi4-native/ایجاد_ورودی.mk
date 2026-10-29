PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords راه_دور_اتصال
remote: build
	$(PYTHON) ابزارها/اجرا_فرمان.py --remote --resolution $(RESOLUTION) $(ARGS)
راه_دور_اتصال: remote
test-remote: build
	$(PYTHON) ابزارها/원격접속시험.py
test-passwords: build
	$(PYTHON) ابزارها/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter شبکه_پشته -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ابزارها/ساخت_سیستم.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ابزارها/COSL배포.py check
cosl-dist: build
	$(PYTHON) ابزارها/ایجاد_عکس.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ابزارها/COSL배포.py bundle
	$(PYTHON) ابزارها/재연결시험.py
desktop: build
	$(PYTHON) ابزارها/اجرا_فرمان.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ابزارها/셸시험.py
test-windows: build
	$(PYTHON) ابزارها/창시험.py
test-swing: build
	$(PYTHON) ابزارها/화면요소시험.py
test-stream: build
	$(PYTHON) ابزارها/흐름시험.py
test-ftp: build
	$(PYTHON) ابزارها/파일전송시험.py
test-elf: build
	$(PYTHON) ابزارها/실행파일시험.py
test-examples: build
	$(PYTHON) ابزارها/예제시험.py
network: build
	$(PYTHON) ابزارها/اجرا_فرمان.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ابزارها/코딩시험.py
test-desktop: build
	$(PYTHON) ابزارها/바탕화면시험.py
run: build
	$(PYTHON) ابزارها/اجرا_فرمان.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ابزارها/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ابزارها/한글입력시험.py
	$(PYTHON) ابزارها/셸시험.py
	$(PYTHON) ابزارها/바탕화면시험.py
	$(PYTHON) ابزارها/창시험.py
	$(PYTHON) ابزارها/화면요소시험.py
	$(PYTHON) ابزارها/흐름시험.py
	$(PYTHON) ابزارها/코딩시험.py
	$(PYTHON) ابزارها/자바가상기계시험.py
	$(PYTHON) ابزارها/부팅시험.py
	$(PYTHON) ابزارها/꾸러미시험.py
	$(PYTHON) ابزارها/해상도시험.py
	$(PYTHON) ابزارها/창크기시험.py
image: build
	$(PYTHON) ابزارها/ایجاد_عکس.py --resolution $(RESOLUTION)
	$(PYTHON) ابزارها/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ابزارها/개발꾸러미내보내기.py

.PHONY: 모두 ساخت_سیستم اجرا_فرمان 시험 통신 رایانه_نما عکس_مقدار 개발꾸러미
모두: all
ساخت_سیستم: build
اجرا_فرمان: run
시험: test
통신: network
رایانه_نما: desktop
عکس_مقدار: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ابزارها/부팅시험.py
test-remmina: build
	$(PYTHON) ابزارها/원격한글시험.py
test-naming:
	$(PYTHON) ابزارها/명명검사.py --시언어
	$(PYTHON) ابزارها/직접호출검사.py
	$(PYTHON) ابزارها/منبع_بررسی.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ابزارها/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ابزارها/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ابزارها/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ابزارها/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ابزارها/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ابزارها/실행계층점검.py

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
