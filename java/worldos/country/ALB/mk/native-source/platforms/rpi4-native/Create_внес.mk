PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords далечинскo_ПОВРЗИ
remote: build
	$(PYTHON) Алатки/Изврши_наредба.py --remote --resolution $(RESOLUTION) $(ARGS)
далечинскo_ПОВРЗИ: remote
test-remote: build
	$(PYTHON) Алатки/원격접속시험.py
test-passwords: build
	$(PYTHON) Алатки/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Мрежа_Купче -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Алатки/верзија_систем.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Алатки/COSL배포.py check
cosl-dist: build
	$(PYTHON) Алатки/Create_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Алатки/COSL배포.py bundle
	$(PYTHON) Алатки/재연결시험.py
desktop: build
	$(PYTHON) Алатки/Изврши_наредба.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Алатки/셸시험.py
test-windows: build
	$(PYTHON) Алатки/창시험.py
test-swing: build
	$(PYTHON) Алатки/화면요소시험.py
test-stream: build
	$(PYTHON) Алатки/흐름시험.py
test-ftp: build
	$(PYTHON) Алатки/파일전송시험.py
test-elf: build
	$(PYTHON) Алатки/실행파일시험.py
test-examples: build
	$(PYTHON) Алатки/예제시험.py
network: build
	$(PYTHON) Алатки/Изврши_наредба.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Алатки/코딩시험.py
test-desktop: build
	$(PYTHON) Алатки/바탕화면시험.py
run: build
	$(PYTHON) Алатки/Изврши_наредба.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Алатки/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Алатки/한글입력시험.py
	$(PYTHON) Алатки/셸시험.py
	$(PYTHON) Алатки/바탕화면시험.py
	$(PYTHON) Алатки/창시험.py
	$(PYTHON) Алатки/화면요소시험.py
	$(PYTHON) Алатки/흐름시험.py
	$(PYTHON) Алатки/코딩시험.py
	$(PYTHON) Алатки/자바가상기계시험.py
	$(PYTHON) Алатки/부팅시험.py
	$(PYTHON) Алатки/꾸러미시험.py
	$(PYTHON) Алатки/해상도시험.py
	$(PYTHON) Алатки/창크기시험.py
image: build
	$(PYTHON) Алатки/Create_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Алатки/извези_SDK.py
sdk: build
	$(PYTHON) Алатки/извези_SDK.py

.PHONY: 모두 верзија_систем Изврши_наредба 시험 통신 десктоп_Приказ IMAGE_VALUE 개발꾸러미
모두: all
верзија_систем: build
Изврши_наредба: run
시험: test
통신: network
десктоп_Приказ: desktop
IMAGE_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Алатки/부팅시험.py
test-remmina: build
	$(PYTHON) Алатки/원격한글시험.py
test-naming:
	$(PYTHON) Алатки/명명검사.py --시언어
	$(PYTHON) Алатки/직접호출검사.py
	$(PYTHON) Алатки/извор_прегледај.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Алатки/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Алатки/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Алатки/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Алатки/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Алатки/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Алатки/실행계층점검.py

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
