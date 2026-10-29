PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords pell_Cysylltu
remote: build
	$(PYTHON) Offer/Gweithredu_gorchymyn.py --remote --resolution $(RESOLUTION) $(ARGS)
pell_Cysylltu: remote
test-remote: build
	$(PYTHON) Offer/원격접속시험.py
test-passwords: build
	$(PYTHON) Offer/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Rhwydwaith_pentwr -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Offer/llunio_system.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Offer/COSL배포.py check
cosl-dist: build
	$(PYTHON) Offer/Creu_llun.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Offer/COSL배포.py bundle
	$(PYTHON) Offer/재연결시험.py
desktop: build
	$(PYTHON) Offer/Gweithredu_gorchymyn.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Offer/셸시험.py
test-windows: build
	$(PYTHON) Offer/창시험.py
test-swing: build
	$(PYTHON) Offer/화면요소시험.py
test-stream: build
	$(PYTHON) Offer/흐름시험.py
test-ftp: build
	$(PYTHON) Offer/파일전송시험.py
test-elf: build
	$(PYTHON) Offer/실행파일시험.py
test-examples: build
	$(PYTHON) Offer/예제시험.py
network: build
	$(PYTHON) Offer/Gweithredu_gorchymyn.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Offer/코딩시험.py
test-desktop: build
	$(PYTHON) Offer/바탕화면시험.py
run: build
	$(PYTHON) Offer/Gweithredu_gorchymyn.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Offer/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Offer/한글입력시험.py
	$(PYTHON) Offer/셸시험.py
	$(PYTHON) Offer/바탕화면시험.py
	$(PYTHON) Offer/창시험.py
	$(PYTHON) Offer/화면요소시험.py
	$(PYTHON) Offer/흐름시험.py
	$(PYTHON) Offer/코딩시험.py
	$(PYTHON) Offer/자바가상기계시험.py
	$(PYTHON) Offer/부팅시험.py
	$(PYTHON) Offer/꾸러미시험.py
	$(PYTHON) Offer/해상도시험.py
	$(PYTHON) Offer/창크기시험.py
image: build
	$(PYTHON) Offer/Creu_llun.py --resolution $(RESOLUTION)
	$(PYTHON) Offer/allgludo_SDK.py
sdk: build
	$(PYTHON) Offer/allgludo_SDK.py

.PHONY: 모두 llunio_system Gweithredu_gorchymyn 시험 통신 bwrdd_gwaith_Gwedd llun_VALUE 개발꾸러미
모두: all
llunio_system: build
Gweithredu_gorchymyn: run
시험: test
통신: network
bwrdd_gwaith_Gwedd: desktop
llun_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Offer/부팅시험.py
test-remmina: build
	$(PYTHON) Offer/원격한글시험.py
test-naming:
	$(PYTHON) Offer/명명검사.py --시언어
	$(PYTHON) Offer/직접호출검사.py
	$(PYTHON) Offer/ffynhonnell_adolygu.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Offer/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Offer/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Offer/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Offer/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Offer/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Offer/실행계층점검.py

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
