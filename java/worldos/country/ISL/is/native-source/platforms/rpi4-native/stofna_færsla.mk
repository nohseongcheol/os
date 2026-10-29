PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords fjartengdur_TENGJA
remote: build
	$(PYTHON) Verkfæri/keyra_skipun.py --remote --resolution $(RESOLUTION) $(ARGS)
fjartengdur_TENGJA: remote
test-remote: build
	$(PYTHON) Verkfæri/원격접속시험.py
test-passwords: build
	$(PYTHON) Verkfæri/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Net_bunki -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Verkfæri/smíð_kerfi.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Verkfæri/COSL배포.py check
cosl-dist: build
	$(PYTHON) Verkfæri/stofna_mynd.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Verkfæri/COSL배포.py bundle
	$(PYTHON) Verkfæri/재연결시험.py
desktop: build
	$(PYTHON) Verkfæri/keyra_skipun.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Verkfæri/셸시험.py
test-windows: build
	$(PYTHON) Verkfæri/창시험.py
test-swing: build
	$(PYTHON) Verkfæri/화면요소시험.py
test-stream: build
	$(PYTHON) Verkfæri/흐름시험.py
test-ftp: build
	$(PYTHON) Verkfæri/파일전송시험.py
test-elf: build
	$(PYTHON) Verkfæri/실행파일시험.py
test-examples: build
	$(PYTHON) Verkfæri/예제시험.py
network: build
	$(PYTHON) Verkfæri/keyra_skipun.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Verkfæri/코딩시험.py
test-desktop: build
	$(PYTHON) Verkfæri/바탕화면시험.py
run: build
	$(PYTHON) Verkfæri/keyra_skipun.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Verkfæri/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Verkfæri/한글입력시험.py
	$(PYTHON) Verkfæri/셸시험.py
	$(PYTHON) Verkfæri/바탕화면시험.py
	$(PYTHON) Verkfæri/창시험.py
	$(PYTHON) Verkfæri/화면요소시험.py
	$(PYTHON) Verkfæri/흐름시험.py
	$(PYTHON) Verkfæri/코딩시험.py
	$(PYTHON) Verkfæri/자바가상기계시험.py
	$(PYTHON) Verkfæri/부팅시험.py
	$(PYTHON) Verkfæri/꾸러미시험.py
	$(PYTHON) Verkfæri/해상도시험.py
	$(PYTHON) Verkfæri/창크기시험.py
image: build
	$(PYTHON) Verkfæri/stofna_mynd.py --resolution $(RESOLUTION)
	$(PYTHON) Verkfæri/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Verkfæri/개발꾸러미내보내기.py

.PHONY: 모두 smíð_kerfi keyra_skipun 시험 통신 skjáborð_Sýn mynd_VALUE 개발꾸러미
모두: all
smíð_kerfi: build
keyra_skipun: run
시험: test
통신: network
skjáborð_Sýn: desktop
mynd_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Verkfæri/부팅시험.py
test-remmina: build
	$(PYTHON) Verkfæri/원격한글시험.py
test-naming:
	$(PYTHON) Verkfæri/명명검사.py --시언어
	$(PYTHON) Verkfæri/직접호출검사.py
	$(PYTHON) Verkfæri/uppruni_umsögn.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Verkfæri/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Verkfæri/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Verkfæri/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Verkfæri/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Verkfæri/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Verkfæri/실행계층점검.py

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
