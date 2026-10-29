PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords masofaviy_ulash
remote: build
	$(PYTHON) Vositalar/bajarmoq_buyruq.py --remote --resolution $(RESOLUTION) $(ARGS)
masofaviy_ulash: remote
test-remote: build
	$(PYTHON) Vositalar/원격접속시험.py
test-passwords: build
	$(PYTHON) Vositalar/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Tarmoq_Stack -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Vositalar/nashr_tizim.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Vositalar/COSL배포.py check
cosl-dist: build
	$(PYTHON) Vositalar/Yaratish_rasm.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Vositalar/COSL배포.py bundle
	$(PYTHON) Vositalar/재연결시험.py
desktop: build
	$(PYTHON) Vositalar/bajarmoq_buyruq.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Vositalar/셸시험.py
test-windows: build
	$(PYTHON) Vositalar/창시험.py
test-swing: build
	$(PYTHON) Vositalar/화면요소시험.py
test-stream: build
	$(PYTHON) Vositalar/흐름시험.py
test-ftp: build
	$(PYTHON) Vositalar/파일전송시험.py
test-elf: build
	$(PYTHON) Vositalar/실행파일시험.py
test-examples: build
	$(PYTHON) Vositalar/예제시험.py
network: build
	$(PYTHON) Vositalar/bajarmoq_buyruq.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Vositalar/코딩시험.py
test-desktop: build
	$(PYTHON) Vositalar/바탕화면시험.py
run: build
	$(PYTHON) Vositalar/bajarmoq_buyruq.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Vositalar/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Vositalar/한글입력시험.py
	$(PYTHON) Vositalar/셸시험.py
	$(PYTHON) Vositalar/바탕화면시험.py
	$(PYTHON) Vositalar/창시험.py
	$(PYTHON) Vositalar/화면요소시험.py
	$(PYTHON) Vositalar/흐름시험.py
	$(PYTHON) Vositalar/코딩시험.py
	$(PYTHON) Vositalar/자바가상기계시험.py
	$(PYTHON) Vositalar/부팅시험.py
	$(PYTHON) Vositalar/꾸러미시험.py
	$(PYTHON) Vositalar/해상도시험.py
	$(PYTHON) Vositalar/창크기시험.py
image: build
	$(PYTHON) Vositalar/Yaratish_rasm.py --resolution $(RESOLUTION)
	$(PYTHON) Vositalar/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Vositalar/개발꾸러미내보내기.py

.PHONY: 모두 nashr_tizim bajarmoq_buyruq 시험 통신 ishchi_stol_ko_rinish rasm_VALUE 개발꾸러미
모두: all
nashr_tizim: build
bajarmoq_buyruq: run
시험: test
통신: network
ishchi_stol_ko_rinish: desktop
rasm_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Vositalar/부팅시험.py
test-remmina: build
	$(PYTHON) Vositalar/원격한글시험.py
test-naming:
	$(PYTHON) Vositalar/명명검사.py --시언어
	$(PYTHON) Vositalar/직접호출검사.py
	$(PYTHON) Vositalar/manba_taqriz.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Vositalar/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Vositalar/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Vositalar/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Vositalar/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Vositalar/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Vositalar/실행계층점검.py

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
