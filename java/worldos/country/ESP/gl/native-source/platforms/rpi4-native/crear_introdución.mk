PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords remoto_CONECTAR
remote: build
	$(PYTHON) Ferramentas/executar_comando.py --remote --resolution $(RESOLUTION) $(ARGS)
remoto_CONECTAR: remote
test-remote: build
	$(PYTHON) Ferramentas/원격접속시험.py
test-passwords: build
	$(PYTHON) Ferramentas/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Rede_Montón -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Ferramentas/compilar_sistema.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Ferramentas/COSL배포.py check
cosl-dist: build
	$(PYTHON) Ferramentas/crear_IMAXE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Ferramentas/COSL배포.py bundle
	$(PYTHON) Ferramentas/재연결시험.py
desktop: build
	$(PYTHON) Ferramentas/executar_comando.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Ferramentas/셸시험.py
test-windows: build
	$(PYTHON) Ferramentas/창시험.py
test-swing: build
	$(PYTHON) Ferramentas/화면요소시험.py
test-stream: build
	$(PYTHON) Ferramentas/흐름시험.py
test-ftp: build
	$(PYTHON) Ferramentas/파일전송시험.py
test-elf: build
	$(PYTHON) Ferramentas/실행파일시험.py
test-examples: build
	$(PYTHON) Ferramentas/예제시험.py
network: build
	$(PYTHON) Ferramentas/executar_comando.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Ferramentas/코딩시험.py
test-desktop: build
	$(PYTHON) Ferramentas/바탕화면시험.py
run: build
	$(PYTHON) Ferramentas/executar_comando.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Ferramentas/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Ferramentas/한글입력시험.py
	$(PYTHON) Ferramentas/셸시험.py
	$(PYTHON) Ferramentas/바탕화면시험.py
	$(PYTHON) Ferramentas/창시험.py
	$(PYTHON) Ferramentas/화면요소시험.py
	$(PYTHON) Ferramentas/흐름시험.py
	$(PYTHON) Ferramentas/코딩시험.py
	$(PYTHON) Ferramentas/자바가상기계시험.py
	$(PYTHON) Ferramentas/부팅시험.py
	$(PYTHON) Ferramentas/꾸러미시험.py
	$(PYTHON) Ferramentas/해상도시험.py
	$(PYTHON) Ferramentas/창크기시험.py
image: build
	$(PYTHON) Ferramentas/crear_IMAXE.py --resolution $(RESOLUTION)
	$(PYTHON) Ferramentas/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Ferramentas/개발꾸러미내보내기.py

.PHONY: 모두 compilar_sistema executar_comando 시험 통신 escritorio_ver IMAXE_VALOR 개발꾸러미
모두: all
compilar_sistema: build
executar_comando: run
시험: test
통신: network
escritorio_ver: desktop
IMAXE_VALOR: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Ferramentas/부팅시험.py
test-remmina: build
	$(PYTHON) Ferramentas/원격한글시험.py
test-naming:
	$(PYTHON) Ferramentas/명명검사.py --시언어
	$(PYTHON) Ferramentas/직접호출검사.py
	$(PYTHON) Ferramentas/fonte_opinión.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Ferramentas/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Ferramentas/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Ferramentas/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Ferramentas/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Ferramentas/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Ferramentas/실행계층점검.py

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
