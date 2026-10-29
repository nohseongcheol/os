PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords urruneko_KONEKTATU
remote: build
	$(PYTHON) Tresnak/exekutatu_komando.py --remote --resolution $(RESOLUTION) $(ARGS)
urruneko_KONEKTATU: remote
test-remote: build
	$(PYTHON) Tresnak/원격접속시험.py
test-passwords: build
	$(PYTHON) Tresnak/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter sare_pila -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Tresnak/eraiki_sistema.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Tresnak/COSL배포.py check
cosl-dist: build
	$(PYTHON) Tresnak/sortu_irudi.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Tresnak/COSL배포.py bundle
	$(PYTHON) Tresnak/재연결시험.py
desktop: build
	$(PYTHON) Tresnak/exekutatu_komando.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Tresnak/셸시험.py
test-windows: build
	$(PYTHON) Tresnak/창시험.py
test-swing: build
	$(PYTHON) Tresnak/화면요소시험.py
test-stream: build
	$(PYTHON) Tresnak/흐름시험.py
test-ftp: build
	$(PYTHON) Tresnak/파일전송시험.py
test-elf: build
	$(PYTHON) Tresnak/실행파일시험.py
test-examples: build
	$(PYTHON) Tresnak/예제시험.py
network: build
	$(PYTHON) Tresnak/exekutatu_komando.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Tresnak/코딩시험.py
test-desktop: build
	$(PYTHON) Tresnak/바탕화면시험.py
run: build
	$(PYTHON) Tresnak/exekutatu_komando.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Tresnak/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Tresnak/한글입력시험.py
	$(PYTHON) Tresnak/셸시험.py
	$(PYTHON) Tresnak/바탕화면시험.py
	$(PYTHON) Tresnak/창시험.py
	$(PYTHON) Tresnak/화면요소시험.py
	$(PYTHON) Tresnak/흐름시험.py
	$(PYTHON) Tresnak/코딩시험.py
	$(PYTHON) Tresnak/자바가상기계시험.py
	$(PYTHON) Tresnak/부팅시험.py
	$(PYTHON) Tresnak/꾸러미시험.py
	$(PYTHON) Tresnak/해상도시험.py
	$(PYTHON) Tresnak/창크기시험.py
image: build
	$(PYTHON) Tresnak/sortu_irudi.py --resolution $(RESOLUTION)
	$(PYTHON) Tresnak/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Tresnak/개발꾸러미내보내기.py

.PHONY: 모두 eraiki_sistema exekutatu_komando 시험 통신 mahaigain_ikusi irudi_balio 개발꾸러미
모두: all
eraiki_sistema: build
exekutatu_komando: run
시험: test
통신: network
mahaigain_ikusi: desktop
irudi_balio: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Tresnak/부팅시험.py
test-remmina: build
	$(PYTHON) Tresnak/원격한글시험.py
test-naming:
	$(PYTHON) Tresnak/명명검사.py --시언어
	$(PYTHON) Tresnak/직접호출검사.py
	$(PYTHON) Tresnak/iturburu_iritzi.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Tresnak/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Tresnak/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Tresnak/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Tresnak/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Tresnak/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Tresnak/실행계층점검.py

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
