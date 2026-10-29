PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords аддалены_злучаць
remote: build
	$(PYTHON) Інструменты/выканаць_каманда.py --remote --resolution $(RESOLUTION) $(ARGS)
аддалены_злучаць: remote
test-remote: build
	$(PYTHON) Інструменты/원격접속시험.py
test-passwords: build
	$(PYTHON) Інструменты/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Сетка_Стэк -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Інструменты/зборка_сістэма.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Інструменты/COSL배포.py check
cosl-dist: build
	$(PYTHON) Інструменты/стварыць_выява.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Інструменты/COSL배포.py bundle
	$(PYTHON) Інструменты/재연결시험.py
desktop: build
	$(PYTHON) Інструменты/выканаць_каманда.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Інструменты/셸시험.py
test-windows: build
	$(PYTHON) Інструменты/창시험.py
test-swing: build
	$(PYTHON) Інструменты/화면요소시험.py
test-stream: build
	$(PYTHON) Інструменты/흐름시험.py
test-ftp: build
	$(PYTHON) Інструменты/파일전송시험.py
test-elf: build
	$(PYTHON) Інструменты/실행파일시험.py
test-examples: build
	$(PYTHON) Інструменты/예제시험.py
network: build
	$(PYTHON) Інструменты/выканаць_каманда.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Інструменты/코딩시험.py
test-desktop: build
	$(PYTHON) Інструменты/바탕화면시험.py
run: build
	$(PYTHON) Інструменты/выканаць_каманда.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Інструменты/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Інструменты/한글입력시험.py
	$(PYTHON) Інструменты/셸시험.py
	$(PYTHON) Інструменты/바탕화면시험.py
	$(PYTHON) Інструменты/창시험.py
	$(PYTHON) Інструменты/화면요소시험.py
	$(PYTHON) Інструменты/흐름시험.py
	$(PYTHON) Інструменты/코딩시험.py
	$(PYTHON) Інструменты/자바가상기계시험.py
	$(PYTHON) Інструменты/부팅시험.py
	$(PYTHON) Інструменты/꾸러미시험.py
	$(PYTHON) Інструменты/해상도시험.py
	$(PYTHON) Інструменты/창크기시험.py
image: build
	$(PYTHON) Інструменты/стварыць_выява.py --resolution $(RESOLUTION)
	$(PYTHON) Інструменты/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Інструменты/개발꾸러미내보내기.py

.PHONY: 모두 зборка_сістэма выканаць_каманда 시험 통신 працоўны_стол_выгляд выява_значэнне 개발꾸러미
모두: all
зборка_сістэма: build
выканаць_каманда: run
시험: test
통신: network
працоўны_стол_выгляд: desktop
выява_значэнне: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Інструменты/부팅시험.py
test-remmina: build
	$(PYTHON) Інструменты/원격한글시험.py
test-naming:
	$(PYTHON) Інструменты/명명검사.py --시언어
	$(PYTHON) Інструменты/직접호출검사.py
	$(PYTHON) Інструменты/крыніца_водгук.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Інструменты/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Інструменты/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Інструменты/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Інструменты/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Інструменты/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Інструменты/실행계층점검.py

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
