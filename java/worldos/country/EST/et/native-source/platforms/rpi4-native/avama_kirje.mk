PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords kauge_Ühenda
remote: build
	$(PYTHON) Tööriistad/Täida_käsk.py --remote --resolution $(RESOLUTION) $(ARGS)
kauge_Ühenda: remote
test-remote: build
	$(PYTHON) Tööriistad/원격접속시험.py
test-passwords: build
	$(PYTHON) Tööriistad/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter võrk_Virn -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Tööriistad/järk_süsteem.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Tööriistad/COSL배포.py check
cosl-dist: build
	$(PYTHON) Tööriistad/avama_pilt.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Tööriistad/COSL배포.py bundle
	$(PYTHON) Tööriistad/재연결시험.py
desktop: build
	$(PYTHON) Tööriistad/Täida_käsk.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Tööriistad/셸시험.py
test-windows: build
	$(PYTHON) Tööriistad/창시험.py
test-swing: build
	$(PYTHON) Tööriistad/화면요소시험.py
test-stream: build
	$(PYTHON) Tööriistad/흐름시험.py
test-ftp: build
	$(PYTHON) Tööriistad/파일전송시험.py
test-elf: build
	$(PYTHON) Tööriistad/실행파일시험.py
test-examples: build
	$(PYTHON) Tööriistad/예제시험.py
network: build
	$(PYTHON) Tööriistad/Täida_käsk.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Tööriistad/코딩시험.py
test-desktop: build
	$(PYTHON) Tööriistad/바탕화면시험.py
run: build
	$(PYTHON) Tööriistad/Täida_käsk.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Tööriistad/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Tööriistad/한글입력시험.py
	$(PYTHON) Tööriistad/셸시험.py
	$(PYTHON) Tööriistad/바탕화면시험.py
	$(PYTHON) Tööriistad/창시험.py
	$(PYTHON) Tööriistad/화면요소시험.py
	$(PYTHON) Tööriistad/흐름시험.py
	$(PYTHON) Tööriistad/코딩시험.py
	$(PYTHON) Tööriistad/자바가상기계시험.py
	$(PYTHON) Tööriistad/부팅시험.py
	$(PYTHON) Tööriistad/꾸러미시험.py
	$(PYTHON) Tööriistad/해상도시험.py
	$(PYTHON) Tööriistad/창크기시험.py
image: build
	$(PYTHON) Tööriistad/avama_pilt.py --resolution $(RESOLUTION)
	$(PYTHON) Tööriistad/eksportima_SDK.py
sdk: build
	$(PYTHON) Tööriistad/eksportima_SDK.py

.PHONY: 모두 järk_süsteem Täida_käsk 시험 통신 töölaud_Kuva pilt_VALUE arenduskomplekt
모두: all
järk_süsteem: build
Täida_käsk: run
시험: test
통신: network
töölaud_Kuva: desktop
pilt_VALUE: image
arenduskomplekt: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Tööriistad/부팅시험.py
test-remmina: build
	$(PYTHON) Tööriistad/원격한글시험.py
test-naming:
	$(PYTHON) Tööriistad/명명검사.py --_15_Keeled
	$(PYTHON) Tööriistad/직접호출검사.py
	$(PYTHON) Tööriistad/lähe_arvustus.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Tööriistad/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Tööriistad/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Tööriistad/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Tööriistad/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Tööriistad/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Tööriistad/실행계층점검.py

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
