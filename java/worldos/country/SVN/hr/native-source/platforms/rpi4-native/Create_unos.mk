PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords udaljeno_CONNECT
remote: build
	$(PYTHON) Alati/Izvrši_naredba.py --remote --resolution $(RESOLUTION) $(ARGS)
udaljeno_CONNECT: remote
test-remote: build
	$(PYTHON) Alati/원격접속시험.py
test-passwords: build
	$(PYTHON) Alati/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter mreža_hrpa -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Alati/međuverzija_sustav.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Alati/COSL배포.py check
cosl-dist: build
	$(PYTHON) Alati/Create_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Alati/COSL배포.py bundle
	$(PYTHON) Alati/재연결시험.py
desktop: build
	$(PYTHON) Alati/Izvrši_naredba.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Alati/셸시험.py
test-windows: build
	$(PYTHON) Alati/창시험.py
test-swing: build
	$(PYTHON) Alati/화면요소시험.py
test-stream: build
	$(PYTHON) Alati/흐름시험.py
test-ftp: build
	$(PYTHON) Alati/파일전송시험.py
test-elf: build
	$(PYTHON) Alati/실행파일시험.py
test-examples: build
	$(PYTHON) Alati/예제시험.py
network: build
	$(PYTHON) Alati/Izvrši_naredba.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Alati/코딩시험.py
test-desktop: build
	$(PYTHON) Alati/바탕화면시험.py
run: build
	$(PYTHON) Alati/Izvrši_naredba.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Alati/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Alati/한글입력시험.py
	$(PYTHON) Alati/셸시험.py
	$(PYTHON) Alati/바탕화면시험.py
	$(PYTHON) Alati/창시험.py
	$(PYTHON) Alati/화면요소시험.py
	$(PYTHON) Alati/흐름시험.py
	$(PYTHON) Alati/코딩시험.py
	$(PYTHON) Alati/자바가상기계시험.py
	$(PYTHON) Alati/부팅시험.py
	$(PYTHON) Alati/꾸러미시험.py
	$(PYTHON) Alati/해상도시험.py
	$(PYTHON) Alati/창크기시험.py
image: build
	$(PYTHON) Alati/Create_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Alati/izvezi_SDK.py
sdk: build
	$(PYTHON) Alati/izvezi_SDK.py

.PHONY: 모두 međuverzija_sustav Izvrši_naredba 시험 통신 stolni_Prikaz IMAGE_VALUE set_razvojnih_alata
모두: all
međuverzija_sustav: build
Izvrši_naredba: run
시험: test
통신: network
stolni_Prikaz: desktop
IMAGE_VALUE: image
set_razvojnih_alata: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Alati/부팅시험.py
test-remmina: build
	$(PYTHON) Alati/원격한글시험.py
test-naming:
	$(PYTHON) Alati/명명검사.py --C_Jezik
	$(PYTHON) Alati/직접호출검사.py
	$(PYTHON) Alati/izvor_osvrt.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Alati/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Alati/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Alati/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Alati/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Alati/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Alati/실행계층점검.py

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
