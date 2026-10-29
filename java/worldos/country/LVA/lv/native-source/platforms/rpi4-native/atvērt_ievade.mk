PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords attāls_saziņa
remote: build
	$(PYTHON) Rīki/Izpildīt_komanda.py --remote --resolution $(RESOLUTION) $(ARGS)
attāls_saziņa: remote
test-remote: build
	$(PYTHON) Rīki/원격접속시험.py
test-passwords: build
	$(PYTHON) Rīki/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter tīkls_kopa -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Rīki/būvējums_sistēma.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Rīki/COSL배포.py check
cosl-dist: build
	$(PYTHON) Rīki/atvērt_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Rīki/COSL배포.py bundle
	$(PYTHON) Rīki/재연결시험.py
desktop: build
	$(PYTHON) Rīki/Izpildīt_komanda.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Rīki/셸시험.py
test-windows: build
	$(PYTHON) Rīki/창시험.py
test-swing: build
	$(PYTHON) Rīki/화면요소시험.py
test-stream: build
	$(PYTHON) Rīki/흐름시험.py
test-ftp: build
	$(PYTHON) Rīki/파일전송시험.py
test-elf: build
	$(PYTHON) Rīki/실행파일시험.py
test-examples: build
	$(PYTHON) Rīki/예제시험.py
network: build
	$(PYTHON) Rīki/Izpildīt_komanda.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Rīki/코딩시험.py
test-desktop: build
	$(PYTHON) Rīki/바탕화면시험.py
run: build
	$(PYTHON) Rīki/Izpildīt_komanda.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Rīki/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Rīki/한글입력시험.py
	$(PYTHON) Rīki/셸시험.py
	$(PYTHON) Rīki/바탕화면시험.py
	$(PYTHON) Rīki/창시험.py
	$(PYTHON) Rīki/화면요소시험.py
	$(PYTHON) Rīki/흐름시험.py
	$(PYTHON) Rīki/코딩시험.py
	$(PYTHON) Rīki/자바가상기계시험.py
	$(PYTHON) Rīki/부팅시험.py
	$(PYTHON) Rīki/꾸러미시험.py
	$(PYTHON) Rīki/해상도시험.py
	$(PYTHON) Rīki/창크기시험.py
image: build
	$(PYTHON) Rīki/atvērt_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Rīki/eksportēt_SDK.py
sdk: build
	$(PYTHON) Rīki/eksportēt_SDK.py

.PHONY: 모두 būvējums_sistēma Izpildīt_komanda 시험 통신 dators_Skats IMAGE_VALUE programmizstrādes_komplekts
모두: all
būvējums_sistēma: build
Izpildīt_komanda: run
시험: test
통신: network
dators_Skats: desktop
IMAGE_VALUE: image
programmizstrādes_komplekts: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Rīki/부팅시험.py
test-remmina: build
	$(PYTHON) Rīki/원격한글시험.py
test-naming:
	$(PYTHON) Rīki/명명검사.py --C_Valodas
	$(PYTHON) Rīki/직접호출검사.py
	$(PYTHON) Rīki/avots_atsauksme.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Rīki/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Rīki/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Rīki/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Rīki/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Rīki/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Rīki/실행계층점검.py

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
