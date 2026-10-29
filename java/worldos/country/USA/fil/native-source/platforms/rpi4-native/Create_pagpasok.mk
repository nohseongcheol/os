PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords malayuan_CONNECT
remote: build
	$(PYTHON) Mga_Tool/Mag_execute_utos.py --remote --resolution $(RESOLUTION) $(ARGS)
malayuan_CONNECT: remote
test-remote: build
	$(PYTHON) Mga_Tool/원격접속시험.py
test-passwords: build
	$(PYTHON) Mga_Tool/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Network_Stack -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Mga_Tool/build_system.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Mga_Tool/COSL배포.py check
cosl-dist: build
	$(PYTHON) Mga_Tool/Create_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Mga_Tool/COSL배포.py bundle
	$(PYTHON) Mga_Tool/재연결시험.py
desktop: build
	$(PYTHON) Mga_Tool/Mag_execute_utos.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Mga_Tool/셸시험.py
test-windows: build
	$(PYTHON) Mga_Tool/창시험.py
test-swing: build
	$(PYTHON) Mga_Tool/화면요소시험.py
test-stream: build
	$(PYTHON) Mga_Tool/흐름시험.py
test-ftp: build
	$(PYTHON) Mga_Tool/파일전송시험.py
test-elf: build
	$(PYTHON) Mga_Tool/실행파일시험.py
test-examples: build
	$(PYTHON) Mga_Tool/예제시험.py
network: build
	$(PYTHON) Mga_Tool/Mag_execute_utos.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Mga_Tool/코딩시험.py
test-desktop: build
	$(PYTHON) Mga_Tool/바탕화면시험.py
run: build
	$(PYTHON) Mga_Tool/Mag_execute_utos.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Mga_Tool/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Mga_Tool/한글입력시험.py
	$(PYTHON) Mga_Tool/셸시험.py
	$(PYTHON) Mga_Tool/바탕화면시험.py
	$(PYTHON) Mga_Tool/창시험.py
	$(PYTHON) Mga_Tool/화면요소시험.py
	$(PYTHON) Mga_Tool/흐름시험.py
	$(PYTHON) Mga_Tool/코딩시험.py
	$(PYTHON) Mga_Tool/자바가상기계시험.py
	$(PYTHON) Mga_Tool/부팅시험.py
	$(PYTHON) Mga_Tool/꾸러미시험.py
	$(PYTHON) Mga_Tool/해상도시험.py
	$(PYTHON) Mga_Tool/창크기시험.py
image: build
	$(PYTHON) Mga_Tool/Create_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Mga_Tool/export_SDK.py
sdk: build
	$(PYTHON) Mga_Tool/export_SDK.py

.PHONY: 모두 build_system Mag_execute_utos 시험 통신 desktop_View IMAGE_VALUE 개발꾸러미
모두: all
build_system: build
Mag_execute_utos: run
시험: test
통신: network
desktop_View: desktop
IMAGE_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Mga_Tool/부팅시험.py
test-remmina: build
	$(PYTHON) Mga_Tool/원격한글시험.py
test-naming:
	$(PYTHON) Mga_Tool/명명검사.py --시언어
	$(PYTHON) Mga_Tool/직접호출검사.py
	$(PYTHON) Mga_Tool/pinagmulan_review.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Mga_Tool/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Mga_Tool/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Mga_Tool/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Mga_Tool/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Mga_Tool/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Mga_Tool/실행계층점검.py

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
