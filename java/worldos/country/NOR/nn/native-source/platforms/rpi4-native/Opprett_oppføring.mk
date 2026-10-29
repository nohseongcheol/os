PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords fjern_KOPLE_TIL
remote: build
	$(PYTHON) Verktøy/Utfør_kommando.py --remote --resolution $(RESOLUTION) $(ARGS)
fjern_KOPLE_TIL: remote
test-remote: build
	$(PYTHON) Verktøy/원격접속시험.py
test-passwords: build
	$(PYTHON) Verktøy/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Nettverk_Stabel -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Verktøy/bygg_system.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Verktøy/COSL배포.py check
cosl-dist: build
	$(PYTHON) Verktøy/Opprett_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Verktøy/COSL배포.py bundle
	$(PYTHON) Verktøy/재연결시험.py
desktop: build
	$(PYTHON) Verktøy/Utfør_kommando.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Verktøy/셸시험.py
test-windows: build
	$(PYTHON) Verktøy/창시험.py
test-swing: build
	$(PYTHON) Verktøy/화면요소시험.py
test-stream: build
	$(PYTHON) Verktøy/흐름시험.py
test-ftp: build
	$(PYTHON) Verktøy/파일전송시험.py
test-elf: build
	$(PYTHON) Verktøy/실행파일시험.py
test-examples: build
	$(PYTHON) Verktøy/예제시험.py
network: build
	$(PYTHON) Verktøy/Utfør_kommando.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Verktøy/코딩시험.py
test-desktop: build
	$(PYTHON) Verktøy/바탕화면시험.py
run: build
	$(PYTHON) Verktøy/Utfør_kommando.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Verktøy/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Verktøy/한글입력시험.py
	$(PYTHON) Verktøy/셸시험.py
	$(PYTHON) Verktøy/바탕화면시험.py
	$(PYTHON) Verktøy/창시험.py
	$(PYTHON) Verktøy/화면요소시험.py
	$(PYTHON) Verktøy/흐름시험.py
	$(PYTHON) Verktøy/코딩시험.py
	$(PYTHON) Verktøy/자바가상기계시험.py
	$(PYTHON) Verktøy/부팅시험.py
	$(PYTHON) Verktøy/꾸러미시험.py
	$(PYTHON) Verktøy/해상도시험.py
	$(PYTHON) Verktøy/창크기시험.py
image: build
	$(PYTHON) Verktøy/Opprett_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Verktøy/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Verktøy/개발꾸러미내보내기.py

.PHONY: 모두 bygg_system Utfør_kommando 시험 통신 stasjonær_vise IMAGE_VALUE 개발꾸러미
모두: all
bygg_system: build
Utfør_kommando: run
시험: test
통신: network
stasjonær_vise: desktop
IMAGE_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Verktøy/부팅시험.py
test-remmina: build
	$(PYTHON) Verktøy/원격한글시험.py
test-naming:
	$(PYTHON) Verktøy/명명검사.py --시언어
	$(PYTHON) Verktøy/직접호출검사.py
	$(PYTHON) Verktøy/kjelde_omtale.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Verktøy/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Verktøy/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Verktøy/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Verktøy/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Verktøy/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Verktøy/실행계층점검.py

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
