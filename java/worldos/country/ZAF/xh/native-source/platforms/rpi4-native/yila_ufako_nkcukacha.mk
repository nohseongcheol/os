PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords kude_I_Connect
remote: build
	$(PYTHON) Izixhobo/ukwenza_umyalelo.py --remote --resolution $(RESOLUTION) $(ARGS)
kude_I_Connect: remote
test-remote: build
	$(PYTHON) Izixhobo/원격접속시험.py
test-passwords: build
	$(PYTHON) Izixhobo/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Inethiwekhi_fumba -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Izixhobo/yakha_inkqubo.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Izixhobo/COSL배포.py check
cosl-dist: build
	$(PYTHON) Izixhobo/yila_umfanekiso.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Izixhobo/COSL배포.py bundle
	$(PYTHON) Izixhobo/재연결시험.py
desktop: build
	$(PYTHON) Izixhobo/ukwenza_umyalelo.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Izixhobo/셸시험.py
test-windows: build
	$(PYTHON) Izixhobo/창시험.py
test-swing: build
	$(PYTHON) Izixhobo/화면요소시험.py
test-stream: build
	$(PYTHON) Izixhobo/흐름시험.py
test-ftp: build
	$(PYTHON) Izixhobo/파일전송시험.py
test-elf: build
	$(PYTHON) Izixhobo/실행파일시험.py
test-examples: build
	$(PYTHON) Izixhobo/예제시험.py
network: build
	$(PYTHON) Izixhobo/ukwenza_umyalelo.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Izixhobo/코딩시험.py
test-desktop: build
	$(PYTHON) Izixhobo/바탕화면시험.py
run: build
	$(PYTHON) Izixhobo/ukwenza_umyalelo.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Izixhobo/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Izixhobo/한글입력시험.py
	$(PYTHON) Izixhobo/셸시험.py
	$(PYTHON) Izixhobo/바탕화면시험.py
	$(PYTHON) Izixhobo/창시험.py
	$(PYTHON) Izixhobo/화면요소시험.py
	$(PYTHON) Izixhobo/흐름시험.py
	$(PYTHON) Izixhobo/코딩시험.py
	$(PYTHON) Izixhobo/자바가상기계시험.py
	$(PYTHON) Izixhobo/부팅시험.py
	$(PYTHON) Izixhobo/꾸러미시험.py
	$(PYTHON) Izixhobo/해상도시험.py
	$(PYTHON) Izixhobo/창크기시험.py
image: build
	$(PYTHON) Izixhobo/yila_umfanekiso.py --resolution $(RESOLUTION)
	$(PYTHON) Izixhobo/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Izixhobo/개발꾸러미내보내기.py

.PHONY: 모두 yakha_inkqubo ukwenza_umyalelo 시험 통신 idesktophu_bona umfanekiso_ixabiso 개발꾸러미
모두: all
yakha_inkqubo: build
ukwenza_umyalelo: run
시험: test
통신: network
idesktophu_bona: desktop
umfanekiso_ixabiso: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Izixhobo/부팅시험.py
test-remmina: build
	$(PYTHON) Izixhobo/원격한글시험.py
test-naming:
	$(PYTHON) Izixhobo/명명검사.py --시언어
	$(PYTHON) Izixhobo/직접호출검사.py
	$(PYTHON) Izixhobo/umthombo_uhlolo.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Izixhobo/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Izixhobo/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Izixhobo/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Izixhobo/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Izixhobo/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Izixhobo/실행계층점검.py

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
