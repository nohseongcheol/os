PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords afstands_KOPPEL
remote: build
	$(PYTHON) Nutsmiddels/uitvoer_bevel.py --remote --resolution $(RESOLUTION) $(ARGS)
afstands_KOPPEL: remote
test-remote: build
	$(PYTHON) Nutsmiddels/원격접속시험.py
test-passwords: build
	$(PYTHON) Nutsmiddels/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Netwerk_Stapel -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Nutsmiddels/bou_stelsel.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Nutsmiddels/COSL배포.py check
cosl-dist: build
	$(PYTHON) Nutsmiddels/Skep_foto.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Nutsmiddels/COSL배포.py bundle
	$(PYTHON) Nutsmiddels/재연결시험.py
desktop: build
	$(PYTHON) Nutsmiddels/uitvoer_bevel.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Nutsmiddels/셸시험.py
test-windows: build
	$(PYTHON) Nutsmiddels/창시험.py
test-swing: build
	$(PYTHON) Nutsmiddels/화면요소시험.py
test-stream: build
	$(PYTHON) Nutsmiddels/흐름시험.py
test-ftp: build
	$(PYTHON) Nutsmiddels/파일전송시험.py
test-elf: build
	$(PYTHON) Nutsmiddels/실행파일시험.py
test-examples: build
	$(PYTHON) Nutsmiddels/예제시험.py
network: build
	$(PYTHON) Nutsmiddels/uitvoer_bevel.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Nutsmiddels/코딩시험.py
test-desktop: build
	$(PYTHON) Nutsmiddels/바탕화면시험.py
run: build
	$(PYTHON) Nutsmiddels/uitvoer_bevel.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Nutsmiddels/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Nutsmiddels/한글입력시험.py
	$(PYTHON) Nutsmiddels/셸시험.py
	$(PYTHON) Nutsmiddels/바탕화면시험.py
	$(PYTHON) Nutsmiddels/창시험.py
	$(PYTHON) Nutsmiddels/화면요소시험.py
	$(PYTHON) Nutsmiddels/흐름시험.py
	$(PYTHON) Nutsmiddels/코딩시험.py
	$(PYTHON) Nutsmiddels/자바가상기계시험.py
	$(PYTHON) Nutsmiddels/부팅시험.py
	$(PYTHON) Nutsmiddels/꾸러미시험.py
	$(PYTHON) Nutsmiddels/해상도시험.py
	$(PYTHON) Nutsmiddels/창크기시험.py
image: build
	$(PYTHON) Nutsmiddels/Skep_foto.py --resolution $(RESOLUTION)
	$(PYTHON) Nutsmiddels/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Nutsmiddels/개발꾸러미내보내기.py

.PHONY: 모두 bou_stelsel uitvoer_bevel 시험 통신 werkskerm_bekyk foto_VALUE 개발꾸러미
모두: all
bou_stelsel: build
uitvoer_bevel: run
시험: test
통신: network
werkskerm_bekyk: desktop
foto_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Nutsmiddels/부팅시험.py
test-remmina: build
	$(PYTHON) Nutsmiddels/원격한글시험.py
test-naming:
	$(PYTHON) Nutsmiddels/명명검사.py --시언어
	$(PYTHON) Nutsmiddels/직접호출검사.py
	$(PYTHON) Nutsmiddels/bron_resensie.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Nutsmiddels/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Nutsmiddels/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Nutsmiddels/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Nutsmiddels/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Nutsmiddels/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Nutsmiddels/실행계층점검.py

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
