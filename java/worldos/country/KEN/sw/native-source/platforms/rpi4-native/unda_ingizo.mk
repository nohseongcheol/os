PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords kwa_mbali_UNGANISHA
remote: build
	$(PYTHON) Zana/tekeleza_amri.py --remote --resolution $(RESOLUTION) $(ARGS)
kwa_mbali_UNGANISHA: remote
test-remote: build
	$(PYTHON) Zana/원격접속시험.py
test-passwords: build
	$(PYTHON) Zana/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Mtandao_Mpororo -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Zana/jenga_mfumo.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Zana/COSL배포.py check
cosl-dist: build
	$(PYTHON) Zana/unda_picha.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Zana/COSL배포.py bundle
	$(PYTHON) Zana/재연결시험.py
desktop: build
	$(PYTHON) Zana/tekeleza_amri.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Zana/셸시험.py
test-windows: build
	$(PYTHON) Zana/창시험.py
test-swing: build
	$(PYTHON) Zana/화면요소시험.py
test-stream: build
	$(PYTHON) Zana/흐름시험.py
test-ftp: build
	$(PYTHON) Zana/파일전송시험.py
test-elf: build
	$(PYTHON) Zana/실행파일시험.py
test-examples: build
	$(PYTHON) Zana/예제시험.py
network: build
	$(PYTHON) Zana/tekeleza_amri.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Zana/코딩시험.py
test-desktop: build
	$(PYTHON) Zana/바탕화면시험.py
run: build
	$(PYTHON) Zana/tekeleza_amri.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Zana/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Zana/한글입력시험.py
	$(PYTHON) Zana/셸시험.py
	$(PYTHON) Zana/바탕화면시험.py
	$(PYTHON) Zana/창시험.py
	$(PYTHON) Zana/화면요소시험.py
	$(PYTHON) Zana/흐름시험.py
	$(PYTHON) Zana/코딩시험.py
	$(PYTHON) Zana/자바가상기계시험.py
	$(PYTHON) Zana/부팅시험.py
	$(PYTHON) Zana/꾸러미시험.py
	$(PYTHON) Zana/해상도시험.py
	$(PYTHON) Zana/창크기시험.py
image: build
	$(PYTHON) Zana/unda_picha.py --resolution $(RESOLUTION)
	$(PYTHON) Zana/hamisha_SDK.py
sdk: build
	$(PYTHON) Zana/hamisha_SDK.py

.PHONY: 모두 jenga_mfumo tekeleza_amri 시험 통신 Eneo_kazi_Onesha picha_thamani 개발꾸러미
모두: all
jenga_mfumo: build
tekeleza_amri: run
시험: test
통신: network
Eneo_kazi_Onesha: desktop
picha_thamani: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Zana/부팅시험.py
test-remmina: build
	$(PYTHON) Zana/원격한글시험.py
test-naming:
	$(PYTHON) Zana/명명검사.py --시언어
	$(PYTHON) Zana/직접호출검사.py
	$(PYTHON) Zana/원문검토.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Zana/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Zana/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Zana/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Zana/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Zana/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Zana/실행계층점검.py

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
