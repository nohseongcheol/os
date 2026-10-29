PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords mill_bogħod_AQBAD
remote: build
	$(PYTHON) Għodod/eżegwixxa_kmand.py --remote --resolution $(RESOLUTION) $(ARGS)
mill_bogħod_AQBAD: remote
test-remote: build
	$(PYTHON) Għodod/원격접속시험.py
test-passwords: build
	$(PYTHON) Għodod/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter netwerk_Munzell -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Għodod/bena_sistema.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Għodod/COSL배포.py check
cosl-dist: build
	$(PYTHON) Għodod/ħalaq_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Għodod/COSL배포.py bundle
	$(PYTHON) Għodod/재연결시험.py
desktop: build
	$(PYTHON) Għodod/eżegwixxa_kmand.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Għodod/셸시험.py
test-windows: build
	$(PYTHON) Għodod/창시험.py
test-swing: build
	$(PYTHON) Għodod/화면요소시험.py
test-stream: build
	$(PYTHON) Għodod/흐름시험.py
test-ftp: build
	$(PYTHON) Għodod/파일전송시험.py
test-elf: build
	$(PYTHON) Għodod/실행파일시험.py
test-examples: build
	$(PYTHON) Għodod/예제시험.py
network: build
	$(PYTHON) Għodod/eżegwixxa_kmand.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Għodod/코딩시험.py
test-desktop: build
	$(PYTHON) Għodod/바탕화면시험.py
run: build
	$(PYTHON) Għodod/eżegwixxa_kmand.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Għodod/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Għodod/한글입력시험.py
	$(PYTHON) Għodod/셸시험.py
	$(PYTHON) Għodod/바탕화면시험.py
	$(PYTHON) Għodod/창시험.py
	$(PYTHON) Għodod/화면요소시험.py
	$(PYTHON) Għodod/흐름시험.py
	$(PYTHON) Għodod/코딩시험.py
	$(PYTHON) Għodod/자바가상기계시험.py
	$(PYTHON) Għodod/부팅시험.py
	$(PYTHON) Għodod/꾸러미시험.py
	$(PYTHON) Għodod/해상도시험.py
	$(PYTHON) Għodod/창크기시험.py
image: build
	$(PYTHON) Għodod/ħalaq_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Għodod/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Għodod/개발꾸러미내보내기.py

.PHONY: 모두 bena_sistema eżegwixxa_kmand 시험 통신 desktop_wera IMAGE_VALUE 개발꾸러미
모두: all
bena_sistema: build
eżegwixxa_kmand: run
시험: test
통신: network
desktop_wera: desktop
IMAGE_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Għodod/부팅시험.py
test-remmina: build
	$(PYTHON) Għodod/원격한글시험.py
test-naming:
	$(PYTHON) Għodod/명명검사.py --시언어
	$(PYTHON) Għodod/직접호출검사.py
	$(PYTHON) Għodod/sors_reċensjoni.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Għodod/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Għodod/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Għodod/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Għodod/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Għodod/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Għodod/실행계층점검.py

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
