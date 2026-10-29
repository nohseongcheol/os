PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords kgakala_Golaganya
remote: build
	$(PYTHON) Thuluse/diragatsa_Taelo.py --remote --resolution $(RESOLUTION) $(ARGS)
kgakala_Golaganya: remote
test-remote: build
	$(PYTHON) Thuluse/원격접속시험.py
test-passwords: build
	$(PYTHON) Thuluse/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Neteweke_kokoanyodinepe -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Thuluse/aga_tsamaiso.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Thuluse/COSL배포.py check
cosl-dist: build
	$(PYTHON) Thuluse/tlhama_Setshwantsho.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Thuluse/COSL배포.py bundle
	$(PYTHON) Thuluse/재연결시험.py
desktop: build
	$(PYTHON) Thuluse/diragatsa_Taelo.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Thuluse/셸시험.py
test-windows: build
	$(PYTHON) Thuluse/창시험.py
test-swing: build
	$(PYTHON) Thuluse/화면요소시험.py
test-stream: build
	$(PYTHON) Thuluse/흐름시험.py
test-ftp: build
	$(PYTHON) Thuluse/파일전송시험.py
test-elf: build
	$(PYTHON) Thuluse/실행파일시험.py
test-examples: build
	$(PYTHON) Thuluse/예제시험.py
network: build
	$(PYTHON) Thuluse/diragatsa_Taelo.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Thuluse/코딩시험.py
test-desktop: build
	$(PYTHON) Thuluse/바탕화면시험.py
run: build
	$(PYTHON) Thuluse/diragatsa_Taelo.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Thuluse/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Thuluse/한글입력시험.py
	$(PYTHON) Thuluse/셸시험.py
	$(PYTHON) Thuluse/바탕화면시험.py
	$(PYTHON) Thuluse/창시험.py
	$(PYTHON) Thuluse/화면요소시험.py
	$(PYTHON) Thuluse/흐름시험.py
	$(PYTHON) Thuluse/코딩시험.py
	$(PYTHON) Thuluse/자바가상기계시험.py
	$(PYTHON) Thuluse/부팅시험.py
	$(PYTHON) Thuluse/꾸러미시험.py
	$(PYTHON) Thuluse/해상도시험.py
	$(PYTHON) Thuluse/창크기시험.py
image: build
	$(PYTHON) Thuluse/tlhama_Setshwantsho.py --resolution $(RESOLUTION)
	$(PYTHON) Thuluse/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Thuluse/개발꾸러미내보내기.py

.PHONY: 모두 aga_tsamaiso diragatsa_Taelo 시험 통신 desekethopo_Tebego Setshwantsho_Boleng 개발꾸러미
모두: all
aga_tsamaiso: build
diragatsa_Taelo: run
시험: test
통신: network
desekethopo_Tebego: desktop
Setshwantsho_Boleng: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Thuluse/부팅시험.py
test-remmina: build
	$(PYTHON) Thuluse/원격한글시험.py
test-naming:
	$(PYTHON) Thuluse/명명검사.py --시언어
	$(PYTHON) Thuluse/직접호출검사.py
	$(PYTHON) Thuluse/Motswedi_tshekatsheko.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Thuluse/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Thuluse/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Thuluse/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Thuluse/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Thuluse/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Thuluse/실행계층점검.py

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
