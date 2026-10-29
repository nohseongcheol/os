PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords extern_Verbannen
remote: build
	$(PYTHON) Tools/ausféieren_Befeel.py --remote --resolution $(RESOLUTION) $(ARGS)
extern_Verbannen: remote
test-remote: build
	$(PYTHON) Tools/원격접속시험.py
test-passwords: build
	$(PYTHON) Tools/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Reseau_Stapel -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Tools/Build_System.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Tools/COSL배포.py check
cosl-dist: build
	$(PYTHON) Tools/Create_Bild.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Tools/COSL배포.py bundle
	$(PYTHON) Tools/재연결시험.py
desktop: build
	$(PYTHON) Tools/ausféieren_Befeel.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Tools/셸시험.py
test-windows: build
	$(PYTHON) Tools/창시험.py
test-swing: build
	$(PYTHON) Tools/화면요소시험.py
test-stream: build
	$(PYTHON) Tools/흐름시험.py
test-ftp: build
	$(PYTHON) Tools/파일전송시험.py
test-elf: build
	$(PYTHON) Tools/실행파일시험.py
test-examples: build
	$(PYTHON) Tools/예제시험.py
network: build
	$(PYTHON) Tools/ausféieren_Befeel.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Tools/코딩시험.py
test-desktop: build
	$(PYTHON) Tools/바탕화면시험.py
run: build
	$(PYTHON) Tools/ausféieren_Befeel.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Tools/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Tools/한글입력시험.py
	$(PYTHON) Tools/셸시험.py
	$(PYTHON) Tools/바탕화면시험.py
	$(PYTHON) Tools/창시험.py
	$(PYTHON) Tools/화면요소시험.py
	$(PYTHON) Tools/흐름시험.py
	$(PYTHON) Tools/코딩시험.py
	$(PYTHON) Tools/자바가상기계시험.py
	$(PYTHON) Tools/부팅시험.py
	$(PYTHON) Tools/꾸러미시험.py
	$(PYTHON) Tools/해상도시험.py
	$(PYTHON) Tools/창크기시험.py
image: build
	$(PYTHON) Tools/Create_Bild.py --resolution $(RESOLUTION)
	$(PYTHON) Tools/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Tools/개발꾸러미내보내기.py

.PHONY: 모두 Build_System ausféieren_Befeel 시험 통신 Desktop_Vue Bild_VALUE 개발꾸러미
모두: all
Build_System: build
ausféieren_Befeel: run
시험: test
통신: network
Desktop_Vue: desktop
Bild_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Tools/부팅시험.py
test-remmina: build
	$(PYTHON) Tools/원격한글시험.py
test-naming:
	$(PYTHON) Tools/명명검사.py --시언어
	$(PYTHON) Tools/직접호출검사.py
	$(PYTHON) Tools/Quell_Kritik.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Tools/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Tools/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Tools/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Tools/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Tools/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Tools/실행계층점검.py

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
