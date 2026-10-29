PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords la_distanță_conecta
remote: build
	$(PYTHON) Instrumente/executa_comandă.py --remote --resolution $(RESOLUTION) $(ARGS)
la_distanță_conecta: remote
test-remote: build
	$(PYTHON) Instrumente/원격접속시험.py
test-passwords: build
	$(PYTHON) Instrumente/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter rețea_Teanc -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Instrumente/generare_sistem.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Instrumente/COSL배포.py check
cosl-dist: build
	$(PYTHON) Instrumente/crea_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Instrumente/COSL배포.py bundle
	$(PYTHON) Instrumente/재연결시험.py
desktop: build
	$(PYTHON) Instrumente/executa_comandă.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Instrumente/셸시험.py
test-windows: build
	$(PYTHON) Instrumente/창시험.py
test-swing: build
	$(PYTHON) Instrumente/화면요소시험.py
test-stream: build
	$(PYTHON) Instrumente/흐름시험.py
test-ftp: build
	$(PYTHON) Instrumente/파일전송시험.py
test-elf: build
	$(PYTHON) Instrumente/실행파일시험.py
test-examples: build
	$(PYTHON) Instrumente/예제시험.py
network: build
	$(PYTHON) Instrumente/executa_comandă.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Instrumente/코딩시험.py
test-desktop: build
	$(PYTHON) Instrumente/바탕화면시험.py
run: build
	$(PYTHON) Instrumente/executa_comandă.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Instrumente/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Instrumente/한글입력시험.py
	$(PYTHON) Instrumente/셸시험.py
	$(PYTHON) Instrumente/바탕화면시험.py
	$(PYTHON) Instrumente/창시험.py
	$(PYTHON) Instrumente/화면요소시험.py
	$(PYTHON) Instrumente/흐름시험.py
	$(PYTHON) Instrumente/코딩시험.py
	$(PYTHON) Instrumente/자바가상기계시험.py
	$(PYTHON) Instrumente/부팅시험.py
	$(PYTHON) Instrumente/꾸러미시험.py
	$(PYTHON) Instrumente/해상도시험.py
	$(PYTHON) Instrumente/창크기시험.py
image: build
	$(PYTHON) Instrumente/crea_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Instrumente/exporta_SDK.py
sdk: build
	$(PYTHON) Instrumente/exporta_SDK.py

.PHONY: 모두 generare_sistem executa_comandă 시험 통신 desktop_vizualiza IMAGE_VALUE kit_de_dezvoltare
모두: all
generare_sistem: build
executa_comandă: run
시험: test
통신: network
desktop_vizualiza: desktop
IMAGE_VALUE: image
kit_de_dezvoltare: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Instrumente/부팅시험.py
test-remmina: build
	$(PYTHON) Instrumente/원격한글시험.py
test-naming:
	$(PYTHON) Instrumente/명명검사.py --C_Limbi_străine
	$(PYTHON) Instrumente/직접호출검사.py
	$(PYTHON) Instrumente/sursă_recenzie.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Instrumente/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Instrumente/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Instrumente/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Instrumente/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Instrumente/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Instrumente/실행계층점검.py

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
